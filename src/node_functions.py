from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, TextType

def text_node_to_html_node(TextNode):
    if TextNode.text_type == TextType.TEXT:
        return LeafNode(tag=None, value=TextNode.text)
    elif TextNode.text_type == TextType.BOLD:
        return LeafNode(tag="b", value=TextNode.text)
    elif TextNode.text_type == TextType.ITALIC:
        return LeafNode(tag="i", value=TextNode.text)
    elif TextNode.text_type == TextType.CODE:
        return LeafNode(tag="code", value=TextNode.text)
    elif TextNode.text_type == TextType.LINK:
        if not TextNode.url:
            raise ValueError("ANCHOR type must have a url")
        return LeafNode(tag="a", value=TextNode.text, props={"href": TextNode.url})
    elif TextNode.text_type == TextType.IMAGE:
        return LeafNode(tag="img", value="", props={"alt": TextNode.text, "src": TextNode.url if TextNode.url else ""})
    else:
        raise ValueError(f"Unsupported text type: {TextNode.text_type}")

def extract_markdown_images(text):
    import re 
    tuple_pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(tuple_pattern, text)

def extract_markdown_links(text):
    import re
    tuple_pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(tuple_pattern, text)

def split_nodes_delimiter(old_nodes: list, delimiter, text_type: TextType):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            parts = node.text.split(delimiter)
            if len(parts) % 2 == 0:
                raise ValueError(f"Unmatched delimiter '{delimiter}' in text: {node.text}")
            for i, part in enumerate(parts):
                if i % 2 == 0:
                    if part:
                        new_nodes.append(TextNode(text=part, text_type=TextType.TEXT))
                else:
                    new_nodes.append(TextNode(text=part, text_type=text_type))
    return new_nodes

def split_nodes_image(old_nodes: list):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            remaining = node.text
            image_chunks = extract_markdown_images(node.text)
            if len(image_chunks) == 0:
                new_nodes.append(node)
                continue
            for chunk in image_chunks:
                sections = remaining.split(f"![{chunk[0]}]({chunk[1]})", 1)
                if len(sections) != 2:
                    raise ValueError(f"Unexpected error splitting text: {remaining} with image markdown ![{chunk[0]}]({chunk[1]})")
                if sections[0]:
                    new_nodes.append(TextNode(text=sections[0], text_type=TextType.TEXT))
                remaining = sections[1]
                new_nodes.append(TextNode(text=chunk[0], text_type=TextType.IMAGE, url=chunk[1]))
            if remaining:
                new_nodes.append(TextNode(text=remaining, text_type=TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes: list):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            remaining = node.text
            link_chunks = extract_markdown_links(node.text)
            if len(link_chunks) == 0:
                new_nodes.append(node)
                continue
            for chunk in link_chunks:
                sections = remaining.split(f"[{chunk[0]}]({chunk[1]})", 1)
                if len(sections) != 2:
                    raise ValueError(f"Unexpected error splitting text: {remaining} with link markdown [{chunk[0]}]({chunk[1]})")
                if sections[0]:
                    new_nodes.append(TextNode(text=sections[0], text_type=TextType.TEXT))
                remaining = sections[1]
                new_nodes.append(TextNode(text=chunk[0], text_type=TextType.LINK, url=chunk[1]))
            if remaining:
                new_nodes.append(TextNode(text=remaining, text_type=TextType.TEXT))
    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text=text, text_type=TextType.TEXT)]
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    return nodes
