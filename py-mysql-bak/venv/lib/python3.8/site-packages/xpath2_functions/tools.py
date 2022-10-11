# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from . import functions as xpath_fns


def register_functions(etree, ns='http://kjw.pt/xpath2-functions', functions=None):
    """
    Usage::

        from lxml import etree
        import xpath2_functions

        # registering all available functions in default namespace
        xpath2_functions.register_functions(etree)

        # registering chosen functions in the empty namespace
        xpath2_functions.register_functions(etree, ns=None, ['string-join'])
    """
    if functions is None:
        functions = xpath_fns.ALL_FUNCTIONS.keys()
    else:
        for fn_name in functions:
            if fn_name not in xpath_fns.ALL_FUNCTIONS:
                raise Exception('Function %s is not available in current version' % fn_name)

    etree_functions = etree.FunctionNamespace(ns)
    etree_functions.prefix = 'xp2f'
    for fn_name in functions:
        etree_functions[fn_name] = xpath_fns.ALL_FUNCTIONS[fn_name]
