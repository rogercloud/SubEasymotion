import sublime, sublime_plugin

from util.theme import change_em_theme, restore_theme_syntax
from util.char import restore_char, replace_char, jump, search_pair,\
        FORWARD, BACKWARD

class CancelEasymotionCommand(sublime_plugin.TextCommand):
    """ Turn off easy motion flag """
    def run(self, edit):
        view = self.view
        settings = view.settings()
        cancel_easymotion(edit, settings, view, False)


class EasyMotionCommand(sublime_plugin.TextCommand):
    """ Turn on easy motion flag """
    def run(self, edit, direct = FORWARD):
        view = self.view
        settings = view.settings()
        settings.set('easy_motion', True)
        settings.set('command_mode', False)
        settings.set('easy_motion_command', direct)
        change_em_theme(settings, view)
        replace_char(view, edit, direct)

class EasyMotionJumpCommand(sublime_plugin.TextCommand):
    """ Jump to char """
    def run(self, edit, char = 'Z'):
        view = self.view
        settings = view.settings()
        offset = search_pair(char)
        cancel_easymotion(edit, settings, view, offset)

def cancel_easymotion(edit, settings, view, offset):
    """ Turn off easymotion is required when both jump and cancel,
        Abstract it to a single func."""
    if typed_command(settings):
        restore_theme_syntax(settings, view)
        direct = settings.get('easy_motion_command')
        region = restore_char(view, edit, direct)
        if not offset:
            jump(view, region, 0 - direct)
        else:
            jump(view, region, offset)
        settings.set('easy_motion_command', False)
    settings.set('easy_motion', False)
    settings.set('command_mode', True)

##########################################################
# Check State Func
def in_em(settings):
    return settings.get('easy_motion')

def typed_command(settings):
    return settings.get('easy_motion_command')
