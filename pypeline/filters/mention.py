import re

from lxml.html import fromstring, tostring
from lxml.etree import SubElement

class Mention(object):
    PARENT_IGNORES = ('pre', 'code', 'a')
    MENTION_RE = r'\B@(?P<username>\w+)'

    def __init__(self, context={}):
        self.context = context

    def __call__(self, content):
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

        mentions = re.findall(self.MENTION_RE, text)

        for mention in mentions:
            yield "@{0}".format(mention)

    def _add_mention_links(self, element):
        """Replaces `@mentions` with links

        :returns: A new element with `@mentions` replaced with anchors.

        """
        text = tostring(element)
        for mention in self._mentioned_logins(element):
            anchor = SubElement(element, "a")
            anchor.attrib['href'] = '#'
            anchor.attrib['class'] = 'mention'
            anchor.text = mention

            text = text.replace(mention, tostring(anchor))

        return fromstring(text)
