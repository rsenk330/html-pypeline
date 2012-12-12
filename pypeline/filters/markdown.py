import misaka as m

def markdown(context={}):
    """Renders HTML from Makrdown text.

    :warning: This filter is different that other filters, and must
              be called at the beginning of the pipeline. It takes text
              and renders HTML instead of modifying HTML.

    :returns: The filter function pointer to render the HTML

    """
    def render(content):
        return m.html(content)

    return render
