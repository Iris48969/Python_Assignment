import tokenize
import sys
import keyword
import io
import html

HTML_TEMPLATE = """<!doctype html>
<html lang=en>
    <head>
        <meta charset=utf-8>
        <title>Pretty Python</title>
        <style>
            pre {{font-size: 16pt}}
            .variable {{color: black}}
            .comment {{color: green}}
            .keyword {{color: blue}}
            .string {{color: orange}}
            .number {{color: red}}
            .operator {{color: purple}}
        </style>
    </head>
    <body>
        <h1>Python code inspector</h1>
        <ul>
            <li><a href="#stats">Statistics</a></li>
            <li><a href="#code">Code</a></li>
        </ul>
        <div id="stats">
            <h2>Statistics</h2>
            <ul>
               {stats}
            </ul>
        </div>
        <div id="code">
            <h2>Python code</h2>
            <pre><code>{code}</pre></code>
        </div>
    </body>
</html>"""

def generate_statistics(tokens, file_content):
    """Generate statistics based on tokens."""
    stats = {
        'n_lines': len(file_content.splitlines()),
        'max_line_length': max(len(line) for line in file_content.splitlines()),
        'max_var_length': 0,
        'min_var_length': float('inf'),
        'n_comments': 0,
        'n_definitions': 0,
        'n_strings': 0,
        'n_numbers': 0,
        'n_repeated_constants': 0
    }
    
    constants = {}
    previous_token = None

    for token in tokens:
        toknum, tokval = token.type, token.string
        if toknum == tokenize.NAME:
            if not keyword.iskeyword(tokval):
                stats['max_var_length'] = max(stats['max_var_length'], len(tokval))
                stats['min_var_length'] = min(stats['min_var_length'], len(tokval))
            elif tokval == 'def' and previous_token is not None and previous_token.type in [tokenize.INDENT, tokenize.DEDENT, tokenize.NEWLINE, tokenize.NL]:
                
                stats['n_definitions'] += 1
        elif toknum == tokenize.COMMENT:
            stats['n_comments'] += 1
        elif toknum == tokenize.STRING:
            stats['n_strings'] += 1
            constants[tokval] = constants.get(tokval, 0) + 1
        elif toknum == tokenize.NUMBER:
            stats['n_numbers'] += 1
            constants[tokval] = constants.get(tokval, 0) + 1
        
        previous_token = token

    
    if stats['min_var_length'] == float('inf'):
        stats['min_var_length'] = 0
    
    
    stats['n_repeated_constants'] = sum(1 for count in constants.values() if count > 1)
    
    return stats

def format_statistics(stats):
    
    return '\n'.join(f'<li>{key.replace("_", " ").capitalize()}: {value}</li>' for key, value in stats.items())
def apply_syntax_highlighting(file_content):
    """Apply syntax highlighting to Python code based on tokens."""
    highlighted_code = ""
    try:
        tokens = tokenize.tokenize(io.BytesIO(file_content.encode('utf-8')).readline)
        for tok_type, tok_string, _, _, _ in tokens:
            if tok_type == tokenize.ENCODING:
                continue  # Skip encoding declaration
            
            # HTML escape the token string to ensure special characters are displayed correctly
            tok_string_escaped = html.escape(tok_string)
            
            if tok_type == tokenize.COMMENT:
                highlighted_code += f'<span class="comment">{tok_string_escaped}</span>'
            elif tok_type == tokenize.STRING:
                highlighted_code += f'<span class="string">{tok_string_escaped}</span>'
            elif tok_type == tokenize.NUMBER:
                highlighted_code += f'<span class="number">{tok_string_escaped}</span>'
            elif tok_type == tokenize.NAME and keyword.iskeyword(tok_string):
                highlighted_code += f'<span class="keyword">{tok_string_escaped}</span>'
            elif tok_type in [tokenize.INDENT, tokenize.DEDENT, tokenize.NEWLINE, tokenize.NL]:
                highlighted_code += tok_string_escaped.replace('    ', '&nbsp;'*4)
            else:
                # Replace spaces with &nbsp; to preserve inline spaces and handle newlines
                highlighted_code += tok_string_escaped.replace(' ', '&nbsp;').replace('\n', '<br>')
                
    except tokenize.TokenError as e:
        print(f"Token error: {e}")
    return highlighted_code

# HTML template definition remains the same
'''
def apply_syntax_highlighting(file_content):
    """Apply syntax highlighting to Python code based on tokens."""
    highlighted_code = ""
    try:
        tokens = tokenize.tokenize(io.BytesIO(file_content.encode('utf-8')).readline)
        for tok_type, tok_string, _, _, _ in tokens:
            if tok_type == tokenize.ENCODING:
                # Skip encoding declaration, which is not part of the actual code
                continue
            elif tok_type == tokenize.COMMENT:
                highlighted_code += f'<span class="comment">{tok_string}</span>'
            elif tok_type == tokenize.STRING:
                highlighted_code += f'<span class="string">{tok_string}</span>'
            elif tok_type == tokenize.NUMBER:
                highlighted_code += f'<span class="number">{tok_string}</span>'
            elif tok_type == tokenize.NAME and keyword.iskeyword(tok_string):
                highlighted_code += f'<span class="keyword">{tok_string}</span>'
            else:
                # Directly append other tokens, including whitespace, to preserve the code structure
                highlighted_code += tok_string
    except tokenize.TokenError as e:
        print(f"Token error: {e}")
    return highlighted_code
'''
# generate_statistics and format_statistics functions remain the same
def main(filename):
    try:
        with tokenize.open(filename) as f:
            file_content = f.read()
        
        # Tokenize the file content and apply syntax highlighting
        highlighted_code = apply_syntax_highlighting(file_content)

        # Generate statistics
        tokens = tokenize.tokenize(io.BytesIO(file_content.encode('utf-8')).readline)
        stats = generate_statistics(list(tokens), file_content)
        formatted_stats = format_statistics(stats)

        # Generate the final HTML output
        html_output = HTML_TEMPLATE.format(stats=formatted_stats, code=highlighted_code)
        print(html_output)
        
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)

# The rest of the script remains unchanged

'''
def main(filename):
    try:
        with tokenize.open(filename) as f:
            file_content = f.read()
        # Apply syntax highlighting
        highlighted_code = apply_syntax_highlighting(file_content)
        # Assuming generate_statistics and format_statistics are defined elsewhere
        tokens = tokenize.tokenize(io.BytesIO(file_content.encode('utf-8')).readline)
        stats = generate_statistics(list(tokens), file_content)
        formatted_stats = format_statistics(stats)
        # Generate the final HTML output
        html_output = HTML_TEMPLATE.format(stats=formatted_stats, code=highlighted_code)
        print(html_output)
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)
'''
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <filename>")
        sys.exit(1)
    main(sys.argv[1])
