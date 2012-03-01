from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter

f = open("tip1.py")

print highlight(f.read(), PythonLexer(), HtmlFormatter(linenos=True,))
#print HtmlFormatter().get_style_defs('.highlight')
