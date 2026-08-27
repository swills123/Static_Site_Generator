import unittest

from markdown_blocks import (
    markdown_to_blocks,
    block_to_block_type,
    BlockType,
    markdown_to_html_node,
    extract_title
)


class TestMarkdownToBlocks(unittest.TestCase):
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

    def test_markdown_to_blocks_single_block(self):
        md = "Just one paragraph here."
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Just one paragraph here."])

    def test_markdown_to_blocks_excessive_newlines(self):
        md = """
This is a paragraph



This is another paragraph after extra blank lines
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is a paragraph",
                "This is another paragraph after extra blank lines",
            ],
        )

    def test_markdown_to_blocks_leading_trailing_whitespace(self):
        md = """

   This paragraph has leading/trailing whitespace   

Another paragraph

"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This paragraph has leading/trailing whitespace",
                "Another paragraph",
            ],
        )

    def test_markdown_to_blocks_heading(self):
        md = """# This is a heading

This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

- This is the first list item in a list block
- This is a list item
- This is another list item
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.",
                "- This is the first list item in a list block\n- This is a list item\n- This is another list item",
            ],
        )

    def test_markdown_to_blocks_empty_string(self):
        blocks = markdown_to_blocks("")
        self.assertEqual(blocks, [])


class TestBlockToBlockType(unittest.TestCase):
    def test_heading(self):
        self.assertEqual(block_to_block_type("# Heading 1"), BlockType.HEADER)

    def test_heading_multiple_hashes(self):
        self.assertEqual(block_to_block_type("### Heading 3"), BlockType.HEADER)

    def test_code_block(self):
        block = "```\nsome code\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_quote_block(self):
        self.assertEqual(block_to_block_type("> This is a quote"), BlockType.QUOTE)

    def test_unordered_list(self):
        block = "- item one\n- item two"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDER_LIST)

    def test_ordered_list(self):
        block = "1. first\n2. second"
        self.assertEqual(block_to_block_type(block), BlockType.ORDER_LIST)

    def test_paragraph(self):
        block = "Just a normal paragraph of text."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_paragraph_with_inline_markdown(self):
        block = "This has **bold** and _italic_ text."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)


class TestMarkdownToHtmlNode(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_heading(self):
        md = "## This is a heading"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><h2>This is a heading</h2></div>")

    def test_quote(self):
        md = "> This is a quote\n> spanning two lines"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html, "<div><blockquote>This is a quote spanning two lines</blockquote></div>"
        )

    def test_unordered_list(self):
        md = "- item one\n- item two"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html, "<div><ul><li>item one</li><li>item two</li></ul></div>"
        )

    def test_ordered_list(self):
        md = "1. first\n2. second"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html, "<div><ol><li>first</li><li>second</li></ol></div>"
        )

    def test_multiple_block_types(self):
        md = """# Heading

A paragraph with **bold** text.

- list item one
- list item two
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading</h1><p>A paragraph with <b>bold</b> text.</p><ul><li>list item one</li><li>list item two</li></ul></div>",
        )
        
class TestExtractTitle(unittest.TestCase):
    def test_basic_title(self):
        self.assertEqual(extract_title("# Hello"), "Hello")

    def test_title_with_extra_whitespace(self):
        self.assertEqual(extract_title("#   Hello World   "), "Hello World")

    def test_title_not_on_first_line(self):
        md = "Some intro text\n\n# The Real Title\n\nMore content"
        self.assertEqual(extract_title(md), "The Real Title")

    def test_no_h1_raises(self):
        md = "## Just an h2\n\nSome text"
        with self.assertRaises(ValueError):
            extract_title(md)

    def test_no_heading_at_all_raises(self):
        md = "Just a plain paragraph, no headings."
        with self.assertRaises(ValueError):
            extract_title(md)

    def test_multiple_h1s_returns_first(self):
        md = "# First Title\n\nSome content\n\n# Second Title"
        self.assertEqual(extract_title(md), "First Title")


if __name__ == "__main__":
    unittest.main()