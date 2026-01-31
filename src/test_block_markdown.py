import unittest
from block_markdown import markdown_to_blocks, block_to_block_type, markdown_to_html_node
from blocktype import BlockType

class TestBlockMarkdown(unittest.TestCase):
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
    def test_block_to_block_type_list(self):
          md = "- This is a list"
          type = block_to_block_type(md)
          self.assertEqual(type, BlockType.UNORDERED_LIST)

    def test_block_to_block_type_code(self):
          md = "```\nCode here\n```"
          type = block_to_block_type(md)
          self.assertEqual(type, BlockType.CODE)
    
    def test_block_to_block_type_ordered_list(self):
          md = """1. One\n2. Two\n3. Three"""
          type = block_to_block_type(md)
          self.assertEqual(type, BlockType.ORDERED_LIST)
    
    def test_block_to_block_types(self):
        block = "# heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
        block = "```\ncode\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
        block = "> quote\n> more quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
        block = "- list\n- items"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)
        block = "1. list\n2. items"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)
        block = "paragraph"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
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
        md = """

# This is a heading 1

## This is a heading 2

### This is a heading 3

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>This is a heading 1</h1><h2>This is a heading 2</h2><h3>This is a heading 3</h3></div>",
        )
    
    def test_quote(self):
        md = """

> This is a single-line quote

> This is line one of a multi-line quote.
> This is line two of a multi-line quote.

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a single-line quote</blockquote><blockquote>This is line one of a multi-line quote. This is line two of a multi-line quote.</blockquote></div>",
        )
    
    def test_ul(self):
        md = """
- Item 1
- Item 2
- Item 3
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>Item 1</li><li>Item 2</li><li>Item 3</li></ul></div>",
        )

    def test_ol(self):
        md = """
1. First
2. Second
3. Third
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>First</li><li>Second</li><li>Third</li></ol></div>",
        )
    
