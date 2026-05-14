from node_functions import split_nodes_delimiter
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

if __name__ == "__main__":
    unittest.main()