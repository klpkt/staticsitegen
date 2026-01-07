import os, shutil
from markdown_to_html_node import markdown_to_html_node
from extract_title import extract_title

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as f:
        markdown = f.read()
    with open(template_path) as f:
        template = f.read()
    content_html = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    final_html = template.replace("{{ Title }}", title).replace("{{ Content }}", content_html)
    dirs = "public/" + '/'.join(dest_path.split('/')[1:-1])
    os.makedirs(dirs, exist_ok=True)
    with open(dest_path, 'w') as f:
        f.write(final_html)