# -*- coding: utf-8 -*-
from collections import OrderedDict


class Styles(object):
    """dict-like"""

    def __init__(self, attributes):
        """
        :param attributes: dict
        """
        self._attributes = attributes

    def _loads(self):
        return self.parse_style(self._attributes.get('style'))

    def _dumps(self, styles):
        self._attributes['style'] = self.serialize_style(styles)

    def set(self, key, value):
        styles = self._loads()
        styles[key] = value
        self._dumps(styles)

    def get(self, key, default=None):
        return self._loads().get(key, default)

    def pop(self, key, default=None):
        styles = self._loads()
        value = styles.pop(key, default)
        self._dumps(styles)
        return value

    def has_key(self, key):
        styles = self._loads()
        return key in styles

    @classmethod
    def serialize_style(cls, styles):
        lst = []
        for key, value in styles.items():
            lst.append(f"{key}: {value};")

        return ' '.join(lst)

    @classmethod
    def parse_style(cls, style):
        styles = OrderedDict()

        if style is None: return styles
        if style.strip() == '': return styles

        for item in style.split(';'):
            key_value = item.split(":", 1)
            if len(key_value) == 2:
                key, value = key_value
                key = key.strip()
                if key:
                    styles[key] = value.strip()

        return styles
