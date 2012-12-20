# HTML-Pypeline [![Build Status](https://travis-ci.org/rsenk330/html-pypeline.png?branch=master)](https://travis-ci.org/rsenk330/html-pypeline)

HTML Pypeline is a python implementation of the [HTML::Pipeline](https://github.com/jch/html-pipeline) ruby library.

It applies a number of different filters (like a pipeline) to the provided content, rendering, for example, Markdown to HTML with emojis.

## Installation

Until it is on pypi, you need to install it by hand:

    python setup.py install

## Usage

```python
import pypeline

filters = [
    pypeline.filters.markdown(),
    pypeline.filters.mention(),
    ...
]
markdown = """\
# Test

**Testing this**

## @mention

@user testing
"""

pipeline = pypeline.Pipeline(filters)
html = pipeline.render(markdown)
```

## Filters

Most of the filters provided by [HTML::Pipeline](https://github.com/jch/html-pipeline) are also provided here.

Filters that are currently completed:

* **MarkdownFilter***: Markdown -> HTML
* **PlainTextInputFilter***: Escapes HTML tags and wraps in a div
* **AutolinkFilter**: Automatic linking of URLs
* **MentionFilter**: Replace `@mentions` with a URL
* **SyntaxHighlightFilter**: Syntax highlighting

*Only one of these can be used at a time, and they must be the _first_ filter in the pipeline.

Filters that are being worked on:

* **EmojiFilter**: Replace [emoji](http://www.emoji-cheat-sheet.com/) tags with images
* **HttpsFilter**: Replace HTTP URLs with HTTPS
* **ImageMaxWidthFilter**: Link to the full size image when creating image previews
* **TextileFilter**: Textile -> HTML
* **TableOfContentsFilter**: Adds the `name` attribute to headers

## Examples

## Developing

1. Clone the repo
1. Create a virtualenv
1. Run `./script/bootstrap`
1. Run unit tests with `nosetests` (`pip install nose coverage` if you don't have nose installed)

## Contributing

1. [Fork it!](https://help.github.com/articles/fork-a-repo)
1. Create your feature branch (`git checkout -b my-new-feature`)
1. Commit your changes (`git commit -am 'Added some feature'`)
1. Push to the branch (`git push origin my-new-feature`)
1. Create new Pull Request
