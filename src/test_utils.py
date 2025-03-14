import unittest
from textnode import TextType, TextNode
from utils import (split_by_full, split_by_delimiter,
                   split_by_image, split_by_link, extract_title)


class TestSplit(unittest.TestCase):
    def test_full_split(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE,
                     "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        new_list = split_by_full(text)
        self.assertListEqual(new_list, expected)

    def test_bold_markdown(self):
        """Test splitting text with bold markdown delimiters (**) correctly"""
        # Input text with bold formatting
        input_text = [TextNode("This is **bold** text", TextType.TEXT),
                      TextNode("Another **bold word** here", TextType.TEXT)]

        # Expected output after processing
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
            TextNode("Another ", TextType.TEXT),
            TextNode("bold word", TextType.BOLD),
            TextNode(" here", TextType.TEXT)
        ]

        # Call the function with bold delimiter
        result = split_by_delimiter(input_text, "**", TextType.BOLD)

        # Verify the result matches expected output
        self.assertEqual(len(result), len(expected))
        for i in range(len(result)):
            self.assertEqual(result[i].text, expected[i].text)
            self.assertEqual(result[i].text_type, expected[i].text_type)

    def test_italic_markdown(self):
        """Test splitting text with italic markdown delimiters (*) correctly"""
        # Input text with italic formatting
        input_text = [TextNode("This is *italic* text", TextType.TEXT),
                      TextNode("Multiple *italic* *words* here", TextType.TEXT)]

        # Expected output after processing
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT),
            TextNode("Multiple ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" ", TextType.TEXT),
            TextNode("words", TextType.ITALIC),
            TextNode(" here", TextType.TEXT)
        ]

        # Call the function with italic delimiter
        result = split_by_delimiter(input_text, "*", TextType.ITALIC)

        # Verify the result matches expected output
        self.assertEqual(len(result), len(expected))
        for i in range(len(result)):
            self.assertEqual(result[i].text, expected[i].text)
            self.assertEqual(result[i].text_type, expected[i].text_type)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_by_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE,
                         "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE,
                    "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_link(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_by_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK,
                         "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "to youtube", TextType.LINK,
                    "https://www.youtube.com/@bootdotdev"
                ),
            ],
            new_nodes,
        )

    def test_extract_header(self):
        md = "# Hello   "
        expected = "Hello"
        self.assertEqual(extract_title(md), expected)

    def test_no_header_raises_exception(self):
        # Markdown text with no header
        md_without_header = """
        This is some markdown text.
        It has multiple lines.
        But none of them start with #
        So it should raise an exception.
        """
        with self.assertRaises(Exception) as context:
            extract_title(md_without_header)
        # Optionally, verify the exception message
        self.assertEqual(str(context.exception),
                         "No header found to use as title!")
