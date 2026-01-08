import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode, markdown_to_blocks, BlockType, block_to_block_type

class TestHTMLNode(unittest.TestCase):
    def test_init(self):
        node = HTMLNode('p', "Hello, world!")
        self.assertEqual(node.tag, 'p')
        self.assertEqual(node.value, "Hello, world!")
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

        node2 = HTMLNode('a', "Wikipedia", None, {"href": "en.wikipedia.org"})
        self.assertEqual(node2.props["href"], "en.wikipedia.org")

    def test_repr(self):
        node = HTMLNode('p', "Hello, world!")
        self.assertEqual(repr(node), "HTMLNode(p, Hello, world!, None, None)")

        node2 = HTMLNode('a', "Wikipedia", None, {"href": "en.wikipedia.org"})
        self.assertEqual(repr(node2), "HTMLNode(a, Wikipedia, None, {'href': 'en.wikipedia.org'})")
    
    def test_props(self):
        node = HTMLNode('p', "Hello, world!")
        self.assertEqual(node.props_to_html(), "")
        
        node2 = HTMLNode('a', "Wikipedia", None, {"href": "en.wikipedia.org"})
        self.assertEqual(node2.props_to_html(), " href=\"en.wikipedia.org\"")

    def test_leaf_to_html_p(self):
        node = LeafNode('p', "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    
    def test_leaf_to_html_a(self):
        node = LeafNode('a', "Wikipedia", {"href": "en.wikipedia.org"})
        self.assertEqual(node.to_html(), '<a href="en.wikipedia.org">Wikipedia</a>')

    def test_leaf_repr(self):
        node = LeafNode('p', "Hello, world!")
        self.assertEqual(repr(node), "LeafNode(p, Hello, world!, None)")

    def test_parent_to_html(self):
        node = ParentNode(
            'p',
            [
                LeafNode('b', "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode('i', "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        )

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_no_children(self): #by the mountain goats
        node = ParentNode("div", [])
        with self.assertRaises(ValueError):
            node.to_html()
    
    def test_to_html_none_children(self):
        node = ParentNode("div", None)
        with self.assertRaises(ValueError):
            node.to_html()

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
    
    def test_markdown_to_blocks_whitespace(self):
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
    
    def test_block_to_blocktype_h1(self):
        self.assertEqual(
            block_to_block_type("# h1"),
            BlockType.HEADING
        )
    
    def test_block_to_blocktype_h2(self):
        self.assertEqual(
            block_to_block_type("## h2"),
            BlockType.HEADING
        )
    
    def test_block_to_blocktype_h6(self):
        self.assertEqual(
            block_to_block_type("###### h6"),
            BlockType.HEADING
        )
    
    def test_block_to_blocktype_no_h7(self):
        self.assertEqual(
            block_to_block_type("####### h7"),
            BlockType.PARAGRAPH
        )
    
    def test_block_to_blocktype_code(self):
        self.assertEqual(
            block_to_block_type("""```
this is some code
yeah
```"""),
            BlockType.CODE
        )
    
    def test_block_to_blocktype_no_code(self):
        self.assertEqual(
            block_to_block_type("""``
this is a fake code tag
````"""),
            BlockType.PARAGRAPH
        )
    
    def test_block_to_blocktype_quote(self):
        self.assertEqual(
            block_to_block_type("> I have a dream"),
            BlockType.QUOTE
        )
    
    def test_block_to_blocktype_big_quote(self):
        self.assertEqual(
            block_to_block_type("""> I have
> a dream"""),
            BlockType.QUOTE
        )
    
    def test_block_to_blocktype_no_quote(self):
        self.assertEqual(
            block_to_block_type(">> I have a nightmare"),
            BlockType.PARAGRAPH
        )
    
    def test_block_to_blocktype_no_quote_big(self):
        self.assertEqual(
            block_to_block_type("""> I have
>a nightmare"""),
            BlockType.PARAGRAPH
        )
    
    def test_block_to_blocktype_ul(self):
        self.assertEqual(
            block_to_block_type("""- item
- item
- item"""),
            BlockType.UL
        )
    
    def test_block_to_blocktype_no_ul(self):
        self.assertEqual(
            block_to_block_type("""- item
-item
- item"""),
            BlockType.PARAGRAPH
        )
    
    def test_block_to_blocktype_ol(self):
        self.assertEqual(
            block_to_block_type("""1. one
2. two
3. three"""),
            BlockType.OL
        )
    
    def test_block_to_blocktype_no_ol(self):
        self.assertEqual(
            block_to_block_type("""1. one
two
3. three"""),
            BlockType.PARAGRAPH
        )
    
    def test_block_to_blocktype_failed_ol(self):
        self.assertEqual(
            block_to_block_type("""1. one
3. three
2. two"""),
            BlockType.PARAGRAPH
        )

if __name__ == "__main__":
    unittest.main()