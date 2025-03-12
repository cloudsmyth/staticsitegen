import unittest

from blockmarkdown import markdown_to_blocks, BlockType, block_to_blocktype


class TestBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_various_block_types(self):
        # Test heading block
        self.assertEqual(block_to_blocktype("# Heading 1"), BlockType.HEADING)
        self.assertEqual(block_to_blocktype("## Heading 2"), BlockType.HEADING)
        self.assertEqual(block_to_blocktype(
            "### Heading 3"), BlockType.HEADING)

        # Test code block
        code_block = "```\ndef hello():\n    print('Hello, world!')\n```"
        self.assertEqual(block_to_blocktype(code_block), BlockType.CODE)

        # Test quote block
        quote_block = "> This is a quote\n> Another line of the quote"
        self.assertEqual(block_to_blocktype(quote_block), BlockType.QUOTE)

        # Test unordered list
        unordered_list = "- Item 1\n- Item 2\n- Item 3"
        self.assertEqual(block_to_blocktype(
            unordered_list), BlockType.UNORDERED)

        # Test ordered list
        ordered_list = "1. First item\n2. Second item\n3. Third item"
        self.assertEqual(block_to_blocktype(ordered_list), BlockType.ORDERED)

        # Test paragraph
        paragraph = "This is a regular paragraph with no special formatting."
        self.assertEqual(block_to_blocktype(paragraph), BlockType.PARAGRAPH)

    def test_edge_cases(self):
        # Test invalid heading (no space after #)
        self.assertEqual(block_to_blocktype("#NoSpace"), BlockType.PARAGRAPH)

        # Test incomplete code block (missing closing ```)
        self.assertEqual(block_to_blocktype(
            "```\ncode without closing"), BlockType.PARAGRAPH)

        # Test mixed list (should default to paragraph)
        mixed_list = "1. First item\n- Second item\n3. Third item"
        self.assertEqual(block_to_blocktype(mixed_list), BlockType.PARAGRAPH)

        # Test empty string
        self.assertEqual(block_to_blocktype(""), BlockType.PARAGRAPH)

        # Test heading with too many # characters
        self.assertEqual(block_to_blocktype(
            "####### Too many hashtags"), BlockType.PARAGRAPH)


if __name__ == "__main__":
    unittest.main()
