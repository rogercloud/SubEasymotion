import sublime, sublime_plugin
import os, plistlib
import util.theme as th
import util.path as pt

class DebugCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        settings = self.view.settings()
        theme = th.Theme(settings)
        old_theme_file = open(theme.abspath(), 'r')
        em_theme_name = theme.name() + '-easy'
        em_theme_file = open(pt.em_theme_path(theme.name()), 'w+')

        old_plist = plistlib.readPlist(old_theme_file)
        print(type(old_plist))
        for_color, back_color = filter_for_back_color(old_plist)
        new_plist = generate_em_theme(em_theme_name, for_color, back_color)
        print(new_plist)
        plistlib.writePlist(new_plist, em_theme_file)
        old_theme_file.close()
        em_theme_file.close()
        # Theme
        settings.set('color_scheme', 'Packages/EasyMotion/themecache/' + em_theme_name)
        # Syntax
        self.view.set_syntax_file('Packages/EasyMotion/EasyMotion.tmLanguage')

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
