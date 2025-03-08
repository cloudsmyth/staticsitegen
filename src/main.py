from textnode import TextNode, TextType


def main():
    node = TextNode("got some bold text",
                    TextType.BOLD,
                    "https://www.boot.dev")
    print(repr(node))


main()
