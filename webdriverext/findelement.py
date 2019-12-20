from .error import _FindElementBase, FindElementError


_default_sentinel = object()


class FindElementMixin(object):

    """Mixin to add default functionality to the various find_element methods."""

    def find_element(self, type_, spec, default=_default_sentinel):

        try:
            return super().find_element(type_, spec)
        except _FindElementBase:
            pass

        if default is not _default_sentinel:
            return default

        raise FindElementError(spec)

    find_element_by_name = lambda self, *args: self.find_element('name', *args)
    find_element_by_id = lambda self, *args: self.find_element('id', *args)
    find_element_by_xpath = lambda self, *args: self.find_element('xpath', *args)
    find_element_by_link_text = lambda self, *args: self.find_element('link text', *args)
    find_element_by_partial_link_text = lambda self, *args: self.find_element('partial link text', *args)
    find_element_by_tag_name = lambda self, *args: self.find_element('tag name', *args)
    find_element_by_class_name = lambda self, *args: self.find_element('class name', *args)
    find_element_by_css_selector = lambda self, *args: self.find_element('css selector', *args)

