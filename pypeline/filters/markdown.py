from xml.sax import saxutils

import misaka as m

class SyntaxRenderer(m.HtmlRenderer):
    def block_code(self, text, lang):
        if lang:
            return '\n<pre lang="{0}">{1}</pre>\n'.format(lang, saxutils.escape(text.strip()))
        else:
            return '\n<pre>{0}</pre>\n'.format(saxutils.escape(text.strip()))

def markdown(context={}):
    """Renders HTML from Makrdown text.

    :warning: This filter is different that other filters, and must
              be called at the beginning of the pipeline. It takes text
              and renders HTML instead of modifying HTML.

    :returns: The filter function pointer to render the HTML

    """
    md = m.Markdown(SyntaxRenderer(), extensions=m.EXT_FENCED_CODE | m.EXT_STRIKETHROUGH | m.EXT_NO_INTRA_EMPHASIS)

    def render(content):
        return md.render(content)

    return render
