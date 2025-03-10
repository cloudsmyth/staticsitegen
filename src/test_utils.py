import unittest
from textnode import TextType, TextNode
from utils import split_by_delimiter, split_by_image, split_by_link


class TestSplitByDelimiter(unittest.TestCase):
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
