import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("p", "Lorem Ipsum")
        node2 = HTMLNode("p", "Lorem Ipsum")
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = HTMLNode("a",
                        "Go to website",
                        children=None,
                        props={"href": "boot.dev"})
        node2 = HTMLNode("p", "Lorem Ipsum")
        self.assertNotEqual(node, node2)

    def test_repr(self):
        # Test the __repr__ method
        node = HTMLNode("p", "Lorem Ipsum", None, None)
        expected_repr = "HTMLNode(p, Lorem Ipsum, None, None)"
        self.assertEqual(repr(node), expected_repr)
        # Test with props
        node_with_props = HTMLNode("a",
                                   "Click me",
                                   None,
                                   {"href": "https://example.com"})
        expected_repr = ("HTMLNode(a, Click me, " +
                         "None, {'href': 'https://example.com'})")
        self.assertEqual(repr(node_with_props), expected_repr)

    def test_leaf_to_html(self):
        node = LeafNode("p", "Hello World")
        self.assertEqual(node.to_html(), "<p>Hello World</p>")

    def test_parent_node_with_leaf_children(self):
        """Test that a ParentNode correctly renders HTML with LeafNode children."""
        child1 = LeafNode("p", "Hello", {"class": "greeting"})
        child2 = LeafNode("p", "World", {"id": "world-id"})

        parent = ParentNode("div", [child1, child2], {"class": "container"})

        expected = '<div class="container"><p class="greeting">Hello</p><p id="world-id">World</p></div>'
        self.assertEqual(parent.to_html(), expected)

    def test_parent_node_with_multiple_props(self):
        """Test that a ParentNode correctly renders multiple HTML properties."""
        child = LeafNode("span", "Content")
        parent = ParentNode(
            "div", [child], {"class": "container", "id": "main", "data-test": "value"})

        expected = '<div class="container" id="main" data-test="value"><span>Content</span></div>'
        self.assertEqual(parent.to_html(), expected)

    def test_parent_node_validation(self):
        """Test that ParentNode properly validates its required attributes."""
        # Test missing tag
        with self.assertRaises(ValueError) as context:
            node = ParentNode(None, ["child"])
            node.to_html()
        self.assertTrue("tag cannot be None" in str(context.exception))

        # Test missing children
        with self.assertRaises(ValueError) as context:
            node = ParentNode("div", None)
            node.to_html()
        self.assertTrue("must have children" in str(context.exception))

        # Test empty children list
        with self.assertRaises(ValueError) as context:
            node = ParentNode("div", [])
            node.to_html()
        self.assertTrue("must have children" in str(context.exception))


if __name__ == "__main__":
    unittest.main()
