import os

DEST_FOLDER = "templates"
DEST_FILE = "index_with_content.html"

def get_parent_way():
    basedir = os.path.abspath(os.getcwd())
    workbooks_dir = os.path.abspath(os.path.join(basedir, '.'))
    return workbooks_dir

def get_default_t_file(dest_folder=DEST_FOLDER, dest_file=DEST_FILE):
    par_way = get_parent_way()
    answer = "{0}\{1}\{2}".format(par_way, dest_folder, dest_file)
    return answer

if __name__ == "__main__":
    print(get_default_t_file())
