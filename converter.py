from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter
import re

HEADER = '<link rel="stylesheet" href="style.css">'

class tip():
	def __init__(self, name):
		self.name = name
		self.path = self.name + "/"
		self.refs = {}
		self.tip_data = ""

	def get_tip_data(self):
		f = open(self.path + "tip.html")
		self.tip_data = f.read()
		f.close()		

	def process_tip(self):
		snippets = re.findall("(<tip id=\"snip(\d*)\" />)", self.tip_data)

		for snippet in snippets:
			f = open(self.path + "snippets/" + "snip" + snippet[1] + ".py")
			snippet_code = f.read()
			snippet_code_lines = snippet_code.split("\n")
			for line in snippet_code_lines:
				references = re.search("(<<<ref#(\d)>>>)", line)
				if references:
					ref = references.groups()[1]
					self.refs[ref] = snippet_code_lines.index(line) + 1
					snippet_code = snippet_code.replace(references.groups()[0], "")
			f.close()
			self.tip_data = self.tip_data.replace(snippet[0], highlight(snippet_code, PythonLexer(), HtmlFormatter(linenos=True,)))

		snippet_refs = re.findall("(<<<ref#(\d)>>>)", self.tip_data)

		for snippet_ref in snippet_refs:
			#print REFS[str(snippet_ref[1])]
			self.tip_data = self.tip_data.replace(snippet_ref[0], str(self.refs[str(snippet_ref[1])]))
			
		output = HEADER + self.tip_data

		f = open("tmp.html", "w")
		f.write(output)
		f.close()

new_tip = tip("tip1")
new_tip.get_tip_data()
new_tip.process_tip()

#print highlight(f.read(), PythonLexer(), HtmlFormatter(linenos=True,))
#print HtmlFormatter().get_style_defs('.highlight')
