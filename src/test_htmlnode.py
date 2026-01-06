import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_init(self):
        node = HTMLNode('p', "Hello world")
        self.assertEqual(node.tag, 'p')
        self.assertEqual(node.value, "Hello world")
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

        node2 = HTMLNode('a', "Wikipedia", None, {"href": "en.wikipedia.org"})
        self.assertEqual(node2.props["href"], "en.wikipedia.org")

    def test_repr(self):
        node = HTMLNode('p', "Hello world")
        self.assertEqual(repr(node), "HTMLNode(p, Hello world, None, None)")

        node2 = HTMLNode('a', "Wikipedia", None, {"href": "en.wikipedia.org"})
        self.assertEqual(repr(node2), "HTMLNode(a, Wikipedia, None, {'href': 'en.wikipedia.org'})")
    
    def test_props(self):
        node = HTMLNode('p', "Hello world")
        self.assertEqual(node.props_to_html(), "")
        
        node2 = HTMLNode('a', "Wikipedia", None, {"href": "en.wikipedia.org"})
        self.assertEqual(node2.props_to_html(), " href=\"en.wikipedia.org\"")

if __name__ == "__main__":
    unittest.main()