import sublime, os

package_path = sublime.packages_path()
sublime_path = os.path.dirname(package_path)
package_name = '/SubEasymotion'
state_cache = package_path + package_name +'/state-store.cache'
