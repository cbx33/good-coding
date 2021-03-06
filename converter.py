from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.lexers import get_lexer_for_filename
from pygments.formatters import HtmlFormatter
import xml.etree.ElementTree as ET
import re
import os

LANG_DICT = {'py': 'Python', 'cpp' : 'C++'}

def set_template():
	global TEMPLATE
	f = open("template.html")
	TEMPLATE = f.read()
	f.close()

set_template()

class tip():
	def __init__(self, name):
		self.name = name
		self.title = ""
		self.subtitle = ""
		self.categories = []
		self.path = self.name + "/"
		self.snippet_path = self.path + "snippets/"
		self.refs = {}
		self.tip_data = ""
		self.langs = []
		self.snippet_file_list = self.cache_snippet_dir()
		self.def_lang = ""
		self.snippets = []

	def set_default_lang(self):
		if "py" in self.langs:
			self.def_lang = "py"
		else:
			self.def_lang = self.langs[0]
		self.langs.remove(self.def_lang)
		self.langs = [self.def_lang] + self.langs
		
	def cache_snippet_dir(self):
		 return os.listdir(self.snippet_path)

	def get_tip_data(self):
		f = open(self.path + "tip.html")
		self.tip_data = f.read()
		f.close()		

	def build_js_refs(self):
		js_ref_list = "\n\t\trefs = new Object;\n"
		count = 1
		for lang in self.langs:
			js_ref_list += "\t"*2 + "refs." + lang + "= new Array();\n"
			for ref in self.refs[lang]:
				js_ref_list += "\t"*2 + "refs." + lang + "[" + str(ref) + "]=" + str(self.refs[lang][ref]) + ";\n"
		return js_ref_list

	def build_js_lang(self):
		js_lang_list = "\n"
		count = 1
		for lang in self.langs:
			js_lang_list += "\t"*2 + 'langs[' + str(count) + '] = "' + lang + '";' + "\n"
			count += 1
		return js_lang_list

	def build_js_snippet(self):
		js_snippet_list = "\n"
		count = 1
		for snippet in self.snippets:
			js_snippet_list += "\t"*2 + 'snippets[' + str(count) + '] = "' + snippet + '";' + "\n"
			count += 1
		return js_snippet_list

	def build_html_categories(self):
		bs_cat = "<em>Categories: </em>"
		for cat in self.categories:
			bs_cat += '<span class="ref">' + cat + '</span>&nbsp'
		return '<div class="categories">' + bs_cat + '</div>'

	def output_tip(self):
		content = "<h1>" + self.title + "</h1>\n" + "<h2>" + self.subtitle + "</h2>\n"
		content += self.build_html_categories()
		content += self.tip_data
		output = TEMPLATE.replace("###CONTENT###", content)
		output = output.replace("###LANG_LIST###", self.build_js_lang())
		output = output.replace("###SNIPPET_LIST###", self.build_js_snippet())
		output = output.replace("###REFS_LIST###", self.build_js_refs())
		output = output.replace("###DEFAULT_LANG###", self.def_lang)
		output = output.replace("###TITLE###", self.title)
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

		if lang_first_time == True:
			self.set_default_lang()

		if len(check_lang) == 0:
			return True
		else:
			return check_lang

	def check_lang_ref(self, lang):
		if self.refs.has_key(lang):
			return True
		else:
			self.refs[lang] = {}

	def process_snippet_refs(self, snippet_code, lang):
		self.check_lang_ref(lang)
		#self.set_default_lang()
		snippet_code_lines = snippet_code.split("\n")
		for line in snippet_code_lines:
			references = re.search("(<<<ref#(\d)>>>)", line)
			if references:
				ref = references.groups()[1]
				self.refs[lang][ref] = snippet_code_lines.index(line) + 1
				snippet_code = snippet_code.replace(references.groups()[0], "")
		return snippet_code

	def process_snippet_lang(self, snippet_name, lang):
		snippet_filename = snippet_name + "." + lang
		snippet_lexer = get_lexer_for_filename(snippet_filename)
		f = open(self.snippet_path+ "/" + snippet_filename)
		snippet_code = f.read()
		f.close()

		snippet_code = self.process_snippet_refs(snippet_code, lang)

		return highlight(snippet_code, snippet_lexer, HtmlFormatter(linenos=True,))

	def is_visible_attrib(self, lang):
		if self.def_lang != lang:
			return 'style="display:none"'
		else:
			return ""

	def wrap_snippet(self, snippet_block, snippet_name, lang):
		div_name = snippet_name + "-" + lang
		header = "\n" + '<div id="' + div_name + '"' + self.is_visible_attrib(lang) + ' class="snippet">' + "\n"
		footer = "\n" + '</div>' + "\n"
		return header + snippet_block + footer		

	def change_lang_control(self, lang):
		attrib = 'onclick="change_lang(\'' + lang + '\')"'
		return attrib

	def wrap_snippet_blocks(self, snippet_blocks, snippet_name):
		header = '<table cellpadding="0" cellspacing="0" border="0" class="controls"><tr>'
		for lang in self.langs:
			if lang == self.def_lang:
				hclass = "active"
			else:
				hclass = "inactive"
			header += '<td id="' + snippet_name + '-btn-' + lang + '" class="' + hclass + '" ' + self.change_lang_control(lang) + ">" + LANG_DICT[lang] + "</td>"
		header += '<td class="helper_lang"><em>Click to change language</em></td></tr></table>'
		return '<div class="snippet-block">' + header + snippet_blocks + '</div>'

	def process_snippet(self, snippet_data):
		snippet_name = snippet_data[1]
		snippet_ref = snippet_data[0]
		self.snippets.append(snippet_name)
		check_snippet = self.check_snippet(snippet_name)
		if check_snippet != True:
			print (", ").join(check_snippet) + " is missing from snippet: " + snippet_name
			exit(1)

		snippet_blocks = ""

		for lang in self.langs:
			snippet_block = self.process_snippet_lang(snippet_name, lang)
			snippet_blocks += self.wrap_snippet(snippet_block, snippet_name, lang)

		snippet_control = self.wrap_snippet_blocks(snippet_blocks, snippet_name)

		self.tip_data = self.tip_data.replace(snippet_ref, snippet_control)

	def process_categories(self, categories):
		sp_cats = []
		cats = categories.split(",")
		for cat in cats:
			sp_cats.append(cat.strip())
		return sp_cats

	def process_metadata(self):
		xml = ET.parse(self.path + "metadata.xml")
		
		self.title = xml.find("title").text
		self.subtitle = xml.find("subtitle").text
		categories = xml.find("categories").text
		self.categories = self.process_categories(categories)

	def process_tip(self):
		self.get_tip_data()

		self.process_metadata()
		
		#Process snippets within the tip
		snippets = re.findall("(<tip id=\"(snip\d*)\" />)", self.tip_data)
		for snippet in snippets:
			self.process_snippet(snippet)

		current_lang = self.def_lang

		#Process snippet references
		snippet_refs = re.findall("(<<<ref#(\d)>>>)", self.tip_data)
		for snippet_ref in snippet_refs:
			div_name = "ref" + snippet_ref[1]
			header = '<span id="' + div_name + '" class="ref">'
			footer = '</span>'
			reference_wrapper = header + str(self.refs[current_lang][str(snippet_ref[1])]) + footer
			self.tip_data = self.tip_data.replace(snippet_ref[0], reference_wrapper)

new_tip = tip("tip1")
new_tip.process_tip()
new_tip.output_tip()
#print highlight(f.read(), PythonLexer(), HtmlFormatter(linenos=True,))
#print HtmlFormatter().get_style_defs('.highlight')
