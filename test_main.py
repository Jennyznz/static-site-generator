import unittest
from main import extract_title

class TestMain(unittest.TestCase):
    def test_extract_title(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

# This is the title

- This is a list
- with items
            """
        title = extract_title(md)
        self.assertEqual("This is the title", title)

    def test_extract_title_two(self):
        md = """
# This is the title
            """
        title = extract_title(md)
        self.assertEqual("This is the title", title)