import unittest

import pypeline

class TestPipeline(unittest.TestCase):
    def setUp(self):
        pass

    def test_pipeline_render(self):
        """Tests the pipeline render function"""
        filters = [
            pypeline.filters.markdown()
        ]
        markdown = "# Test\n*Testing this*"

        pipeline = pypeline.Pipeline(filters)
        html = pipeline.render(markdown)

        self.assertIsNotNone(html)
        self.assertNotEqual(html, markdown)
