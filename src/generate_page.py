import os, shutil
from markdown_to_html_node import markdown_to_html_node
from extract_title import extract_title

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as f:
        markdown = f.read()
    with open(template_path) as f:
        template = f.read()
    content_html = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    final_html = template.replace("{{ Title }}", title).replace("{{ Content }}", content_html)
    old = final_html
    final_html = final_html.replace('href="/', f'href="{basepath}')
    final_html = final_html.replace('src="/', f'href="{basepath}')
    dirs = "docs/" + '/'.join(dest_path.split('/')[1:-1])
    os.makedirs(dirs, exist_ok=True)
    with open(dest_path, 'w') as f:
        f.write(final_html)

def generate_pages_recursive(content_path, template_path, basepath):
    # first call, content_path is ""
    if os.path.isfile(f"content/{content_path}"):
        print(f"Copying content{content_path} to docs{content_path}")
        md_file = f"content{content_path}"
        html_file = f"docs{content_path[:-3]}.html"
        generate_page(md_file, template_path, html_file, basepath)
    else:
        if not os.path.exists(f"docs/{content_path}"):
            print(f"Creating folder docs{content_path}")
            os.mkdir(f"docs/{content_path}")
        for sub_path in os.listdir(f"content/{content_path}"):
            generate_pages_recursive(f"{content_path}/{sub_path}", template_path, basepath)