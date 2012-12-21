from lxml.etree import Element
from lxml.html import fromstring, tostring

class ImageMaxWidth(object):
    def __call__(self, content):
        element = fromstring(content)

        for el in element.findall("..//img"):
            # Skip if there is already a defined style
            if element.attrib.get('style', None): continue

            # Try to avoid js injection from `javascript:` urls
            if element.attrib.get('src', '').strip().startswith("javascript"): continue

            el.attrib['style'] = "max-width:100%;"

            if not self._is_link(el):
                anchor = self._link_image(el)

                el.getparent().replace(el, anchor)

        return tostring(element)

    def _is_link(self, element):
        if element is None: return False
        if element.tag == 'a': return True

        return self._is_link(element.getparent())

    def _link_image(self, element):
        anchor = Element("a")
        anchor.attrib['href'] = element.attrib.get('src', '')
        anchor.attrib['target'] = '_blank'

        anchor.append(element)

        return anchor
