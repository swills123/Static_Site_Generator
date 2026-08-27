import unittest
from textnode import TextNode, TextType
from inline_markdown import split_nodes_delimiter

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_code_block(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
        )

    def test_bold(self):
        node = TextNode("This is text with a **bolded phrase** in the middle", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded phrase", TextType.BOLD),
                TextNode(" in the middle", TextType.TEXT),
            ],
        )

    def test_italic(self):
        node = TextNode("This is an _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
        )

    def test_multiple_delimited_sections(self):
        node = TextNode("**bold1** and **bold2**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("bold1", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("bold2", TextType.BOLD),
            ],
        )

    def test_delimiter_at_start(self):
        node = TextNode("`code` at the start", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("code", TextType.CODE),
                TextNode(" at the start", TextType.TEXT),
            ],
        )

    def test_delimiter_at_end(self):
        node = TextNode("ends with `code`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("ends with ", TextType.TEXT),
                TextNode("code", TextType.CODE),
            ],
        )

    def test_non_text_node_passthrough(self):
        node = TextNode("already bold", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [TextNode("already bold", TextType.BOLD)])

    def test_unmatched_delimiter_raises(self):
        node = TextNode("This has an `unclosed code block", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "`", TextType.CODE)

    def test_multiple_old_nodes(self):
        node1 = TextNode("has `code` here", TextType.TEXT)
        node2 = TextNode("already italic", TextType.ITALIC)
        new_nodes = split_nodes_delimiter([node1, node2], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("has ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(" here", TextType.TEXT),
                TextNode("already italic", TextType.ITALIC),
            ],
        )

    def test_no_delimiter_present(self):
        node = TextNode("plain text, nothing special", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [TextNode("plain text, nothing special", TextType.TEXT)])


if __name__ == "__main__":
    unittest.main()