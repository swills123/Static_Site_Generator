from htmlnode import LeafNode, ParentNode
from inline_markdown import text_to_textnodes
from textnode import TextNode, TextType, text_node_to_html_node
from enum import Enum



class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADER = "header"
    CODE = "code"
    QUOTE = "quote"
    UNORDER_LIST = "unorder_list"
    ORDER_LIST = "order_list"

def markdown_to_blocks(text: str) -> list[TextNode]:
    raw_blocks = text.split("\n\n")
    blocks = []
    for block in raw_blocks:
        stripped = block.strip()
        if stripped == "":
            continue
        blocks.append(stripped)
    return blocks

def markdown_to_html_node(text: str) -> ParentNode:
    blocks = markdown_to_blocks(text)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children)

def block_to_block_type(block:str) -> BlockType:
    stripped = block.strip()
    if stripped.startswith("#"):
        return BlockType.HEADER
    elif stripped.startswith("```"):
        return BlockType.CODE
    elif stripped.startswith(">"): 
        return BlockType.QUOTE
    elif stripped.startswith("- "):
        return BlockType.UNORDER_LIST
    elif stripped[0].isdigit() and stripped[1:3] == ". ":
        return BlockType.ORDER_LIST
    else:
        return BlockType.PARAGRAPH
    
def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        child = text_node_to_html_node(text_node)
        children.append(child)
    return children

def paragraph_to_html_node(block):
    text = block.replace("\n", " ")
    children = text_to_children(text)
    return ParentNode("p", children)

def headers_to_html_node(block):
    parts = block.split(" ", 1)
    level = len(parts[0])
    text = parts[1]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)

def code_to_html_node(block):
    text = block.strip("`")
    if text.startswith("\n"):
        text = text[1:]
    text_node = TextNode(text, TextType.CODE)
    child = text_node_to_html_node(text_node)
    return ParentNode("pre", [child])

def quote_to_html_node(block):
    lines = block.split("\n")
    cleaned_lines = []
    for line in lines:
        cleaned = line.lstrip("> ").rstrip()
        cleaned_lines.append(cleaned)
    text = " ".join(cleaned_lines)
    children = text_to_children(text)
    return ParentNode("blockquote", children)

def unorder_list_to_html_node(block):
    lines = block.split("\n")
    list_items = []
    for line in lines:
        cleaned = line.lstrip("- ").rstrip()
        children = text_to_children(cleaned)
        list_item_node = ParentNode("li", children)
        list_items.append(list_item_node)
    return ParentNode("ul", list_items)

def ordered_list_to_html_node(block):
    lines = block.split("\n")
    list_items = []
    for line in lines:
        cleaned = line.split(". ", 1)[1]
        children = text_to_children(cleaned)
        list_item_node = ParentNode("li", children)
        list_items.append(list_item_node)
    return ParentNode("ol", list_items)

def block_to_html_node(block:str) -> ParentNode:
    block_type = block_to_block_type(block)
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    elif block_type == BlockType.HEADER:
        return headers_to_html_node(block)
    elif block_type == BlockType.CODE:
        return code_to_html_node(block)
    elif block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    elif block_type == BlockType.UNORDER_LIST:
        return unorder_list_to_html_node(block)
    elif block_type == BlockType.ORDER_LIST:
        return ordered_list_to_html_node(block)
    else:
        raise ValueError(f"Unknown block type: {block_type}")


def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
    raise ValueError("No h1 header found")
