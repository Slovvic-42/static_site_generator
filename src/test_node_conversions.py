from node_functions import text_node_to_html_node, markdown_to_blocks
from textnode import TextNode, TextType
from htmlnode import LeafNode
import unittest 

class TestNodeConversion(unittest.TestCase):
    def test_text_to_html(self):
        text_node = TextNode("Hello, world!", TextType.TEXT)
        html_node = text_node_to_html_node(text_node)
        expected_html_node = LeafNode(tag=None, value="Hello, world!")
        self.assertEqual(html_node, expected_html_node)

    def test_bold_to_html(self):
        text_node = TextNode("Bold text", TextType.BOLD)
        html_node = text_node_to_html_node(text_node)
        expected_html_node = LeafNode(tag="b", value="Bold text")
        self.assertEqual(html_node, expected_html_node)

    def test_anchor_to_html(self):
        text_node = TextNode("Click here", TextType.LINK, url="https://example.com")
        html_node = text_node_to_html_node(text_node)
        expected_html_node = LeafNode(tag="a", value="Click here", props={"href": "https://example.com"})
        self.assertEqual(html_node, expected_html_node)

    def test_image_to_html(self):
        text_node = TextNode("An image", TextType.IMAGE, url="https://example.com/image.png")
        html_node = text_node_to_html_node(text_node)
        expected_html_node = LeafNode(tag="img", value="", props={"alt": "An image", "src": "https://example.com/image.png"})
        self.assertEqual(html_node, expected_html_node)

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_single_block(self):
        md = """
Hi Friends, 
This is al one block
it should return as a single item list
       """ 
        blocks = markdown_to_blocks(md)
        self.assertEqual(len(blocks), 1)

    
    def test_unnecessary_blocks(self):
        md = """
Hi Friends, 



This is al one block



it should return as a single item list
       """ 
        blocks = markdown_to_blocks(md)
        self.assertEqual(len(blocks), 3)
        self.assertEqual(len(blocks), 3)



if __name__ == "__main__":
    unittest.main()