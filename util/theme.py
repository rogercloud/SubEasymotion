# -*- coding: utf-8 -*-

"""
    livecss.theme
    ~~~~~~~~~

    This module implements abstraction around ST theme.

"""

from os.path import basename, normpath, relpath, exists
from random import randint
import os.path
import re

import sublime

class Theme(object):
    """Global object represents ST color scheme """
    def __init__(self, settings):
        self.package_path = sublime.packages_path()
        self.sublime_path = os.path.dirname(self.package_path)
        self._settings = settings
        self.abs_path = None

    def abspath(self):
        if self.abs_path:
            return self.abs_path

        theme_path = self._settings.get('color_scheme') or ""
        if theme_path.startswith('Packages'):
            theme_path = os.path.join(self.sublime_path, theme_path)

        self.abs_path = normpath(theme_path)
        return self.abs_path

    def dirname(self):
        return os.path.dirname(self.abspath())

    def name(self):
        return basename(self.abspath())

    def set(self, theme_path):
        """Set current theme.
        :param theme: abs or relpath to SUBLIME_PATH
        """
        if exists(theme_path):
            self._settings.set('color_scheme', relpath(theme_path, self.sublime_path))

    def on_select_new_theme(cls, callback):
        self._settings.add_on_change('color_scheme', callback)



#def is_colorized(name):
#    if name.startswith(theme.prefix):
#        return True
#
#
#def colorized_path(path):
#    dirname = os.path.dirname(path)
#    name = basename(path)
#    return os.path.join(dirname, colorized_name(name))
#
#
#def colorized_name(name):
#    random = str(randint(1, 10 ** 15)) + '-'
#    return theme.prefix + random + uncolorized_name(name)
#
#
#def uncolorized_name(name):
#    if is_colorized(name):
#        s = re.search(theme.prefix + "(\d+-)?(?P<Name>.*)", name)
#        self_name = s.group('Name')
#        return self_name
#    return name
#
#
#def uncolorized_path(path):
#    dirname = os.path.dirname(path)
#    name = basename(path)
#    return os.path.join(dirname, uncolorized_name(name))
