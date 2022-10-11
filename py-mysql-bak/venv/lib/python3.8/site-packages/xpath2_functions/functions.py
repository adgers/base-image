# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from lxml.etree import _Element


def textify_node(node):
    if isinstance(node, _Element):
        return node.xpath('.//text()')[0]
    else:
        return node


def string_join(context, items, separator):
    items = [textify_node(i) for i in items]
    return separator.join(items)


def lower_case(context, item, *args, **kwargs):
    if type(item) is list:
        items = []
        for i in item:
            items.append(i.lower())
        return items
    return item


ALL_FUNCTIONS = {
    'string-join': string_join,
    'lower-case': lower_case,
}
