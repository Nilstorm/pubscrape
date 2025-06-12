import re
latex_replacements = {
                r'\\rightarrow': '→',
                r'\\leftarrow': '←',
                r'\\Sigma': 'Σ',
                r'\\ell': 'ℓ',
                r'\\barν': 'ν',
                r'\\times': '×',
                r'\\infty': '∞',
                r'\\alpha': 'α',
                r'\\beta': 'β',
                r'\\gamma': 'γ',
                r'\\int': '∫',
                r'\\sum': '∑',
                r'\\partial': '∂',
                # Add ore LaTeX symbols as needed...
                }
unicode_fractions = {
    ('1', '2'): '½',
    ('1', '4'): '¼',
    ('3', '4'): '¾',
    ('1', '3'): '⅓',
    ('2', '3'): '⅔',
    ('1', '5'): '⅕',
    # Add more if needed
}

def replace_frac(m):
        num, denom = m.group(1), m.group(2)
        if (num, denom) in unicode_fractions:
            return unicode_fractions[(num, denom)]
        else:
            return f"{num}⁄{denom}"  # Use Unicode fraction slash
def clean_latex_math(match):
  math_expr = match.group(1)
  
  # Replace known LaTeX commands with their Unicode equivalents, but don't touch subscripts or superscripts
  for latex, unicode in latex_replacements.items():
      math_expr = re.sub(latex, unicode, math_expr)  # Using re.sub to handle replacements
  # Remove any extra LaTeX spacing like \,
  math_expr = re.sub(r'\\,', '', math_expr)
  return math_expr
  # Function to process the entire string
def clean_text(text):
      fraction_re = re.compile(r'\\frac{([^}]+)}{([^}]+)}')
      print(f"Original text: {text}")  # Debugging output
      cleaned_text = re.sub(r'\$(.*?)\$', clean_latex_math, text)  # For $...$
      cleaned_text = re.sub(r'\\\((.*?)\\\)', clean_latex_math, cleaned_text)  # For \( ... \)
      cleaned_text = fraction_re.sub(r'\1/\2', cleaned_text)
      cleaned_text = re.sub(r'\\frac\{([^{}]+)\}\{([^{}]+)\}', replace_frac, cleaned_text)
      print(f"Converted text for LaTeX: {cleaned_text}")
      return cleaned_text

clean_text("Magnetic moments of \\frac{1}{2}^- baryon resonances")