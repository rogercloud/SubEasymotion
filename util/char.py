import sublime
import os, pickle, re

from path import package_path, state_cache

FORWARD = 1
BACKWARD = 2

class NaviRegion:
    """ state class for storing """
    def __init__(self, region, string, pair):
        self.begin = region.begin()
        self.end = region.end()
        self.string = string
        self.pair = pair


def add_char():
    """ produce char from a to Z """
    ret = add_char.char
    if ret == 'z':
        add_char.char = 'A'
    elif ret == 'Z':
        return 'Z'
    else:
        add_char.char = chr(ord(ret) + 1)
    return ret

def region_check_point(region, string, pair):
    """ Save origin region string and region position """
    navi = NaviRegion(region, string, pair)
    f = open(state_cache, 'w+')
    pickle.dump(navi, f)
    f.close()

def read_check_point():
    f = open(state_cache, 'r')
    region = pickle.load(f)
    f.close()
    return region

def locate_pair(direct, string):
    """ Locate the altered char in the string.
        Return value's the relative position in
        string """
    start = 0
    add_char.char = 'a'
    pair = []
    pos = []
    while True:
        match = re.search('[^\w]\w', string[start:])
        if match:
            start += match.end(0) - 1
            if direct == FORWARD:
                pair.append((add_char(), start))
            else:
                pos.append(start)
        else:
            break

    # BACKWARD needs for more care
    if direct == BACKWARD:
        pos.reverse()
        for p in pos:
            pair.append((add_char(), p))
        # First Char in BACKWARD
        if pos and (len(string) - 1) != pos[-1] \
                and not (string[0] == ' ' or string[0] == '\t'):
           pair.append((add_char(),0)) 
        
    return pair
 
def _replace(string, location):
    """ Really does character replace work. """
    for l in location:
        # Unicode replace
        char, pos = l
        string = string[:pos] + string[pos:].replace(string[pos], unicode(char), 1)
    return string

def replace_char(view, edit, direct):
    """ Replace begin character to a-zA-Z """
    if direct == FORWARD:
        start = view.sel()[0].begin()
        end = view.visible_region().end()
    else:
        start = view.visible_region().begin()
        end = view.sel()[0].end()

    region = sublime.Region(start, end)
    string = view.substr(region)
    pair = locate_pair(direct, string)
    region_check_point(region, string, pair)

    string = _replace(string, pair)
    view.replace(edit, region, string)

def restore_char(view, edit, direct):
    """ When edit complete, restore the strings """
    f = open(state_cache, 'r')
    region = pickle.load(f)
    f.close()
    view.replace(edit, sublime.Region(region.begin, region.end), 
            region.string)
    return region

def search_pair(char):
    """ Search though pair for postion according to char """
    region = read_check_point()
    pair = region.pair 
    for p in pair:
        if p[0] == char:
            return p[1]
    return None                 # not found

def jump(view, region, offset):
    """ Move cursor to specific offset, 
        if offset < 0, restore the cursor position """
    view.sel().clear()
    if offset < 0:              # cancel jump
        if not (offset + FORWARD):
            view.sel().add(sublime.Region(region.begin))
        else:
            view.sel().add(sublime.Region(region.end))
    else:
        view.sel().add(sublime.Region(region.begin + offset))
