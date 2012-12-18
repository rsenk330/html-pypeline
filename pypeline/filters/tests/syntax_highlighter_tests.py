from pypeline.utils import unittest

from pypeline.filters import syntax_highlighter

class SyntaxHighlighterTests(unittest.TestCase):
    def setUp(self):
        self.filter = syntax_highlighter()

    def test_set_context(self):
        self.assertEqual(self.filter.context, {})
