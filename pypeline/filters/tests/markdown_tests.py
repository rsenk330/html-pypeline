import pypeline

from pypeline.utils import unittest

class MarkdownTests(unittest.TestCase):
    def setUp(self):
        filters = [
            pypeline.filters.markdown()
        ]

        self.renderer = pypeline.Pipeline(filters)

    def test_markdown_render(self):
        """Tests to make sure markdown is rendered with the markdown filter"""
        markdown = """\
# Test Header

This is test markdown. It **should** render in *HTML*.
"""
        html = self.renderer.render(markdown)

        self.assertEqual(html, "<h1>Test Header</h1>\n\n<p>This is test markdown. It <strong>should</strong> render in <em>HTML</em>.</p>\n")

class SyntaxRendererTests(unittest.TestCase):
    def setUp(self):
        self.renderer = pypeline.filters.SyntaxRenderer()

    def test_block_code_lang_set(self):
        """Test to make sure that the proper code block is rendered (with lang)"""
        expected = '\n<pre lang="python">code sample</pre>\n'
        self.assertEqual(self.renderer.block_code("code sample", "python"), expected)

    def test_block_code_lang_not_set(self):
        """Test to make sure that the proper code block is rendered (without lang)"""
        expected = '\n<pre>code sample</pre>\n'
        self.assertEqual(self.renderer.block_code("code sample", None), expected)
