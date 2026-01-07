from htmlnode import HTMLNode, markdown_to_blocks, block_to_block_type, ParentNode, BlockType
from textnode import TextNode, text_to_textnodes, TextType, text_node_to_html_node

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    html_nodes = []
    for text_node in text_nodes:
        html_nodes.append(text_node_to_html_node(text_node))
    return html_nodes


def block_to_html_node(block):
    block_type = block_to_block_type(block)
    tag = block_type.value
    if tag == "h":
        tag += str(len(block.split(' ')[0]))
    node = ParentNode(tag, [])

    match block_type:
        case BlockType.PARAGRAPH:
            content = block.replace('\n', ' ')
            node.children = text_to_children(content)
        case BlockType.HEADING:
            content = ' '.join(block.split(' ')[1:])
            node.children = text_to_children(content)
        case BlockType.CODE:
            content = block[4:-3]
            node.children = [text_node_to_html_node(TextNode(content, TextType.CODE))]
        case BlockType.QUOTE:
            content = block.split('\n')
            for line in content:
                node.children.append(text_to_children(line[2:]))
        case BlockType.UL:
            content = block.split('\n')
            for line in content:
                line_node = ParentNode('li', [])
                line_node.children = text_to_children(line[2:])
                node.children.append(line_node)
        case BlockType.OL:
            content = block.split('\n')
            for line in content:
                line_node = ParentNode('li', [])
                line_content = ' '.join(line.split(' ')[1:])
                line_node.children = text_to_children(line_content)
                node.children.append(line_node)
    return node


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    main_div = ParentNode('div', [])
    for block in blocks:
        block_node = block_to_html_node(block)
        main_div.children.append(block_node)
    return main_div