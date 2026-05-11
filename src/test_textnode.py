import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_neq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_url_eq(self):
        node = TextNode("Click here", TextType.ANCHOR, url="https://example.com")
        node2 = TextNode("Click here", TextType.ANCHOR, url="https://example.com")
        self.assertEqual(node, node2)

    def test_url_neq(self):
        node = TextNode("Click here", TextType.ANCHOR, url="https://example.com")
        node2 = TextNode("Click here", TextType.ANCHOR, url="https://example.org")
        self.assertNotEqual(node, node2)

    def test_none_url_eq(self):
        node = TextNode("Click here", TextType.ANCHOR, url="https://example.com")
        node2 = TextNode("Click here", TextType.ANCHOR)
        self.assertNotEqual(node, node2)

if __name__ == "__main__":
    unittest.main()