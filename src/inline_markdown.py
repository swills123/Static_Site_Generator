from textnode import TextNode, TextType
import re



def split_nodes_delimiter(old_nodes:list[TextNode], delimiter: str, text_type:TextType) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        parts = old_node.text.split(delimiter)
        if len(parts) % 2 == 0:
            raise ValueError("Invalid markdown, formatted section not closed")
        for i, part in enumerate(parts):
            if part == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(part, TextType.TEXT))
            else:
                new_nodes.append(TextNode(part, text_type)) 
    return new_nodes 

def extract_markdown_images(text):
    matches = re.findall(r'!\[(.*?)\]\((.*?)\)', text)
    return matches


def extract_markdown_links(text):
    matches = re.findall(r'(?<!!)\[(.*?)\]\((.*?)\)', text)
    return matches


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        parts = re.split(r'(!\[.*?\]\(.*?\))', old_node.text)
        for part in parts:
            if part == "":
                continue
            image_match = re.match(r'!\[(.*?)\]\((.*?)\)', part)
            if image_match:
                alt_text, url = image_match.groups()
                new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
            else:
                new_nodes.append(TextNode(part, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        parts = re.split(r'(?<!!)(\[.*?\]\(.*?\))', old_node.text)
        for part in parts:
            if part == "":
                continue
            link_match = re.match(r'(?<!!)\[(.*?)\]\((.*?)\)', part)
            if link_match:
                link_text, url = link_match.groups()
                new_nodes.append(TextNode(link_text, TextType.LINK, url))
            else:
                new_nodes.append(TextNode(part, TextType.TEXT))
    return new_nodes

def text_to_textnodes(text: str) -> list[TextNode]:
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

         

    