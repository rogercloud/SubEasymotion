import sublime, sublime_plugin
import os
from util.theme import change_em_theme, restore_theme_syntax
import util.path as pt
import re

class EasyMotionCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        view = self.view
        settings = view.settings()
        if is_in_em(settings):
            restore_theme_syntax(settings, view)
            return
        else:
            change_em_theme(settings, view)
        start = view.sel()[0].begin()
        end = view.visible_region().end()
        selected_region = sublime.Region(start, end)
        string = view.substr(selected_region)
        new_string = string
        start = 0
        char = 'a'
        while True:
            match = re.search('[^\w]\w', new_string[start:])
            if match: 
                start += match.end(0) - 1
                print new_string[start:]
                new_string = new_string[:start] + new_string[start:].replace(new_string[start], unicode(char), 1)
                print new_string[start:]
                char = chr(ord(char) + 1)
                #new_string = new_string[start:]
            else:
                break
        print new_string
        view.replace(edit, selected_region, new_string)

def is_in_em(settings):
    return settings.get('easy_motion')

