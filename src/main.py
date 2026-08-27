import os
import shutil
from markdown_blocks import markdown_to_html_node, extract_title


def copy_static_to_public(src, dst):
    if not os.path.exists(dst):
        os.mkdir(dst)

    for item in os.listdir(src):
        src_path = os.path.join(src, item)
        dst_path = os.path.join(dst, item)

        if os.path.isfile(src_path):
            print(f"Copying file: {src_path} -> {dst_path}")
            shutil.copy(src_path, dst_path)
        else:
            print(f"Creating directory: {dst_path}")
            copy_static_to_public(src_path, dst_path)
            
def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as f:
        markdown_content = f.read()
    print("Read markdown file successfully")
    with open(template_path) as f:
        template_content = f.read()
    print("Read template file successfully")
    html_node = markdown_to_html_node(markdown_content)
    print("Converted markdown to HTML node")
    content_html = html_node.to_html()
    print("Converted HTML node to string")
    title = extract_title(markdown_content)
    print(f"Extracted title: {title}")
    final_html = template_content.replace("{{ Title }}", title)
    final_html = final_html.replace("{{ Content }}", content_html)
    print("Replaced placeholders")
    dest_dir = os.path.dirname(dest_path)
    if dest_dir != "":
        os.makedirs(dest_dir, exist_ok=True)
    print(f"Ensured directory exists: {dest_dir}")
    with open(dest_path, "w") as f:
        f.write(final_html)
    print("Wrote file successfully")
    
def generate_pages_recursive(dir_path_content, template_path, dest_dir_public):
    for item in os.listdir(dir_path_content):
        src_path = os.path.join(dir_path_content, item)
        dst_path = os.path.join(dest_dir_public, item)
        if os.path.isfile(src_path) and src_path.endswith(".md"):
            generate_page(src_path, template_path, dst_path.replace(".md", ".html"))
        elif os.path.isdir(src_path):
            generate_pages_recursive(src_path, template_path, dst_path)

def main():
    if os.path.exists("public"):
        shutil.rmtree("public")
    copy_static_to_public("static", "public")
    generate_pages_recursive("content", "template.html", "public")


main()