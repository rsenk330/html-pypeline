from lxml.etree import Element
from lxml.html import tostring

def plaintext():
    """Escapes plaintext and wraps in a div

    :warning: This filter is different that other filters, and must
              be called at the beginning of the pipeline. It takes text
              and renders HTML instead of modifying HTML.

    :returns: The filter function pointer to render to HTML

    """
    def render(content):
        wrapper = Element("div")
        wrapper.text = content

        return tostring(wrapper)

    return render
