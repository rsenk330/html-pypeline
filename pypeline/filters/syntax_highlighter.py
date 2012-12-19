from lxml.html import fromstring, tostring
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name
from pygments.util import ClassNotFound

class SyntaxHighlighter(object):
    """Highlights syntax with pygments.

    To highlight HTML, wrap the code in a ``<code lang="..."></code>`` tag.
    The `lang` attribute specifies the language the code block is written in.

    In Markdown, you can using fenced code blocks. The markdown filter will
    automatically replace that with the correct HTML code.

    Example markdown:

        ```python
        print("Here is sample python code")
        ```

    """

    def __init__(self, context={}):
        self.context = context
        self.formatter = HtmlFormatter(linenos=False, cssclass="source")

    def __call__(self, content):
        fragment = fromstring(content)

        for el in fragment.findall("..//code"):
            lang = el.attrib.get('lang', None)
            if lang is None: continue

            highlighted = self._highlight(lang, tostring(el))

            el.clear()
            el.append(fromstring(highlighted))

        return tostring(fragment)

    def _highlight(self, language, code):
        try:
            lexar = get_lexer_by_name(language, strip_all=True)
        except ClassNotFound:
            # Fallback to the plain-text lexar
            lexar = get_lexer_by_name('text', strip_all=True)

        return highlight(code, lexar, self.formatter)
