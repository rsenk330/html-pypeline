import unittest

import pypeline

class MarkdownTests(unittest.TestCase):
    def test_markdown_render(self):
        """Tests to make sure markdown is rendered with the markdown filter"""
        markdown = """\
# Test Header

This is test markdown. It **should** render in *HTML*.
"""
        filters = [
            pypeline.filters.markdown()
        ]

        renderer = pypeline.Pipeline(filters)
        html = renderer.render(markdown)

        self.assertEqual(html, "<h1>Test Header</h1>\n\n<p>This is test markdown. It <strong>should</strong> render in <em>HTML</em>.</p>\n")
