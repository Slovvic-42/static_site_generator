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
