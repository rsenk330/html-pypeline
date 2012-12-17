import pypeline

from lxml.doctestcompare import LXMLOutputChecker

from pypeline.utils import unittest

class MentionTests(unittest.TestCase):
    def setUp(self):
        filters = [
            pypeline.filters.mention()
        ]

        self.renderer = pypeline.Pipeline(filters)

    def _string_eql(self, expected, filtered):
        return LXMLOutputChecker().check_output(expected, filtered, 0)

    def test_mention_replace(self):
        """Tests to see if @mentions are replaces with URLs"""
        html_fragment = """\
<div>
    <h1>Testing</h1>
    <p>Blah</p>
    <p>@mention to a @user</p>
</div>"""
        expected = """\
<div>
    <h1>Testing</h1>
    <p>Blah</p>
    <p><a href="#" class="mention">@mention</a> to a <a href="#" class="mention">@user</a></p>
</div>"""

        filtered = self.renderer.render(html_fragment)

        self.assertNotEqual(filtered, html_fragment)
        self.assertTrue(self._string_eql(expected, filtered), "{0} != {1}".format(filtered, expected))
