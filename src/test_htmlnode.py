import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode(tag="div", value="Hello", children=[], props={"class": "greeting"})
        node2 = HTMLNode(tag="div", value="Hello", children=[], props={"class": "greeting"})
        self.assertEqual(node, node2)
    
    def test_neq(self):
        node = HTMLNode(tag="div", value="Hello", children=[], props={"class": "greeting"})
        node2 = HTMLNode(tag="div", value="Hello", children=[], props={"class": "farewell"})
        self.assertNotEqual(node, node2)
    
    def test_children_eq(self):
        child1 = HTMLNode(tag="span", value="Child", children=[], props={})
        child2 = HTMLNode(tag="span", value="Child", children=[], props={})
        node = HTMLNode(tag="div", value=None, children=[child1], props={})
        node2 = HTMLNode(tag="div", value=None, children=[child2], props={})
        self.assertEqual(node, node2)

    def test_props_to_html(self):
        node = HTMLNode(tag="a", value="Link", children=[], props={"href": "https://example.com", "target": "_blank"})
        self.assertEqual(node.props_to_html(), ' href="https://example.com" target="_blank"')

    def test_to_html_not_implemented(self):
        node = HTMLNode(tag="div", value="Hello", children=[], props={})
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_repr(self):
        node = HTMLNode(tag="div", value="Hello", children=[], props={"class": "greeting"})
        expected_repr = "HTMLNode(tag=div, value=Hello, children=[], props={'class': 'greeting'})"
        self.assertEqual(repr(node), expected_repr)

    def test_defaults(self):
        node = HTMLNode()
        self.assertEqual(node.tag, None)
        self.assertEqual(node.value, None)
        self.assertEqual(node.children, [])
        self.assertEqual(node.props, {})
    
    def test_empty_string_value(self):
        node = HTMLNode(value="")
        self.assertEqual(node.value, "")
    
    def test_neq_different_tag(self):
        node = HTMLNode(tag="div", value="Hello")
        node2 = HTMLNode(tag="p", value="Hello")
        self.assertNotEqual(node, node2)

    def test_neq_different_type(self):
        node = HTMLNode(tag="div", value="Hello")
        self.assertNotEqual(node, "not a node")

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_b(self):
        node = LeafNode("b", "Hello, world!")
        self.assertEqual(node.to_html(), "<b>Hello, world!</b>")

    def test_leaf_to_html_div(self):
        node = LeafNode("div", "Hello, world!")
        self.assertEqual(node.to_html(), "<div>Hello, world!</div>")

    def test_parent_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_parent_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_parent_to_html_with_props(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node], {"class": "container"})
        self.assertEqual(
            parent_node.to_html(),
            '<div class="container"><span>child</span></div>',
        )
    
    def test_parent_to_html_no_children(self):
        with self.assertRaises(ValueError):
            parent_node = ParentNode("div", [])
            parent_node.to_html()

    def test_parent_to_html_no_tag(self):
        child_node = LeafNode("span", "child")
        with self.assertRaises(ValueError):
            parent_node = ParentNode(None, [child_node])
            parent_node.to_html()

    def test_parent_to_html_no_children_and_no_tag(self):
        with self.assertRaises(ValueError):
            parent_node = ParentNode(None, [])
            parent_node.to_html()

if __name__ == "__main__":
    unittest.main()