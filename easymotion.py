import sublime, sublime_plugin
import os
from util.theme import change_em_theme, restore_theme_syntax
import util.path as pt

class EasyMotionCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        view = self.view
        settings = view.settings()
        if is_in_em(settings):
            restore_theme_syntax(settings, view)
            return
        else:
            change_em_theme(settings, view)


def is_in_em(settings):
    return settings.get('easy_motion')
