class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("to_html method not implemented")

    def props_to_html(self):
        if self.props is None:
            return ""
        str = ''
        for prop in self.props:
            str += f' {prop}="{self.props[prop]}"'
        return str

    def __eq__(self, other):
        if not isinstance(other, HTMLNode):
            return False
        return (self.tag == other.tag and
                self.value == other.value and
                self.children == other.children and
                self.props == other.props)

    def __repr__(self):
        return (f"{self.__class__.__name__}(" +
                f"{self.tag}, {self.value}, {self.children}, {self.props})")


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("value cannot be None")
        if self.tag is None:
            return self.value
        if self.tag == "img":
            return f"<{self.tag}{self.props_to_html()} />"
        return (f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>")


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError("tag cannot be None")
        if not self.children:
            raise ValueError("must have children")
        result_string = f"<{self.tag}{self.props_to_html()}>"
        for child in self.children:
            result_string += child.to_html()
        result_string += f"</{self.tag}>"
        return result_string

    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"
