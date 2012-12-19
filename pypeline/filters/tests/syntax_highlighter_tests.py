from lxml.html import fromstring

from pypeline.filters import syntax_highlighter
from pypeline.utils import unittest

class SyntaxHighlighterTests(unittest.TestCase):
    def setUp(self):
        self.filter = syntax_highlighter()

    def test_set_context(self):
        """Tests to make sure the default context is set"""
        self.assertEqual(self.filter.context, {})

    def test_highlight_valid_lang(self):
        """Tests to make sure syntax is highlighted with a valid lang"""
        html = """\
def test():
    for i in range(10):
        print(i)
"""

        highlighted = fromstring(self.filter._highlight('python', html))

        self.assertTrue(highlighted.findall("..//pre"))
        self.assertTrue(highlighted.findall("..//span"))

    def test_highlight_invalid_lang(self):
        """Tests to make sure syntax is highlighted with a invalid lang"""
        html = """\
def test():
    for i in range(10):
        print(i)
"""

        highlighted = fromstring(self.filter._highlight('invalid', html))

        self.assertTrue(highlighted.findall(".//pre"))
        self.assertFalse(highlighted.findall(".//code"))

    def test_render_valid_lang(self):
        """Tests to make sure syntax is rendered with a valid lang"""
        html = """\
<code lang="python">
    def test():
        for i in range(10):
            print(i)
</code>
"""
        highlighted = fromstring(self.filter(html))

        self.assertEqual(len(highlighted.findall("..//div[@class='source']")), 1)
        self.assertTrue(highlighted.findall("..//div"))
        self.assertTrue(highlighted.findall("..//pre"))
        self.assertTrue(highlighted.findall("..//span"))
        self.assertTrue(highlighted.findall("..//code"))

    def test_render_invalid_lang(self):
        """Tests to make sure syntax is rendered with an invalid lang"""
        html = """\
<code lang="invalid">
    def test():
        for i in range(10):
            print(i)
</code>
"""
        highlighted = fromstring(self.filter(html))

        self.assertEqual(len(highlighted.findall("..//div[@class='source']")), 1)
        self.assertTrue(highlighted.findall("..//div"))
        self.assertTrue(highlighted.findall("..//pre"))
        self.assertTrue(highlighted.findall("..//code"))
        self.assertFalse(highlighted.findall("..//span"))

    def test_render_html_escape(self):
        """Make sure tags are escaped"""
        html = """\
<code lang="html">
    <script type="text/html">
        alert("Hello world!");
    </script>
</code>
"""

        highlighted = fromstring(self.filter(html))

        self.assertFalse(highlighted.findall("..//script"))
