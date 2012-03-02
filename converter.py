from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter
import re
import os

HEADER = '<link rel="stylesheet" href="style.css">'

class tip():
	def __init__(self, name):
		self.name = name
		self.path = self.name + "/"
		self.snippet_path = self.path + "snippets/"
		self.refs = {}
		self.tip_data = ""
		self.langs = []
		self.snippet_file_list = self.cache_snippet_dir()
		
	def cache_snippet_dir(self):
		 return os.listdir(self.snippet_path)

	def get_tip_data(self):
		f = open(self.path + "tip.html")
		self.tip_data = f.read()
		f.close()		

	def output_tip(self):
		output = HEADER + self.tip_data

		f = open("tmp.html", "w")
		f.write(output)
		f.close()

	def check_snippet(self, name):
		lang_first_time = False
		if self.langs == []:
			lang_first_time = True
			check_lang = []
		else:
			check_lang = self.langs[:]
		for filename in self.snippet_file_list:
			if name in filename:
				path_split = os.path.splitext(filename)
				extn = path_split[1].split(".")[1]
				if lang_first_time == True:
					self.langs.append(extn)
				else:
					check_lang.remove(extn)
		if len(check_lang) == 0:
			return True
		else:
			return check_lang
		print self.langs

	def process_snippet(self, snippet_data):
		check_snippet = self.check_snippet(snippet_data[1])
		if check_snippet != True:
			print (", ").join(check_snippet) + " is missing from snippet: " + snippet_data[1]
			
		exit(0)
			
		f = open(self.path + "snippets/" + snippet_data[1] + ".py")
		snippet_code = f.read()
		snippet_code_lines = snippet_code.split("\n")
		for line in snippet_code_lines:
			references = re.search("(<<<ref#(\d)>>>)", line)
			if references:
				ref = references.groups()[1]
				self.refs[ref] = snippet_code_lines.index(line) + 1
				snippet_code = snippet_code.replace(references.groups()[0], "")
		f.close()
		self.tip_data = self.tip_data.replace(snippet_data[0], highlight(snippet_code, PythonLexer(), HtmlFormatter(linenos=True,)))

	def process_tip(self):
		self.get_tip_data()
		
		#Process snippets within the tip
		snippets = re.findall("(<tip id=\"(snip\d*)\" />)", self.tip_data)
		for snippet in snippets:
			self.process_snippet(snippet)

		#Process snippet references
		snippet_refs = re.findall("(<<<ref#(\d)>>>)", self.tip_data)
		for snippet_ref in snippet_refs:
			self.tip_data = self.tip_data.replace(snippet_ref[0], str(self.refs[str(snippet_ref[1])]))


new_tip = tip("tip1")
new_tip.process_tip()

#print highlight(f.read(), PythonLexer(), HtmlFormatter(linenos=True,))
#print HtmlFormatter().get_style_defs('.highlight')
