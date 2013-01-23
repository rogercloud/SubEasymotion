import sublime, os

package_path = sublime.packages_path()
sublime_path = os.path.dirname(package_path)

def em_theme_path(name):
    return package_path + '/EasyMotion/themecache/' + name + '-easy'
