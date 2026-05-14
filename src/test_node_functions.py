from node_functions import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link
from textnode import TextNode, TextType
import unittest

class TestNodeFunctions(unittest.TestCase):
    
    def test_split_nodes_delimiter(self):
        # Test basic splitting
        nodes = [TextNode(text="Hello **world**!", text_type=TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "Hello ")
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[1].text, "world")
        self.assertEqual(result[1].text_type, TextType.BOLD)
        self.assertEqual(result[2].text, "!")
        self.assertEqual(result[2].text_type, TextType.TEXT)

    def test_unmatched_delimiter(self):
        # Test unmatched delimiter
        nodes = [TextNode(text="Hello *world!", text_type=TextType.TEXT)]
        with self.assertRaises(ValueError):
            split_nodes_delimiter(nodes, "*", TextType.BOLD)
    
    def test_no_delimiter(self):
        # Test no delimiter
        nodes = [TextNode(text="Hello world!", text_type=TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, "Hello world!")
        self.assertEqual(result[0].text_type, TextType.TEXT)

    def test_multiple_delimiters(self):
        # Test multiple delimiters
        nodes = [TextNode(text="**Hello** **world**!", text_type=TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertEqual(len(result), 4)
        self.assertEqual(result[0].text, "Hello")
        self.assertEqual(result[0].text_type, TextType.BOLD)
        self.assertEqual(result[1].text, " ")
        self.assertEqual(result[1].text_type, TextType.TEXT)
        self.assertEqual(result[2].text, "world")
        self.assertEqual(result[2].text_type, TextType.BOLD)
        self.assertEqual(result[3].text, "!")
        self.assertEqual(result[3].text_type, TextType.TEXT)
    
    def test_mixed_delimiters(self):
        # Test mixed delimiters
        nodes = [TextNode(text="**Hello** _world_!", text_type=TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        result = split_nodes_delimiter(result, "_", TextType.ITALIC)
        self.assertEqual(len(result), 4)
        self.assertEqual(result[0].text, "Hello")
        self.assertEqual(result[0].text_type, TextType.BOLD)
        self.assertEqual(result[1].text, " ")
        self.assertEqual(result[1].text_type, TextType.TEXT)
        self.assertEqual(result[2].text, "world")
        self.assertEqual(result[2].text_type, TextType.ITALIC)
        self.assertEqual(result[3].text, "!")
        self.assertEqual(result[3].text_type, TextType.TEXT)

    def test_bold_input_node(self):
        # Test input node is already bold
        nodes = [TextNode(text="**Hello**", text_type=TextType.BOLD)]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, "**Hello**")
        self.assertEqual(result[0].text_type, TextType.BOLD)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        )
        self.assertListEqual([("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")], matches)

    def test_no_closing_parenthesis(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png"
        )
        self.assertListEqual([], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)

    def test_no_closing_parenthesis_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://www.example.com"
        )
        self.assertListEqual([], matches)

    def test_no_alt_text_images(self):
        matches = extract_markdown_links(
            "This is text with a [](https://www.example.com)"
        )
        self.assertListEqual([("", "https://www.example.com")], matches)

    def test_no_anchor_text_links(self):
        matches = extract_markdown_links(
            "This is text with a [](https://www.example.com)"
        )
        self.assertListEqual([("", "https://www.example.com")], matches)

    def test_no_url_links(self):
        matches = extract_markdown_links(
            "This is text with a [link]()"
        )
        self.assertListEqual([("link", "")], matches)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    
    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://www.example.com) and another [second link](https://www.example2.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.example.com"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://www.example2.com"
                ),
            ],
            new_nodes,
        )
    
    def test_split_links_no_anchor_text(self):
        node = TextNode(
            "This is text with a [](https://www.example.com) and another [](https://www.example2.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("", TextType.LINK, "https://www.example.com"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "", TextType.LINK, "https://www.example2.com"
                ),
            ],
            new_nodes,
        )
    
    def test_split_links_no_url(self):
        node = TextNode(
            "This is text with a [link]() and another [second link]()",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, ""),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, ""
                ),
            ],
            new_nodes,
        )
    
    def test_split_images_no_alt_text(self):
        node = TextNode(
            "This is text with an ![](https://i.imgur.com/zjjcJKZ.png) and another ![](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    
    def test_split_images_plain_text(self):
        node = TextNode(
            "This is text with no images",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with no images", TextType.TEXT)
            ],
            new_nodes,
        )
    
    def test_split_links_plain_text(self):
        node = TextNode(
            "This is text with no links",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with no links", TextType.TEXT)
            ],
            new_nodes,
        )

if __name__ == "__main__":
    unittest.main()