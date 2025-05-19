from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

from pygments.styles import get_all_styles

styles = list(get_all_styles())
print(styles)

code = 'print("Hello world!")'
lang = 'python'
# print(highlight(code, lexer=get_lexer_by_name(lang), formatter=HtmlFormatter()))
