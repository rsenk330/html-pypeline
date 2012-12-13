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
