import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        p = {
            "href": "https://www.google.com",
            "target": "_blank",
        }
        node = HTMLNode(props=p)
        func_result = node.props_to_html()
        to_match = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(func_result, to_match)
    
    def test_values(self):
        node = HTMLNode("p", "Hello")
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "Hello")
    
    def test_repr(self):
        child_node = HTMLNode(value="hey")
        node = HTMLNode("h1", "Nothing here?", [child_node])
        self.assertEqual(node.__repr__(), f"HTMLNode(tag='h1', value='Nothing here?', children=[{child_node}], props='')")

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    
    def test_leaf_to_html_h1(self):
        node = LeafNode("h1", "Title One")
        self.assertEqual(node.to_html(), "<h1>Title One</h1>")

    def test_leaf_to_html_div(self):
        node = LeafNode("div", "Everything")
        self.assertEqual(node.to_html(), "<div>Everything</div>")

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child = LeafNode("div", "A child")
        parent = ParentNode("div", children=[child])
        self.assertEqual(parent.to_html(), "<div><div>A child</div></div>")

    def test_to_html_with_grandchildren(self):
        grandchildren = LeafNode("div", "A grandchild")
        child = ParentNode("div", children=[grandchildren])
        parent = ParentNode("div", children=[child])
        self.assertEqual(parent.to_html(), "<div><div><div>A grandchild</div></div></div>")
