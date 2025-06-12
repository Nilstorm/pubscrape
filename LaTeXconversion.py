import re

# Define LaTeX to Unicode replacements, excluding subscript and superscript
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
    # Add more LaTeX symbols as needed...
}

# Function to clean LaTeX math expressions and replace symbols
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
    print(f"Original text: {text}")  # Debugging output
    cleaned_text = re.sub(r'\$(.*?)\$', clean_latex_math, text)  # For $...$
    cleaned_text = re.sub(r'\\\((.*?)\\\)', clean_latex_math, cleaned_text)  # For \( ... \)
    
    return cleaned_text

# Sample scraped text
sample_text = "Phenomenology of the semileptonic $Σ_{b}^{*0}\\,\\rightarrow\\,  Σ_{c}^{+}\\,\\ell\\,\\barν_{\\ell}$ transition within QCD sum rules."

# Clean the text
cleaned_text = clean_text(sample_text)

# Output cleaned text
print(f"Cleaned text: {cleaned_text}")