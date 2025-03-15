import re
from blockmarkdown import (
    block_to_blocktype, markdown_to_blocks, BlockType, heading_level)
from htmlnode import HTMLNode, ParentNode
from textnode import text_node_to_html_node, TextNode, TextType
from utils import split_by_full


def markdown_to_html_node(md):
    blocks = markdown_to_blocks(md)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children, None)


def block_to_html_node(block):
    typ = block_to_blocktype(block)
    if typ == BlockType.HEADING:
        return markdown_heading(block)
    elif typ == BlockType.PARAGRAPH:
        return markdown_paragraph(block)
    elif typ == BlockType.QUOTE:
        return markdown_quote(block)
    elif typ == BlockType.UNORDERED:
        return markdown_unordered(block)
    elif typ == BlockType.ORDERED:
        return markdown_ordered(block)
    elif typ == BlockType.CODE:
        return markdown_code(block)


def markdown_paragraph(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_node(paragraph)
    return ParentNode("p", children)


def markdown_heading(block):
    level = heading_level(block)
    heading_text = block[level + 1:]
    children = text_to_node(heading_text)
    return ParentNode(f"h{level}", children)


def markdown_quote(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_node(content)
    return ParentNode("blockquote", children)


def markdown_unordered(block):
    lines = block.split("\n")
    li_nodes = [ParentNode("li", text_to_node(line[2:]))
                for line in lines
                if line.startswith("- ")]
    return ParentNode("ul", li_nodes)


def markdown_ordered(block):
    lines = block.split("\n")
    li_nodes = []
    for line in lines:
        # Extract number and content using regex
        match = re.match(r"^\d+\.\s(.*)", line)
        if match:
            # This gets the text after the number.
            item_text = match.group(1)
            li_nodes.append(
                ParentNode("li", text_to_node(item_text)))
    return ParentNode("ol", li_nodes)


def markdown_code(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")
    text = block[4:-3]
    code_text_node = TextNode(text, TextType.TEXT)
    child = text_node_to_html_node(code_text_node)
    code = ParentNode("code", [child])
    return ParentNode("pre", [code])


def text_to_node(block):
    text_nodes = split_by_full(block)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children
