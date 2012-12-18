from lxml.html import fromstring, tostring
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name

class SyntaxHighlighter(object):
    def __init__(self, context={}):
        self.context = context

    def __call__(self, content):
        fragment = fromstring(content)

        for el in fragment.findall(".//code"):
            if el.attrib.get('lang', None) is None: continue

            el.getparent().replace(el, self._highlight(tostring(el)))

        return tostring(fragment)

    def _highlight(self, language, code):
        lexar = get_lexer_by_name(language, strip_all=True)
        formatter = HtmlFormatter(linenos=True, cssclass="source")

        return highlight(code, lexar, formatter)
