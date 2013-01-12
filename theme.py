import sublime, sublime_plugin

class ReadSchemeCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		settings = self.view.settings()
		theme = settings.get('color_scheme')

		settings.set('color_scheme', 'Packages/EasyMotion/EasyMotion.tmTheme')
