# -*- coding: utf-8 -*-

"""
    Use some code from livecss
    ~~~~~~~~~

    This module implements abstraction around ST theme.

"""

from os.path import basename, normpath, relpath, exists
from random import randint
import os.path
import re
import plistlib

import sublime
from path import package_path, sublime_path

em_syntax = 'Packages/EasyMotion/EasyMotion.tmLanguage'

class Theme(object):
    """Global object represents ST color scheme """
    def __init__(self, theme_path):
        self.theme_path = theme_path
        self.abs_path = None

    def abspath(self):
        if self.abs_path:
            return self.abs_path

        # likely
        if self.theme_path.startswith('Packages'):
            self.theme_path = os.path.join(sublime_path, self.theme_path)

        self.abs_path = normpath(self.theme_path)
        return self.abs_path

    def dirname(self):
        return os.path.dirname(self.abspath())

    def name(self):
        return basename(self.abspath())


class EMTheme():
    def __init__(self, theme):
        self.theme = theme
        self.easy_theme_cache = "/EasyMotion/themecache/"

    def name(self):
        return self.theme.name() + "-easy"

    def abspath(self):
        return package_path + self.easy_theme_cache + self.name()

    def dirname(self):
        return os.path.dirname(abspath())


def theme_from_settings(settings):
    return settings.get('color_scheme')

def set(settings, theme_path):
    """Set current theme.
        :param theme: abs or relpath to SUBLIME_PATH
    """
    if exists(theme_path):
        settings.set('color_scheme', relpath(theme_path, sublime_path))

def on_new_theme(settings, callback):
    settings.add_on_change('color_scheme', callback)

def store_theme_syntax(settings, theme, syntax):
    settings.set('easy_motion_replace_theme', theme)
    settings.set('easy_motion_replace_syntax', syntax)

def restore_theme_syntax(settings, view):
    view.set_syntax_file(settings.get('easy_motion_replace_syntax'))
    set(settings, settings.get('easy_motion_replace_theme'))

def generate_em_theme(name, for_color, back_color):
    dict = {
            'name': name, 
            'settings':[{
                'settings':{
                    'background': back_color, 
                    'foreground': for_color
                    }
                }, {
                    'name': 'Start Character',
                    'scope':'keyword.easymotion',
                    'settings': {'foreground': '#FF0000'}
                    }
                ] 
           }
    return dict

def filter_for_back_color(plist):
    settings = plist['settings']
    for_color = None
    back_color = None
    for s in settings:
        if not 'scope' in s:
            for_color = s['settings']['foreground']
            back_color = s['settings']['background']
            break

    return for_color, back_color

def change_em_theme(settings, view):
    # current syntax and theme
    syntax = settings.get('syntax')
    theme = Theme(theme_from_settings(settings))
    emtheme = EMTheme(theme)
    store_theme_syntax(settings, theme.abspath(), syntax)

    theme_file = open(theme.abspath(), 'r')
    em_theme_file = open(emtheme.abspath(), 'w+')

    # parse theme
    plist = plistlib.readPlist(theme_file)
    for_color, back_color = filter_for_back_color(plist)
    new_plist = generate_em_theme(emtheme.name(), for_color, back_color)
    plistlib.writePlist(new_plist, em_theme_file)

    # flush file , set syntax and theme
    theme_file.close()
    em_theme_file.close()
    set(settings, emtheme.abspath())
    view.set_syntax_file(em_syntax)

