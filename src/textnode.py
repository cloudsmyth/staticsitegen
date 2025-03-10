from enum import Enum
from htmlnode import LeafNode


class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


def text_node_to_html_node(node):
    if node.text_type.value == TextType.TEXT.value:
        return LeafNode(None, node.text)
    elif node.text_type.value == TextType.BOLD.value:
        return LeafNode("b", node.text)
    elif node.text_type.value == TextType.ITALIC.value:
        return LeafNode("i", node.text)
    elif node.text_type.value == TextType.CODE.value:
        return LeafNode("code", node.text)
    elif node.text_type.value == TextType.LINK.value:
        return LeafNode("a", node.text, {"href": node.url})
    elif node.text_type.value == TextType.IMAGE.value:
        return LeafNode("img", "", {"src": node.url, "alt": node.text})
    else:
        raise Exception("Unknown text type")


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, o):
        if not isinstance(o, TextNode):
            return False
        return (self.text == o.text and
                self.text_type == o.text_type and
                self.url == o.url)

    def __repr__(self):
        return (f"{self.__class__.__name__}" +
                f"({self.text}, {self.text_type.value}, {self.url})")
