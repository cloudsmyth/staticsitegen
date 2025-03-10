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
