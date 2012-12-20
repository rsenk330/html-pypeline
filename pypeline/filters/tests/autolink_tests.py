from lxml.html import fromstring

from pypeline.filters import autolink
from pypeline.utils import unittest

class AutoLinkTests(unittest.TestCase):
    def setUp(self):
        self.filter = autolink()

    def test_render_http(self):
        """Tests to see if http links are converted to `<a></a>` elements"""
        html = """\
<div>
    <p>http://test.com</p>
</div>
"""
        filtered = fromstring(self.filter(html))

        anchors = filtered.findall("..//a")

        self.assertEqual(len(anchors), 1)
        self.assertEqual(anchors[0].attrib['href'], "http://test.com")
        self.assertEqual(anchors[0].text, "http://test.com")

    def test_render_https(self):
        """Tests to see if http links are converted to `<a></a>` elements"""
        html = """\
<div>
    <p>https://test.com</p>
</div>
"""
        filtered = fromstring(self.filter(html))

        anchors = filtered.findall("..//a")

        self.assertEqual(len(anchors), 1)
        self.assertEqual(anchors[0].attrib['href'], "https://test.com")
        self.assertEqual(anchors[0].text, "https://test.com")

    def test_render_mailto(self):
        """Tests to see if mailto links are converted to `<a></a>` elements"""
        html = """\
<div>
    <p>mailto:test@test.com</p>
</div>
"""
        filtered = fromstring(self.filter(html))

        anchors = filtered.findall("..//a")

        self.assertEqual(len(anchors), 1)
        self.assertEqual(anchors[0].attrib['href'], "mailto:test@test.com")
        self.assertEqual(anchors[0].text, "test@test.com")

    def test_render_multiple(self):
        """Tests to see if all links are converted to `<a></a>` elements"""
        html = """\
<div>
    <p>https://test.com</p>
    <p>http://test.com</p>
    <p>mailto:test@test.com</p>
</div>
"""
        filtered = fromstring(self.filter(html))

        anchors = filtered.findall("..//a")

        self.assertEqual(len(anchors), 3)
        self.assertEqual(anchors[0].attrib['href'], "https://test.com")
        self.assertEqual(anchors[0].text, "https://test.com")
        self.assertEqual(anchors[1].attrib['href'], "http://test.com")
        self.assertEqual(anchors[1].text, "http://test.com")
        self.assertEqual(anchors[2].attrib['href'], "mailto:test@test.com")
        self.assertEqual(anchors[2].text, "test@test.com")
