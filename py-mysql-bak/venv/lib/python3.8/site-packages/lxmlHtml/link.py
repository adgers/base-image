# -*- coding: utf-8 -*-


class Link(object):
    def __init__(self, element, attribute, link, position):
        self.element = element
        self.attribute = attribute
        self.link = link
        self.position = position

    @property
    def text(self):
        return self.element.text
