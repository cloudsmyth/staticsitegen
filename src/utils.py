import re
from textnode import TextNode, TextType


def split_by_delimiter(old, delimit, text_type):
    new = []
    for o in old:
        if o.text_type != TextType.TEXT:
            new.append(o)
            continue
        sections = []
        splt = o.text.split(delimit)
        if len(splt) % 2 == 0:
            raise Exception("not valid markdown")
        for i in range(len(splt)):
            if splt[i] == "":
                continue
            if i % 2 == 0:
                sections.append(TextNode(splt[i], TextType.TEXT))
            else:
                sections.append(TextNode(splt[i], text_type))
        new.extend(sections)
    return new


def split_by_link(old):
    results = []
    pattern = r'\[(.*?)\]\((.*?)\)'

    for o in old:
        if o.text_type != TextType.TEXT:
            results.append(o)
            continue
        node = match_node_transformer(o.text, pattern, TextType.LINK)
        results.extend(node)

    return results


def split_by_image(old):
    results = []
    pattern = r'!\[(.*?)\]\((.*?)\)'

    for o in old:
        if o.text_type != TextType.TEXT:
            results.append(o)
            continue
        node = match_node_transformer(o.text, pattern, TextType.IMAGE)
        results.extend(node)

    return results


def match_node_transformer(text, pattern, text_type):
    results = []
    last_end = 0

    for match in re.finditer(pattern, text):
        # Text before the image
        if match.start() > last_end:
            results.append(
                TextNode(text[last_end:match.start()], TextType.TEXT))

        # The image
        results.append(TextNode(match.group(1), text_type, match.group(2)))
        last_end = match.end()

    # Text after the last image
    if last_end < len(text):
        results.append(
            TextNode(text[last_end:], TextType.TEXT))

    return results


def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches


def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches
