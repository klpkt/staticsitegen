import unittest

from textnode import TextNode, TextType, text_node_to_html_node, split_nodes_delimiter

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node1 = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node1, node2)
        
        node3 = TextNode("This is a link", TextType.LINK, "en.wikipedia.org")
        self.assertNotEqual(node1, node3)
        node4 = TextNode("This is a link", TextType.LINK, "google.com")
        self.assertNotEqual(node3, node4)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    
    def test_bold(self):
        node = TextNode("this is bolded", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'b')
    
    def test_link(self):
        node = TextNode("this is a link", TextType.LINK, "en.wikipedia.org")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'a')
        self.assertEqual(html_node.props['href'], "en.wikipedia.org")

    def test_split_bold(self):
        node = TextNode("This is some **bolded** text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [
            TextNode("This is some ", TextType.TEXT),
            TextNode("bolded", TextType.BOLD),
            TextNode(" text", TextType.TEXT)
        ])
    
    def test_split_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT)
        ])
    
    def test_split_bold_and_italic(self):
        node = TextNode("This is some **bolded** and some _italic_ text", TextType.TEXT)
        mid_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(mid_nodes, "_", TextType.ITALIC)
        self.assertEqual(new_nodes, [
            TextNode("This is some ", TextType.TEXT),
            TextNode("bolded", TextType.BOLD),
            TextNode(" and some ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT)
        ])

    def test_already_special_text(self):
        node = TextNode("This text is already bolded", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [
            TextNode("This text is already bolded", TextType.BOLD)
        ])
    
    def test_split_bolded_italic(self):
        node = TextNode("This is some **bolded _and italic_ text**, eventually", TextType.TEXT)
        mid_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(mid_nodes, "_", TextType.ITALIC)
        self.assertEqual(new_nodes, [
            TextNode("This is some ", TextType.TEXT),
            TextNode("bolded _and italic_ text", TextType.BOLD),
            #TextNode("bolded ", TextType.BOLD),
            #TextNode("and italic", (TextType.BOLD, TextType.ITALIC)),
            #TextNode(" text", TextType.BOLD),
            TextNode(", eventually", TextType.TEXT)
        ])
    
    def test_unbalanced(self):
        node = TextNode("This text is **invalid markdown", TextType.TEXT)
        with self.assertRaises(Exception):
            new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)

    def test_no_change(self):
        node = TextNode("This text has no special syntax", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [node])

if __name__ == "__main__":
    unittest.main()