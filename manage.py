### Site Generator created  1/24 ###
### refactored 2/3/21 ###
### jinja2 added 2/13/21###
import sys
import utils

#print if no argument provided 
if len(sys.argv) == 1:
    print("Please specify ’build’ or ’new’ as an argument")
    quit()

command = sys.argv[1]
if command == "build":
    print("Build was specified")
    if __name__ == "__main__":
        utils.main()
elif command == "new":
    print("New page was specified")
    file_name_input = input("Please provide new file name: ")
    new_file_name = utils.create_new_html_page(file_name_input)
    print('Content page "' + new_file_name + '''" was created in 'content' folder.''')
else:
    print("Please specify ’build’ or ’new’")


