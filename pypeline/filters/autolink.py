# from lxml.html import fromstring, tostring
from lxml.html.clean import autolink_html

def autolink(context={}):
    """The autolink filter automatically add links.

    It does this by looking for things that look like links, which includes
    anything starting with `http`, `https`, and `mailto` and replaces it
    with an anchor element.

    """
    def render(content):
        return autolink_html(content)

    return render
