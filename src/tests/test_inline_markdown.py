import unittest
from inline_markdown import extract_markdown_images, extract_markdown_links, split_nodes_image
from textnode import TextNode, TextType


class TestExtractMarkdown(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images_multiple(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        matches = extract_markdown_images(text)
        self.assertListEqual(
            [
                ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
            ],
            matches,
        )

    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        matches = extract_markdown_links(text)
        self.assertListEqual(
            [
                ("to boot dev", "https://www.boot.dev"),
                ("to youtube", "https://www.youtube.com/@bootdotdev"),
            ],
            matches,
        )

    def test_extract_no_images(self):
        matches = extract_markdown_images("This text has no images at all.")
        self.assertListEqual([], matches)

    def test_extract_no_links(self):
        matches = extract_markdown_links("This text has no links at all.")
        self.assertListEqual([], matches)

    def test_links_does_not_match_images(self):
        text = "Here's an image: ![alt text](https://example.com/img.png)"
        matches = extract_markdown_links(text)
        self.assertListEqual([], matches)

    def test_images_does_not_match_links(self):
        text = "Here's a link: [click here](https://example.com)"
        matches = extract_markdown_images(text)
        self.assertListEqual([], matches)

    def test_mixed_images_and_links(self):
        text = "An image ![alt](https://img.com/a.png) and a [link](https://example.com)"
        image_matches = extract_markdown_images(text)
        link_matches = extract_markdown_links(text)
        self.assertListEqual([("alt", "https://img.com/a.png")], image_matches)
        self.assertListEqual([("link", "https://example.com")], link_matches)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )
if __name__ == "__main__":
    unittest.main()