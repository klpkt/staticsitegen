import unittest

from htmlnode import HTMLNode, LeafNode

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

if __name__ == "__main__":
    unittest.main()