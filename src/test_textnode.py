import unittest

from textnode import TextNode, TextType, text_node_to_html_node, split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_images, split_nodes_links, text_to_textnodes

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

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images_not_link(self):
        matches = extract_markdown_images(
            "This text links [to Wikipedia](\"https://en.wikipedia.org\")"
        )
        self.assertListEqual([], matches)

    def test_extract_multiple_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        )
        self.assertListEqual([("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This text links [to Wikipedia](https://en.wikipedia.org)"
        )
        self.assertListEqual([("to Wikipedia", "https://en.wikipedia.org")], matches)

    def test_extract_multiple_markdown_links(self):
        matches = extract_markdown_links(
            "This text links to [Wikipedia](https://en.wikipedia.org) and to [YouTube](https://www.youtube.com)"
        )
        self.assertListEqual([("Wikipedia", "https://en.wikipedia.org"), ("YouTube", "https://www.youtube.com")], matches)

    def test_extract_markdown_links_not_images(self):
        matches = extract_markdown_links(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([], matches)
    
    def test_split_nodes_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_images([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )
    
    def test_split_nodes_links(self):
        node = TextNode(
            "This text links to [Wikipedia](https://en.wikipedia.org) and to [YouTube](https://www.youtube.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_links([node])
        self.assertListEqual(
            [
                TextNode("This text links to ", TextType.TEXT),
                TextNode("Wikipedia", TextType.LINK, "https://en.wikipedia.org"),
                TextNode(" and to ", TextType.TEXT),
                TextNode("YouTube", TextType.LINK, "https://www.youtube.com"),
            ],
            new_nodes,
        )

    def test_text_to_textnodes(self):
        nodes = text_to_textnodes("This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)")
        self.assertEqual(nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ])

if __name__ == "__main__":
    unittest.main()