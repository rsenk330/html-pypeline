from xml.sax import saxutils

import pypeline

from pypeline.utils import unittest

class PlaintextTests(unittest.TestCase):
    def setUp(self):
        self.filter = pypeline.filters.plaintext()

    def test_render(self):
        """Tests to make sure the wrapping <div>...</div> is inserted"""
        input = "Testing the plaintext filter"
        filtered = self.filter(input)

        self.assertEqual(filtered, "<div>{0}</div>".format(input))

    def test_render_html(self):
        """Tests to make sure the HTML input is escaped"""
        input = "<p>testing the plaintext filter</p>"
        filtered = self.filter(input)

        self.assertEqual(filtered, "<div>{0}</div>".format(saxutils.escape(input)))
