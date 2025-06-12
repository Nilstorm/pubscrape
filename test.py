from pylatexenc.latex2text import LatexNodes2Text

# Example LaTeX string
latex_string = "\\sqrt{s}=13"

# Convert LaTeX to plain text (Unicode)
latex_string=latex_string.replace("'\\'","'\'")
plain_text = LatexNodes2Text().latex_to_text(latex_string)

print(plain_text)