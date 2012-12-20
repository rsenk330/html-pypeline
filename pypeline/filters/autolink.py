# from lxml.html import fromstring, tostring
from lxml.html.clean import autolink_html

def autolink(context={}):
    def render(content):
        return autolink_html(content)

    return render
