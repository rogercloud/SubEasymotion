import sublime
import os, pickle, re

from path import package_path

FORWARD = 1
BACKWARD = 2

class NaviRegion:
    def __init__(self, region, string, pair):
        self.begin = region.begin()
        self.end = region.end()
        self.string = string
        self.pair = pair

def add_char():
    """ Add character """
    ret = add_char.char
    if ret == 'z':
        add_char.char = 'A'
    elif ret == 'Z':
        return 'Z'
    else:
        add_char.char = chr(ord(ret) + 1)
    return ret

def region_check_point(region, string, pair):
    """ Save origin region string and region position"""
    navi = NaviRegion(region, string, pair)
    f = open(package_path + '/state-store.cache', 'w+')
    pickle.dump(navi, f)
    f.close()

def locate_pair(direct, string):
    """ Locate the altered char in the string.
        Return value's the relative position in
        string"""
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
    f = open(package_path + '/state-store.cache', 'r')
    region = pickle.load(f)
    f.close()
    view.replace(edit, sublime.Region(region.begin, region.end), 
            region.string)
    return region

def search_pair(char):
    f = open(package_path + '/state-store.cache', 'r')
    region = pickle.load(f)
    f.close()
    pair = region.pair 
    for p in pair:
        if p[0] == char:
            return p[1]
    return pair[-1][1]          # not found

def jump(view, region, offset):
    view.sel().clear()
    if offset < 0:              # cancel jump
        if not (offset + FORWARD):
            view.sel().add(sublime.Region(region.begin))
        else:
            view.sel().add(sublime.Region(region.end))
    else:
        view.sel().add(sublime.Region(region.begin + offset))
