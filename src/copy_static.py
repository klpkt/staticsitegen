import os, shutil

def copy_static(path):
    if os.path.isfile(f"static/{path}"):
        print(f"Copying static{path} to docs{path}")
        shutil.copy(f"static/{path}", f"docs/{path}")
    else:
        print(f"Creating folder docs{path}/")
        os.mkdir(f"docs/{path}")
        for sub_path in os.listdir(f"static/{path}"):
            copy_static(f"{path}/{sub_path}")