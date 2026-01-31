from textnode import TextNode, TextType
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
        else:
            parts = node.text.split(delimiter)
            if len(parts) % 2 == 0:
                raise Exception("Delimiter not found in text block")
            for i in range(len(parts)):
                if parts[i] == "":
                    continue
                if i % 2 == 0:
                    new_nodes.append(TextNode(parts[i], TextType.TEXT))
                else:
                    new_nodes.append(TextNode(parts[i], text_type))
    return new_nodes

def extract_markdown_images(text): 
        matches = re.findall(r"!\[([^\]]*)\]\(([^\)]+)\)", text)
        return matches
    
def extract_markdown_links(text):
        matches = re.findall(r"\[([^\]]*)\]\(([^\)]+)\)", text)
        return matches

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if not node.text_type == TextType.TEXT:
             new_nodes.append(node)
             continue
        matches = extract_markdown_images(node.text)
        if len(matches) == 0:
            new_nodes.append(node)
            continue
        updated_text = node.text
        for tuple in matches:
            image_alt = tuple[0]
            image_link = tuple[1]
            sections = updated_text.split(f"![{image_alt}]({image_link})", 1)
            if sections[0] != "":
                the_text = TextNode(sections[0], TextType.TEXT)
                new_nodes.append(the_text)
            the_link = TextNode(image_alt, TextType.IMAGE, image_link)
            new_nodes.append(the_link)
            updated_text = sections[1]
        if updated_text != "":
            trailing_text = TextNode(updated_text, TextType.TEXT)
            new_nodes.append(trailing_text)
    return new_nodes
        
     
def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        matches = extract_markdown_links(node.text)
        if len(matches) == 0:
            new_nodes.append(node)
            continue
        updated_text = node.text
        for tuple in matches:
            anchor = tuple[0]
            url = tuple[1]
            sections = updated_text.split(f"[{anchor}]({url})", 1)
            if len(sections) > 1:
                after = sections[1]
            else:
                after = ""
            if sections[0] != "":
                the_text = TextNode(sections[0], TextType.TEXT)
                new_nodes.append(the_text)
            the_link = TextNode(anchor, TextType.LINK, url)
            new_nodes.append(the_link)
            updated_text = after
        if updated_text != "":
            trailing = TextNode(updated_text, TextType.TEXT)
            new_nodes.append(trailing)
    return new_nodes

def text_to_textnodes(text):
    new_nodes = [TextNode(text, TextType.TEXT)]
    new_nodes = split_nodes_link(split_nodes_image(new_nodes))
    new_nodes = split_nodes_delimiter(new_nodes, "**", TextType.BOLD)
    new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
    new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)
    return new_nodes