import os, shutil

from copy_static import copy_static
from generate_page import generate_pages_recursive

def main():
    if os.path.exists("public"):
        shutil.rmtree("public")
    copy_static("")
    generate_pages_recursive("", "template.html")


if __name__ == "__main__":
    main()