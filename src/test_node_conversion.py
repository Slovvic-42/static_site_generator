from node_conversion import text_node_to_html_node
from textnode import TextNode, TextType
from htmlnode import LeafNode
import unittest 

class TestNodeConversion(unittest.TestCase):
    def test_plain_to_html(self):
        text_node = TextNode("Hello, world!", TextType.PLAIN)
        html_node = text_node_to_html_node(text_node)
        expected_html_node = LeafNode(tag=None, value="Hello, world!")
        self.assertEqual(html_node, expected_html_node)

    def test_bold_to_html(self):
        text_node = TextNode("Bold text", TextType.BOLD)
        html_node = text_node_to_html_node(text_node)
        expected_html_node = LeafNode(tag="b", value="Bold text")
        self.assertEqual(html_node, expected_html_node)

    def test_anchor_to_html(self):
        text_node = TextNode("Click here", TextType.ANCHOR, url="https://example.com")
        html_node = text_node_to_html_node(text_node)
        expected_html_node = LeafNode(tag="a", value="Click here", props={"href": "https://example.com"})
        self.assertEqual(html_node, expected_html_node)

    def test_image_to_html(self):
        text_node = TextNode("An image", TextType.IMAGE, url="https://example.com/image.png")
        html_node = text_node_to_html_node(text_node)
        expected_html_node = LeafNode(tag="img", value="", props={"alt": "An image", "src": "https://example.com/image.png"})
        self.assertEqual(html_node, expected_html_node)

if __name__ == "__main__":
    unittest.main()