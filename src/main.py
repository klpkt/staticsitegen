from textnode import TextType, TextNode

node = TextNode("helo", TextType.BOLD)
print(node)
link = TextNode("boots", TextType.LINK, "boot.dev")
print(link)