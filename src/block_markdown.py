from blocktype import BlockType
from htmlnode import HTMLNode, ParentNode, LeafNode
from textnode import TextNode, TextType, text_node_to_html_node
from inline_markdown import text_to_textnodes
import re

def markdown_to_blocks(markdown):
    block_strings = []
    parts = markdown.split("\n\n")
    for part in parts:
        if part != "":
            block_strings.append(part.strip())
    return block_strings

def block_to_block_type(markdown):
    lines = markdown.split("\n")
    if len(lines) == 1 and re.match(r"^(#{1,6})\s+.+$", lines[0]):
        return BlockType.HEADING
    elif lines[0] == "```" and lines[-1] == "```":
        return BlockType.CODE
    else:
        quote = True
        unordered = True
        ordered = True
        for index, line in enumerate(lines):
            if line != "":
                if line[0] != ">":
                    quote = False
                if len(line) > 1:
                    if line[0] != "-" or line[1] != " ":
                        unordered = False
                if not line.startswith(f"{index + 1}."):
                    ordered = False
        if quote:
            return BlockType.QUOTE
        elif unordered:
            return BlockType.UNORDERED_LIST
        elif ordered:
            return BlockType.ORDERED_LIST
        else:
            return BlockType.PARAGRAPH

def get_header_text(block, header_num):
    return block[header_num + 1:]

def get_header_number(block):
    for index, char in enumerate(block):
        if char != "#":
            return index
        
def get_code_text(block):
    lines = block.split("\n")
    if lines and lines[0].startswith("```"):
        lines = lines[1:]
    if lines and lines[-1].startswith("```"):    
        lines = lines[:-1]
    return "\n".join(lines)

def get_quote_text(block):
    new_lines = []
    lines = block.split("\n")
    for line in lines:
        new_lines.append(line[1:].lstrip())
    return " ".join(new_lines)

def get_ul_items_text(block):
    new_lines = []
    lines = block.split("\n")
    for line in lines:
        line = line[2:]
        new_lines.append(line)
    return new_lines

def get_ol_items_text(block):
    new_lines = []
    lines = block.split("\n")
    for index, line in enumerate(lines):
        line = line[3 + index // 9:]
        new_lines.append(line)
    return new_lines

def get_paragraph_text(block):
    text = " ".join(block.split("\n"))
    return text


def markdown_to_html_node(markdown):
    children = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.PARAGRAPH:
                text = get_paragraph_text(block)
                sub_children = text_to_children(text)      
                node = ParentNode('p', sub_children) 
                children.append(node)
            case BlockType.HEADING:
                header_number = get_header_number(block)
                text = get_header_text(block, header_number)
                sub_children = text_to_children(text)      
                node = ParentNode(f'h{header_number}', sub_children)
                children.append(node)  
            case BlockType.CODE:
                code_text = get_code_text(block)
                if not code_text.endswith("\n"):
                    code_text += "\n"
                node = TextNode(code_text, TextType.CODE)
                code_node = text_node_to_html_node(node) 
                pre_node = ParentNode('pre', [code_node])
                children.append(pre_node)
            case BlockType.QUOTE:
                text = get_quote_text(block)
                sub_children = text_to_children(text)      
                node = ParentNode('blockquote', sub_children)
                children.append(node)
            case BlockType.UNORDERED_LIST:
                ul_items_text = get_ul_items_text(block)
                items_and_their_children = []
                for item in ul_items_text:
                    child_node = ParentNode("li", text_to_children(item))
                    items_and_their_children.append(child_node)
                node = ParentNode('ul', items_and_their_children)
                children.append(node)
            case BlockType.ORDERED_LIST:
                ol_items_text = get_ol_items_text(block)
                items_and_their_children = []
                for item in ol_items_text:
                    child_node = ParentNode("li", text_to_children(item))
                    items_and_their_children.append(child_node)
                node = ParentNode('ol', items_and_their_children)
                children.append(node)
    return ParentNode("div", children=children)

def text_to_children(text):
    nodes = text_to_textnodes(text)
    children = []
    for node in nodes:
        children.append(text_node_to_html_node(node))
    return children