### Site Generator created  1/24 ###
### refactored 2/3/21 ###
### jinja2 added 2/13/21###
import datetime
import glob
import os
from jinja2 import Template
import re
##########################################################

### Create dictionaries - pages and blog_posts

def create_page_list():
    all_html_files = glob.glob("content/*.html")
    pages = []
    for file in all_html_files:
        filename = os.path.basename(file)
        name_only, extension = os.path.splitext(filename)
        title = name_only.capitalize()
        content = "./content/" + filename
        output = "./docs/" + filename
        pages.append({
            "title": title,
            "filename": content,
            "output": output,
            "link": filename,
        })
    return pages


def create_blog_posts_list():
    all_blog_posts = glob.glob("blog/*.html")
    blog_posts_dict = []
    for post in all_blog_posts:
        post_filename = os.path.basename(post)
        name_only, extension = os.path.splitext(post_filename)
        filename = "blog/" + post_filename
        output = "./docs/" + post_filename
        #grab post info from blog post html
        blog_post_html = open(filename).read()
        image_search = re.search(r'src=(.*?) class', blog_post_html).group(1)
        date_search = re.search(r'<h6>(.*?)</h6>', blog_post_html).group(1)
        title_search = re.search(r'<h1>(.*?)</h1>', blog_post_html).group(1)
        subtitle_search = re.search(r'<h3>(.*?)</h3>', blog_post_html).group(1)
        #prevent func from bombing
        if False:
            print("Blog information in html files is incomplete. These must be filled in before site can be generated. Aborting site generation.")
            quit()
        #else:
        #    image = image_search.group(1)
        #    date = date_search.group(1)
        ######
        blog_posts_dict.append({
            "filename": filename,
            "date": date_search,
            "title": title_search,
            "subtitle": subtitle_search,
            "output": output,
            "image": image_search,
        })
    return blog_posts_dict


### Create Blank html page (in content directory)

def create_new_html_page(file_name_input):
    #file_name scrubbed
    content_template_html = """<div class="row"></div>"""
    open("./content/" + file_name_input, "w+").write(content_template_html)
    return file_name_input


### Read input files

def read_content(file_name):
    return open(file_name).read()

### Placeholder replacement, using Jinja

def placeholder_replacement_base(base,page_title,content,pages):
    base = Template(base)
    return base.render({
            'pages_dict': pages,
            'content': content,
            'title': page_title,
            'get_year': datetime.datetime.now().strftime("%Y")
})


### write 'thoughts' blog pages

def write_blog_posts(blog_posts,base,pages):
    for post in blog_posts:
        blog_content = open(post['filename']).read()
        #write complete blog page
        base_template = Template(base)
        blog_page_final = base_template.render({
                                'title': 'Thoughts',
                                'pages_dict': pages,
                                'content': blog_content,
                                'get_year': datetime.datetime.now().strftime("%Y"),
        })
        open(post['output'], "w+").write(blog_page_final)

def write_thoughts_blog_past_posts(blog_posts_info,past_posts_html):
    blog_past_posts = '' #this is the placeholder to append each old post info
    for post in reversed(blog_posts_info):
        #define variables
        blog_post_title = post['title']
        blog_post_subtitle = post['subtitle']
        blog_post_date = post['date']
        blog_post_output = post['output'].replace('/docs','')
        blog_post_image = post['image']
        blog_post_filename = post['filename']
        #read input files
        past_post_layout = open(past_posts_html).read()
        #set variable text
        past_post_layout_template = Template(past_post_layout)
        past_post_layout_template_with_subs = past_post_layout_template.render({
                            'blog_post_link': blog_post_output,
                            'blog_post_title': blog_post_title,
                            'blog_post_date': blog_post_date,
                            'blog_post_subtitle': blog_post_subtitle,
                            'blog_post_image': blog_post_image,
        })
        blog_past_posts = blog_past_posts + past_post_layout_template_with_subs
    return blog_past_posts
    
    
def write_thoughts_content(thoughts_base,blog_posts,blog_past_posts):
    #write 'thoughts' (blog_post_image, blog_post_link, blog_post_title, blog_post_subtitle, blog_past_posts)
    base_template = Template(thoughts_base)
    last = True
    for post in reversed(blog_posts):
        if last:
            last = False
            return base_template.render(
                blog_post_image = post['image'],
                blog_post_link = post['output'].replace('/docs',''),
                blog_post_title = post['title'],
                blog_post_subtitle = post['subtitle'],
                blog_past_posts = blog_past_posts,
            )


###########################################################################################
def main():
    pages = create_page_list()
    for page in pages:
        #define variables
        file_name = page['filename']
        file_output = page['output']
        file_title = page['title']
        #read input files
        base = open("./templates/base.html").read()
        base_html = read_content(file_name)
        blog_posts_dict = create_blog_posts_list()
        if page['title'] == 'Thoughts':
            #write specific blog post
            write_blog_posts(blog_posts_dict,base,pages)
            #write thoughts - first past posts, then complete page
            blog_past_posts = write_thoughts_blog_past_posts(blog_posts_dict,"./templates/blog_past_post_base.html")
            thought_content = write_thoughts_content(base_html,blog_posts_dict,blog_past_posts)
            #write 'content' for Thoughts main page
            complete_page = placeholder_replacement_base(base,file_title,thought_content,pages)
        else:
            complete_page = placeholder_replacement_base(base,file_title,base_html,pages)
        open(file_output, "w+").write(complete_page)
    

    print('Site complete! Please review for accuracy.')
 ###########################################################################################
