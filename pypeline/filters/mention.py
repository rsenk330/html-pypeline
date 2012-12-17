import re

from lxml.html import fromstring, tostring
from lxml.etree import SubElement

class Mention(object):
    """Replaces `@mention`'s with a URL pointing to the user's profile.

    The URL can be configured by setting the ``user_url`` key in the `context`.
    By default, it is set to `/users/{username}. ``{username}`` will always
    be replaced by everything after the `@` symbol in the `@mention`.

    Ignored usernames can be configured by setting the ``ignore_username``
    key in the `context`. By default, it ignores `mention` and `mentioning`.
    This should always be an iterable.

    The class applied to `@mention` links defaults to ``mention``. This can
    be changed by setting the ``class`` key in the `context`.

    """
    PARENT_IGNORES = ('pre', 'code', 'a')
    MENTION_RE = r'\B@(?P<username>\w+)'

    def __init__(self, context={}):
        """Creates a new `@mention` filter.

        :param dict context: The filters context

        """
        self.context = {
            'user_url': '/users/{username}',
            'ignore_username': ['mention', 'mentioning'],
            'class': 'mention'
        }

        self.context.update(context)

    def __call__(self, content):
        """Runs the filter and replaces all `@mention`'s with links"""
        fragment = fromstring(content)

        for index, el in enumerate(fragment):
            text = el.text

            if '@' not in text: continue
            if self._should_ignore(el): continue

            fragment[index] = self._add_mention_links(el)

        return tostring(fragment)

    def _should_ignore(self, element):
        """Checks to see if an `@mention` should be ignored.

        This will check all parent elements to see if it is contained in
        any of the `PARENT_IGNORES`.

        :param lxml.html.HtmlElement element: The HTML element containing
                                              the `@mention`.
        :returns: True if this `@mention` should be ignored, otherwise False

        """
        if element is None: return False
        if element.tag in self.PARENT_IGNORES: return True

        return self._should_ignore(element.getparent())

    def _mentioned_logins(self, element):
        """Generator that yields a list of all `@mentions`."""
        text = element.text

        mentions = set(re.findall(self.MENTION_RE, text))

        for mention in mentions:
            if mention not in self.context['ignore_username']:
                yield "@{0}".format(mention)

    def _add_mention_links(self, element):
        """Replaces `@mentions` with links

        :returns: A new element with `@mentions` replaced with anchors.

        """
        text = tostring(element)
        for mention in self._mentioned_logins(element):
            url = self.context['user_url'].format(username=mention[1:])

            anchor = SubElement(element, "a")
            anchor.attrib['href'] = url
            anchor.attrib['class'] = self.context['class']
            anchor.text = mention

            text = re.sub(r'{0}\b'.format(mention), tostring(anchor), text)

        return fromstring(text)
