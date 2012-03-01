from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter
import re

TIP_NAME = "tip1"
path = TIP_NAME + "/"

HEADER = '<link rel="stylesheet" href="style.css">'
REFS = {}

f = open(path + "tip.html")
tip_html = f.read()
f.close()

snippets = re.findall("(<tip id=\"snip(\d*)\" />)", tip_html)

for snippet in snippets:
	f = open(path + "snippets/" + "snip" + snippet[1] + ".py")
	snippet_code = f.read()
	snippet_code_lines = snippet_code.split("\n")
	for line in snippet_code_lines:
		references = re.search("(<<<ref#(\d)>>>)", line)
		if references:
			ref = references.groups()[1]
			REFS[ref] = snippet_code_lines.index(line) + 1
			snippet_code = snippet_code.replace(references.groups()[0], "")
	f.close()
	tip_html = tip_html.replace(snippet[0], highlight(snippet_code, PythonLexer(), HtmlFormatter(linenos=True,)))

snippet_refs = re.findall("(<<<ref#(\d)>>>)", tip_html)

for snippet_ref in snippet_refs:
	#print REFS[str(snippet_ref[1])]
	tip_html = tip_html.replace(snippet_ref[0], str(REFS[str(snippet_ref[1])]))
	
output = HEADER + tip_html

f = open("tmp.html", "w")
f.write(output)
f.close()

#print highlight(f.read(), PythonLexer(), HtmlFormatter(linenos=True,))
#print HtmlFormatter().get_style_defs('.highlight')
