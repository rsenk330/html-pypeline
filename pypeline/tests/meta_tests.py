import unittest

import pypeline

class MetaTests(unittest.TestCase):
    def test_version(self):
        """Test for accurate version number"""
        self.assertEqual(pypeline.__version__, '0.1')

    def test_title(self):
        """Test to see if the title is present"""
        self.assertEqual(pypeline.__title__, 'html-pypeline')
