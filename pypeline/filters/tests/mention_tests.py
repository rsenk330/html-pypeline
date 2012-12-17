import pypeline

from lxml.doctestcompare import LXMLOutputChecker
from lxml.html import fromstring, tostring

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
        self.assertTrue(self._string_eql(expected, filtered), "{0} != {1}".format(expected, filtered))

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
        self.assertTrue(self._string_eql(expected, filtered), "{0} != {1}".format(expected, filtered))

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
        self.assertTrue(self._string_eql(expected, filtered), "{0} != {1}".format(expected, filtered))

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
        self.assertTrue(self._string_eql(expected, filtered), "{0} != {1}".format(expected, filtered))

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
        self.assertTrue(self._string_eql(expected, filtered), "{0} != {1}".format(expected, filtered))

    def test_should_ignore(self):
        """Tests to see if `@mention`'s that should be ignored are"""
        filter = pypeline.filters.mention()

        pre_frag = '<pre>@mentionee to a @user and @mention</pre>'
        code_frag = '<code>@mentionee to a @user and @mention</code>'
        a_frag = '<a href="#">@mention</a>'
        nested_frag = '<pre><code><div><p>@user mention</p></div></code></pre>'
        p_frag = '<p>@user mention is here</p>'

        pre_el = fromstring(pre_frag)
        code_el = fromstring(code_frag)
        a_el = fromstring(a_frag)
        nested_el = fromstring(nested_frag)
        p_el = fromstring(p_frag)

        self.assertTrue(filter._should_ignore(pre_el))
        self.assertTrue(filter._should_ignore(code_el))
        self.assertTrue(filter._should_ignore(a_el))
        self.assertTrue(filter._should_ignore(nested_el))

        self.assertFalse(filter._should_ignore(p_el))

    def test_mentioned_logins(self):
        """Tests to make sure all mentioned logins are found"""
        filter = pypeline.filters.mention()

        p_frag = '<p>@user mention is @mention here @user duplicate @user2 another @user3</p>'
        p_elem = fromstring(p_frag)

        mentions = sorted(list(filter._mentioned_logins(p_elem)))

        self.assertListEqual(mentions, ['@user', '@user2', '@user3'])

    def test_add_mention_links(self):
        """Tests to see if all `@mention`'s are replaced with links"""
        filter = pypeline.filters.mention()

        p_frag = '<p>@user mention is @mention here @user duplicate @user2 another @user3</p>'
        p_elem = fromstring(p_frag)

        expected = '<p><a href="/users/user" class="mention">@user</a> mention is @mention here <a href="/users/user" class="mention">@user</a> duplicate <a href="/users/user2" class="mention">@user2</a> another <a href="/users/user3" class="mention">@user3</a></p>'

        filtered = tostring(filter._add_mention_links(p_elem))

        self.assertTrue(self._string_eql(expected, filtered), "{0} != {1}".format(expected, filtered))
