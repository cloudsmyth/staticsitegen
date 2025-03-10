import unittest

from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import LeafNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_text_to_html_node(self):
        # Test regular text conversion
        text_node = TextNode("Hello, world!", TextType.TEXT)
        html_node = text_node_to_html_node(text_node)
        expected_node = LeafNode(None, "Hello, world!")
        self.assertEqual(html_node, expected_node)
        self.assertEqual(html_node.to_html(), "Hello, world!")

    def test_bold_to_html_node(self):
        # Test bold text conversion
        text_node = TextNode("Bold text", TextType.BOLD)
        html_node = text_node_to_html_node(text_node)
        expected_node = LeafNode("b", "Bold text")
        self.assertEqual(html_node, expected_node)
        self.assertEqual(html_node.to_html(), "<b>Bold text</b>")

    def test_italic_to_html_node(self):
        # Test italic text conversion
        text_node = TextNode("Italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(text_node)
        expected_node = LeafNode("i", "Italic text")
        self.assertEqual(html_node, expected_node)
        self.assertEqual(html_node.to_html(), "<i>Italic text</i>")

    def test_code_to_html_node(self):
        # Test code text conversion
        text_node = TextNode("def hello():", TextType.CODE)
        html_node = text_node_to_html_node(text_node)
        expected_node = LeafNode("code", "def hello():")
        self.assertEqual(html_node, expected_node)
        self.assertEqual(html_node.to_html(), "<code>def hello():</code>")

    def test_link_to_html_node(self):
        # Test link conversion
        text_node = TextNode("Click here", TextType.LINK,
                             "https://example.com")
        html_node = text_node_to_html_node(text_node)
        expected_node = LeafNode(
            "a", "Click here", {"href": "https://example.com"})
        self.assertEqual(html_node, expected_node)
        self.assertEqual(html_node.to_html(),
                         '<a href="https://example.com">Click here</a>')

    def test_image_to_html_node(self):
        # Test image conversion
        text_node = TextNode("Image description", TextType.IMAGE, "image.jpg")
        html_node = text_node_to_html_node(text_node)
        expected_node = LeafNode(
            "img", "", {"src": "image.jpg", "alt": "Image description"})
        self.assertEqual(html_node, expected_node)
        self.assertEqual(html_node.to_html(),
                         '<img src="image.jpg" alt="Image description" />')

    def test_unknown_type(self):
        # Test error handling for unknown type
        text_node = TextNode("Test", "whattheheck")
        with self.assertRaises(Exception):
            text_node_to_html_node(text_node)


if __name__ == "__main__":
    unittest.main()
