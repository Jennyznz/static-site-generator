import os, shutil, sys
from textnode import TextNode, TextType
from block_markdown import markdown_to_html_node

def main():
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    else:
        basepath = "/"
    copy_src_to_dest("static", "docs")
    generate_pages_recursive("content", "template.html", "docs", basepath)

def copy_src_to_dest(src, dest):
    if not os.path.exists(src):
        return
    if not os.path.exists(dest):
        os.mkdir(dest)
    else:
        # Delete and recreate dest directory
        shutil.rmtree(dest)
        os.mkdir(dest)
    # Recursively copy src content
    src_content = os.listdir(src)
    for content in src_content:
        path_to_content = os.path.join(src, content)
        if os.path.isfile(path_to_content):
            shutil.copy(path_to_content, dest)
        else: # Subdirectory
            new_subdirectory = os.path.join(dest, content)
            os.mkdir(new_subdirectory)
            copy_src_to_dest(path_to_content, new_subdirectory)

def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line[:2] == "# ":
            return line[2:].strip()
    raise Exception("No Title found")

def generate_page(from_path, template_path, dest_path, basepath):
    fp = open(from_path)
    fp_content = fp.read()
    tp = open(template_path)
    tp_content = tp.read()

    fp_to_html_node = markdown_to_html_node(fp_content)
    fp_to_html = fp_to_html_node.to_html()
    fp_title = extract_title(fp_content)

    modified_template = tp_content.replace("{{ Title }}", fp_title)
    modified_template = modified_template.replace("{{ Content }}", fp_to_html)
    modified_template = modified_template.replace('href="/', f'href="{basepath}')
    modified_template = modified_template.replace('src="/', f'src="{basepath}')


    dest_dir = os.path.dirname(dest_path)  # Returns the last directory in the given path
    if dest_dir != "":
        os.makedirs(dest_dir, exist_ok=True)    # Make the destination directory if it doesn't exist
    
    dest_file = open(dest_path, "w") 
    dest_file.write(modified_template)

    fp.close()
    tp.close()
    dest_file.close()

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    content_entries = os.listdir(dir_path_content)
    for entry in content_entries:
        entry_path = os.path.join(dir_path_content, entry)
        if os.path.isfile(entry_path):
            parts = entry.split(".")
            file_name = parts[0]
            dest_file_path = os.path.join(dest_dir_path, f"{file_name}.html")
            generate_page(entry_path, template_path, dest_file_path, basepath)
        else: # Directory
            next_dest = os.path.join(dest_dir_path, entry)
            os.makedirs(next_dest, exist_ok=True)
            generate_pages_recursive(entry_path, template_path, next_dest, basepath)

main()