from lxml.html import fromstring
from pypeline.filters import image_max_width
from pypeline.utils import unittest

class ImageMaxWidthTests(unittest.TestCase):
    def setUp(self):
        self.renderer = image_max_width()

    def test_call(self):
        pass

    def test_is_link_with_link(self):
        """Tests is_link with a parent link present"""
        html = """\
<div>
    <a href="#">
        <img src="http://test.com"></img>
    </a>
</div>"""

        filtered = fromstring(self.renderer(html))
        links = filtered.findall("..//a")

        self.assertTrue(len(links), 1)
        self.fail("not yet finished")

    def test_is_link_without_link(self):
        """Tests is_link without a parent link present"""
        pass

    def test_link_image(self):
        pass
