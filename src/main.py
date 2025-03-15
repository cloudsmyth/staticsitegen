import os
import shutil
import sys

from utils import extract_title
from md_to_html import markdown_to_html_node


def main():
    base_path = "/"
    if len(sys.argv) > 1:
        base_path = sys.argv[1]
        print(base_path)

    source = "static"
    dest = "docs"
    copy_dirs(source, dest)
    generate_all_pages("content", "template.html", dest, base_path)


def copy_dirs(source_dir, dest_dir):
    if not os.path.exists(source_dir):
        print(f"Source directory {source_dir} does not exist")
        return

    if os.path.exists(dest_dir):
        print("Cleaning out destination dir...")
        shutil.rmtree(dest_dir)

    os.mkdir(dest_dir)

    recursive_copy(source_dir, dest_dir)
    print("Copying complete!")


def recursive_copy(source_dir, dest_dir):
    for item in os.listdir(source_dir):
        source_path = os.path.join(source_dir, item)
        dest_path = os.path.join(dest_dir, item)

        if os.path.isdir(source_path):
            if not os.path.exists(dest_path):
                print(f"Directory made: {dest_path}")
                os.mkdir(dest_path)
            recursive_copy(source_path, dest_path)
        else:
            shutil.copy(source_path, dest_path)


def generate_all_pages(from_dir, template_path, dest_dir, base_path):
    print('Generating all pages....')
    if not os.path.exists(from_dir):
        print(f"{from_dir} does not exist...")
        return

    for item in os.listdir(from_dir):
        from_path = os.path.join(from_dir, item)
        dest_path = os.path.join(dest_dir, item)

        if os.path.isdir(from_path):
            if not os.path.exists(dest_path):
                print(f"Content directory made: {dest_path}")
                os.mkdir(dest_path)
            generate_all_pages(from_path, template_path, dest_path, base_path)
        else:
            dest_path = dest_path.replace(".md", ".html")
            generate_page(from_path, template_path, dest_path, base_path)
    print('Finished!')


def generate_page(from_path, template_path, dest_path, base_path):
    print('Generating page {from_path} to {dest_path} using {template_path}')
    with open(from_path, 'r') as file:
        markdown = file.read()
    with open(template_path, 'r') as file:
        template = file.read()
    title = extract_title(markdown)
    template = template.replace("{{ Title }}", title)

    nodes = markdown_to_html_node(markdown).to_html()
    template = template.replace("{{ Content }}", nodes)
    template = template.replace('href="/', f'href="{base_path}')
    template = template.replace('src="/', f'src="{base_path}')
    with open(dest_path, 'w') as file:
        file.write(template)


main()
