# -*- coding: utf-8 -*-
import re
from urllib.parse import urljoin

from lxml import html, etree
from lxml.html import HtmlElement

from lxmlHtml.link import Link
from lxmlHtml.styles import Styles


class HtmlElementProxy(HtmlElement):
    """
    HtmlElement 代理类 序列化，属性操作，节点操作

    _Element https://lxml.de/api/lxml.etree._Element-class.html
    ElementBase https://lxml.de/api/lxml.etree.ElementBase-class.html
    HtmlMixin https://lxml.de/api/lxml.html.HtmlMixin-class.html
    HtmlElement https://lxml.de/api/lxml.html.HtmlElement-class.html
    """

    def __init__(self, element, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.root = element

    # 序列化，反序列化
    def __str__(self):
        return self.tostring()

    def __repr__(self):
        return self.__str__()

    @classmethod
    def makeelement(cls, _tag, attrib=None, nsmap=None, **_extra):
        return html.Element(_tag, attrib=attrib, nsmap=nsmap, **_extra)

    @staticmethod
    def makecomment(*args, **kwargs):
        return html.HtmlComment(*args, **kwargs)

    @classmethod
    def fragment_fromstring(cls, text, create_parent=False, base_url=None, parser=None, **kw):
        return cls(html.fragment_fromstring(text, create_parent, base_url, parser, **kw))

    @classmethod
    def document_fromstring(cls, text, parser=None, ensure_head_body=False, **kw):
        return cls(html.document_fromstring(text, parser, ensure_head_body, **kw))

    def tostring(self, pretty_print=False, include_meta_content_type=False,
                 encoding="unicode", method="html", with_tail=True, doctype=None):
        return html.tostring(self.root, pretty_print, include_meta_content_type,
                             encoding, method, with_tail, doctype)

    def urljoin(self, href):
        return urljoin(self.root.base_url, href)

    def open_in_browser(self, encoding='utf-8'):
        html.open_in_browser(self.root, encoding)

    # 属性操作
    def get(self, key, default=None):
        return self.root.get(key, default)

    def set(self, key, value):
        self.root.set(key, value)

    def pop(self, key, default=None):
        return self.root.attrib.pop(key, default)

    def has_key(self, key):
        return self.root.attrib.has_key(key)

    def keys(self):
        return self.root.keys()

    def values(self):
        return self.root.values()

    def items(self):
        return self.root.items()

    def clear_attrs(self):
        self.root.attrib.clear()

    # 属性
    @property
    def attrib(self):
        return self.root.attrib

    @property
    def base(self):
        return self.root.base

    @property
    def tag(self):
        return self.root.tag

    @property
    def tail(self):
        return self.root.tail

    @property
    def text(self):
        return self.root.text

    @property
    def base_url(self):
        return self.root.base_url

    @property
    def body(self):
        return self.root.body

    @property
    def classes(self):
        """set"""
        return self.root.classes

    @property
    def styles(self):
        """orderDict"""
        return Styles(self.root.attrib)

    @property
    def forms(self):
        return self.root.forms

    @property
    def head(self):
        return self.root.head

    @property
    def label(self):
        return self.root.label

    def addnext(self, element):
        self.root.addnext(element)

    def addprevious(self, element):
        self.root.addprevious(element)

    def getnext(self):
        return self.root.getnext()

    def getprevious(self):
        return self.root.getPrevious()

    def clear(self, keep_tail=False):
        self.root.clear(keep_tail)

    def append(self, element):
        self.root.append(element)

    def insert(self, index, element):
        self.root.insert(index, element)

    def remove(self, element):
        self.root.remove(element)

    def replace(self, old_element, new_element):
        self.root.replace(old_element, new_element)

    def extend(self, elements):
        self.root.extend(elements)

    def find(self, path, namespaces=None):
        return self.root.find(path, namespaces)

    def findall(self, path, namespaces=None):
        return self.root.findall(path, namespaces)

    def findtext(self, path, default=None, namespaces=None):
        return self.root.findtext(path, default, namespaces)

    def getchildren(self):
        return [self.__class__(child) for child in self.root.getchildren()]

    def getparent(self):
        return self.__class__(self.root.getparent())

    def getroottree(self):
        return self.__class__(self.root.getroottree())

    def index(self, child, start=None, stop=None):
        return self.root.index(self, child, start, stop)

    # 选择器
    def cssselect(self, *args, **kwargs):
        lst = []
        for element in self.root.cssselect(*args, **kwargs):
            if isinstance(element, self.__class__.__bases__):
                lst.append(self.__class__(element))
            else:
                lst.append(element)
        return lst

    def css(self, query, *args, **kwargs):
        """等价于cssselect, 进行简写"""
        return self.cssselect(query, *args, **kwargs)

    def css_first(self, query, default=None, **kwargs):
        result = self.css(query, **kwargs)
        if result:
            return result[0]
        else:
            return default

    def re(self, pattern, flags=0):
        return re.findall(pattern, self.to_sting(), flags=flags)

    def re_first(self, pattern, default=None, flags=0):
        result = self.re(pattern, flags)
        if result:
            return result[0]
        else:
            return default

    def xpath(self, _path, namespaces=None, extensions=None, smart_strings=True, **_variables):
        lst = []
        for element in self.root.xpath(
                _path, namespaces=namespaces, extensions=extensions,
                smart_strings=smart_strings, **_variables):
            if isinstance(element, self.__class__.__bases__):
                lst.append(self.__class__(element))
            else:
                lst.append(element)
        return lst

    def xpath_first(self, query, default=None, **kwargs):
        result = self.xpath(query, **kwargs)
        if result:
            return result[0]
        else:
            return default

    # 扩展方法
    def drop_tag(self):
        """移除标签，不移除子节点"""
        return self.root.drop_tag()

    def drop_tree(self):
        """移除标签，移除子节点"""
        return self.root.drop_tree()

    def text_content(self):
        return self.root.text_content()

    def find_class(self, class_name):
        return self.root.find_class(class_name)

    def find_rel_links(self, rel):
        return self.root.find_rel_links(rel)

    def get_element_by_id(self, id, *default):
        return self.root.get_element_by_id(id, *default)

    def make_links_absolute(self, base_url=None, resolve_base_href=True, handle_failures=None):
        return self.root.make_links_absolute(base_url, resolve_base_href, handle_failures)

    def resolve_base_href(self, handle_failures=None):
        return self.root.resolve_base_href(handle_failures)

    def rewrite_links(self, link_repl_func, resolve_base_href=True, base_href=None):
        """newLink link_repl_func(oldLink) """
        return self.root.rewrite_links(link_repl_func, resolve_base_href, base_href)

    # 迭代器
    def iter(self, tag=None, *tags):
        for element in self.root.iter(tag=tag, *tags):
            yield self.__class__(element)

    def getiterator(self, tag=None, *tags):
        return self.iter(tag=tag, *tags)

    def iterancestors(self, tag=None, *tags):
        for element in self.root.iterancestors(tag=tag, *tags):
            yield self.__class__(element)

    def iterchildren(self, tag=None, *tags, reversed=False):
        for element in self.root.iterchildren(tag=tag, reversed=reversed, *tags):
            yield self.__class__(element)

    def iterdescendants(self, tag=None, *tags):
        for element in self.root.iterdescendants(tag=tag, *tags):
            yield self.__class__(element)

    def iterfind(self, path, namespaces=None):
        for element in self.root.iterfind(path, namespaces):
            yield self.__class__(element)

    def itersiblings(self, tag=None, *tags, preceding=False):
        for element in self.root.itersiblings(tag=tag, *tags, preceding=preceding):
            yield self.__class__(element)

    def itertext(self, tag=None, *tags, with_tail=True):
        for element in self.root.itertext(tag, *tags, with_tail=with_tail):
            yield element

    def iterlinks(self):
        for element, attribute, link, pos in self.root.iterlinks():
            yield Link(element, attribute, link, pos)

    # 从etree扩展
    def strip_attributes(self, *attribute_names):
        etree.strip_attributes(self.root, *attribute_names)

    def strip_elements(self, *tag_names, with_tail=True):
        etree.strip_elements(self.root, *tag_names, with_tail=with_tail)

    def strip_tags(self, *tag_names):
        etree.strip_tags(self.root, *tag_names)

    # 常用扩展
    def get_title(self, query='//title/text()'):
        return self.xpath_first(query)

    def get_description(self, query='//meta[@name="description"]/@content'):
        return self.xpath_first(query)

    def get_keywords(self, query='//meta[@name="keywords"]/@content'):
        return self.xpath_first(query)


Element = HtmlElementProxy
