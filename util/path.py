import sublime, os

package_path = sublime.packages_path()
sublime_path = os.path.dirname(package_path)
state_cache = package_path + '/state-store.cache'
