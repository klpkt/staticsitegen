from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "p"
    HEADING = "h"
    CODE = "pre"
    QUOTE = "blockquote"
    UL = "ul"
    OL = "OL"

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if self.props is None or len(self.props) == 0:
            return ""
        html = " "
        for prop in self.props:
            html += f'{prop}="{self.props[prop]}"'
        return html
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
    
    def to_html(self):
        if self.value is None:
            raise ValueError("All leaf nodes must have a value")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.children is None or len(self.children) == 0:
            raise ValueError("All parent nodes must have children")
        if self.tag is None:
            raise ValueError("All parent nodes must have a tag")
        html_list = [f"<{self.tag}{self.props_to_html()}>"]
        for child in self.children:
            html_list.append(child.to_html())
        html_list.append(f"</{self.tag}>")
        return ''.join(html_list)

def markdown_to_blocks(markdown):
    blocks = map(lambda x: x.strip(), markdown.split('\n\n'))
    return list(filter(lambda x: len(x)>0, blocks))

def is_heading(block):
    if '\n' in block:
        return False
    if block[0] != '#':
        return False
    for i in range(1, 7):
        if block[i] == ' ':
            return True
        if block[i] != '#':
            return False
    return False

def is_code(block):
    return block[:4] == "```\n" and block[-3:] == "```"

def is_quote(block):
    for line in block.split('\n'):
        if not line.startswith("> "):
            return False
    return True

def is_ul(block):
    for line in block.split('\n'):
        if not line.startswith("- "):
            return False
    return True

def is_ol(block):
    for i, line in enumerate(block.split('\n')):
        if not line.startswith(f"{i+1}. "):
            return False
    return True

def block_to_block_type(block):
    if is_heading(block):
        return BlockType.HEADING
    if is_code(block):
        return BlockType.CODE
    if is_quote(block):
        return BlockType.QUOTE
    if is_ul(block):
        return BlockType.UL
    if is_ol(block):
        return BlockType.OL
    return BlockType.PARAGRAPH