import unittest

import pypeline

class MetaTests(unittest.TestCase):
    def test_version(self):
        self.assertEqual(pypeline.__version__, '0.1')

    def test_title(self):
        self.assertEqual(pypeline.__title__, 'html-pypeline')
