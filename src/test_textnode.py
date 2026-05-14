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
        node = TextNode("Click here", TextType.LINK, url="https://example.com")
        node2 = TextNode("Click here", TextType.LINK, url="https://example.com")
        self.assertEqual(node, node2)

    def test_url_neq(self):
        node = TextNode("Click here", TextType.LINK, url="https://example.com")
        node2 = TextNode("Click here", TextType.LINK, url="https://example.org")
        self.assertNotEqual(node, node2)

    def test_none_url_eq(self):
        node = TextNode("Click here", TextType.LINK, url="https://example.com")
        node2 = TextNode("Click here", TextType.LINK)
        self.assertNotEqual(node, node2)

    def test_image_repr(self):
        node = TextNode("An image", TextType.IMAGE)
        expected_repr = "TextNode(An image, image, None)"
        self.assertEqual(repr(node), expected_repr)

if __name__ == "__main__":
    unittest.main()