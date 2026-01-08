import os, shutil, sys

from copy_static import copy_static
from generate_page import generate_pages_recursive

def main():
    args = sys.argv
    basepath = "/"
    if len(args) >= 2:
        basepath = args[1]

    if os.path.exists("docs"):
        shutil.rmtree("docs")
    copy_static("")
    generate_pages_recursive("", "template.html", basepath)


if __name__ == "__main__":
    main()