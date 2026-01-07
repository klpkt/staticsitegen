import os, shutil

from copy_static import copy_static
from generate_page import generate_page

def main():
    if os.path.exists("public"):
        shutil.rmtree("public")
    copy_static("")
    generate_page("content/index.md", "template.html", "public/index.html")


if __name__ == "__main__":
    main()