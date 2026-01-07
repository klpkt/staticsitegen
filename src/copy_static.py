import os, shutil

def copy_static(path):
    if os.path.isfile(f"static/{path}"):
        print(f"Copying static{path} to public{path}")
        shutil.copy(f"static/{path}", f"public/{path}")
    else:
        print(f"Creating folder public{path}/")
        os.mkdir(f"public/{path}")
        for sub_path in os.listdir(f"static/{path}"):
            copy_static(f"{path}/{sub_path}")