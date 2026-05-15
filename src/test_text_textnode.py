from node_functions import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes
from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
import unittest

class TestTextToHtmlNodes(unittest.TestCase):
    def test_text_to_textnodes(self):
        text = "This is **bold** text, this is _italic_ text, this is `code` text, this is an image ![alt text](image_url), and this is a link [link text](link_url)"
        self.assertListEqual(
            text_to_textnodes(text),
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" text, this is ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" text, this is ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(" text, this is an image ", TextType.TEXT),
                TextNode("alt text", TextType.IMAGE, "image_url"),
                TextNode(", and this is a link ", TextType.TEXT),
                TextNode("link text", TextType.LINK, "link_url"),
            ],
        )
    
    def test_text_to_textnodes_plain(self):
        nodes = text_to_textnodes("Just plain text")
        self.assertListEqual(
            [TextNode("Just plain text", TextType.TEXT)],
            nodes,
        )
    
    def test_text_to_textnodes_bold_only(self):
        nodes = text_to_textnodes("**bold**")
        self.assertListEqual(
            [TextNode("bold", TextType.BOLD)],
            nodes,
        )

    def test_text_to_textnodes_bold_and_italic(self):
        nodes = text_to_textnodes("**bold** and _italic_")
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            nodes,
        )

if __name__ == "__main__":
    unittest.main()
