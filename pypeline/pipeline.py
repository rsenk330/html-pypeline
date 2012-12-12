class Pipeline(object):
    def __init__(self, filters, **kwargs):
        """Initialize a new pipeline

        Any arguments that should be passed to specific filters
        should be passed as a kwarg.

        :param list filters: A list of filters. All filters should inherit

        Example:

            import pypeline
            renderer = pypeline.Renderer([
                MarkdownFilter,
                ...,
                MentionFilter
            ])

            renderer.render(content)

        """
        self.filters = filters
        self.context = kwargs

    def render(self, content):
        """Passes the `content` through the pipeline and renders it.

        :param str content: The content to pass down the pipeline
        :returns: The rendered HTML

        """
        rendered = content
        for filter in self.filters:
            rendered = filter(rendered)

        return rendered
