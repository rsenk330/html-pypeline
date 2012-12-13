import pypeline

from pypeline.utils import unittest

class TestPipeline(unittest.TestCase):
    def setUp(self):
        filters = [
            pypeline.filters.markdown()
        ]

        self.markdown = "# Test\n*Testing this*"
        self.pipeline = pypeline.Pipeline(filters)

    def test_pipeline_render(self):
        """Tests the pipeline render function"""
        html = self.pipeline.render(self.markdown)

        self.assertIsNotNone(html)
        self.assertNotEqual(html, self.markdown)

    def test_pipeline_render_empty(self):
        """Tests the pipeline render function with empty content"""
        markdown = ""
        html = self.pipeline.render(markdown)

        self.assertIsNotNone(html)
        self.assertEqual(html, "")

    def test_pipeline_render_no_filter(self):
        """Tests the pipeline render function with no filters"""
        pipeline = pypeline.Pipeline([])
        html = pipeline.render(self.markdown)

        self.assertIsNotNone(html)
        self.assertEqual(html, self.markdown)
