from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, TextType

def text_node_to_html_node(TextNode):
    if TextNode.text_type == TextType.PLAIN:
        return LeafNode(tag=None, value=TextNode.text)
    elif TextNode.text_type == TextType.BOLD:
        return LeafNode(tag="b", value=TextNode.text)
    elif TextNode.text_type == TextType.ITALIC:
        return LeafNode(tag="i", value=TextNode.text)
    elif TextNode.text_type == TextType.UNDERLINE:
        return LeafNode(tag="u", value=TextNode.text)
    elif TextNode.text_type == TextType.STRIKETHROUGH:
        return LeafNode(tag="s", value=TextNode.text)
    elif TextNode.text_type == TextType.CODE:
        return LeafNode(tag="code", value=TextNode.text)
    elif TextNode.text_type == TextType.ANCHOR:
        if not TextNode.url:
            raise ValueError("ANCHOR type must have a url")
        return LeafNode(tag="a", value=TextNode.text, props={"href": TextNode.url})
    elif TextNode.text_type == TextType.IMAGE:
        return LeafNode(tag="img", value="", props={"alt": TextNode.text, "src": TextNode.url if TextNode.url else ""})
    else:
        raise ValueError(f"Unsupported text type: {TextNode.text_type}")
