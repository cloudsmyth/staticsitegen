import unittest

from htmlnode import HTMLNode


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
        expected_repr = "HTMLNode(a, Click me, None, {'href': 'https://example.com'})"
        self.assertEqual(repr(node_with_props), expected_repr)


if __name__ == "__main__":
    unittest.main()
