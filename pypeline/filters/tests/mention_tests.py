import pypeline

from lxml.doctestcompare import LXMLOutputChecker

from pypeline.utils import unittest

class MentionTests(unittest.TestCase):
    def setUp(self):
        self.renderer = pypeline.Pipeline(self._build_filters())

        self.html_fragment = """\
<div>
    <h1>Testing</h1>
    <p>Blah</p>
    <p>@mentionee to a @user and @mention</p>
</div>"""

    def _build_filters(self, context={}):
        return [
            pypeline.filters.mention(context)
        ]

    def _string_eql(self, expected, filtered):
        return LXMLOutputChecker().check_output(expected, filtered, 0)

    def test_mention_replace(self):
        """Tests to see if @mentions are replaced with URLs"""
        expected = """\
<div>
    <h1>Testing</h1>
    <p>Blah</p>
    <p><a href="/users/mentionee" class="mention">@mentionee</a> to a <a href="/users/user" class="mention">@user</a>  and @mention</p>
</div>"""

        filtered = self.renderer.render(self.html_fragment)

        self.assertNotEqual(filtered, self.html_fragment)
        self.assertTrue(self._string_eql(expected, filtered), "{0} != {1}".format(filtered, expected))

    def test_mention_replace_user_url(self):
        renderer = pypeline.Pipeline(self._build_filters({'user_url': 'http://localhost:5000/users/{username}'}))
        expected = """\
<div>
    <h1>Testing</h1>
    <p>Blah</p>
    <p><a href="http://localhost:5000/users/mentionee" class="mention">@mentionee</a> to a <a href="http://localhost:5000/users/user" class="mention">@user</a>  and @mention</p>
</div>"""

        filtered = renderer.render(self.html_fragment)

        self.assertNotEqual(filtered, self.html_fragment)
        self.assertTrue(self._string_eql(expected, filtered), "{0} != {1}".format(filtered, expected))

    def test_mention_set_class(self):
        renderer = pypeline.Pipeline(self._build_filters({'class': 'user-mention'}))
        expected = """\
<div>
    <h1>Testing</h1>
    <p>Blah</p>
    <p><a href="/users/mentionee" class="user-mention">@mentionee</a> to a <a href="/users/user" class="user-mention">@user</a>  and @mention</p>
</div>"""

        filtered = renderer.render(self.html_fragment)

        self.assertNotEqual(filtered, self.html_fragment)
        self.assertTrue(self._string_eql(expected, filtered), "{0} != {1}".format(filtered, expected))

    def test_mention_ignore_username(self):
        """Tests to see if @mentions are replaced with URLs"""
        renderer = pypeline.Pipeline(self._build_filters({'ignore_username': ['mentionee']}))
        expected = """\
<div>
    <h1>Testing</h1>
    <p>Blah</p>
    <p>@mentionee to a <a href="/users/user" class="mention">@user</a> and <a href="/users/mention" class="mention">@mention</a></p>
</div>"""

        filtered = renderer.render(self.html_fragment)

        self.assertNotEqual(filtered, self.html_fragment)
        self.assertTrue(self._string_eql(expected, filtered), "{0} != {1}".format(filtered, expected))

    def test_mention_duplicates(self):
        """Tests to see if @mentions are replaced with URLs"""
        renderer = pypeline.Pipeline(self._build_filters({'ignore_username': ['mentionee']}))
        html_fragment = """\
<div>
    <h1>Testing</h1>
    <p>Blah</p>
    <p>@mentionee to a @user and @user again and @mention</p>
</div>"""

        expected = """\
<div>
    <h1>Testing</h1>
    <p>Blah</p>
    <p>@mentionee to a <a href="/users/user" class="mention">@user</a> and <a href="/users/user" class="mention">@user</a> again and <a href="/users/mention" class="mention">@mention</a></p>
</div>"""

        filtered = renderer.render(html_fragment)

        self.assertNotEqual(filtered, html_fragment)
        self.assertTrue(self._string_eql(expected, filtered), "{0} != {1}".format(filtered, expected))
