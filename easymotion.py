import sublime, sublime_plugin

from util.theme import change_em_theme, restore_theme_syntax
from util.char import restore_char, replace_char, FORWARD, BACKWARD

class EasyMotionCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        view = self.view
        settings = view.settings()
        if is_in_em(settings):
            restore_theme_syntax(settings, view)
            restore_char(view, edit, BACKWARD)
            return
        else:
            change_em_theme(settings, view)
            replace_char(view, edit, BACKWARD)

def is_in_em(settings):
    return settings.get('easy_motion')
