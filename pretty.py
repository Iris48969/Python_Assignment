import tokenize
import sys
import keyword
import io
import html
from keyword import iskeyword

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
        'number_of_lines': len(file_content.splitlines()),
        'maximum_line_length': max(len(line) for line in file_content.splitlines()),
        'maximum_variable_length': 0,
        'minimum_variable_length': float('inf'),
        'number_of_comment_lines': 0,
        'number_of_definitions': 0,
        'number_of_strings': 0,
        'number_of_numbers': 0,
        'number_of_repeated_constants': 0
    }
    
    constants = {}
    previous_token = None

    for token in tokens:
        toknum, tokval = token.type, token.string
        if toknum == tokenize.NAME:
            if not keyword.iskeyword(tokval):
                stats['maximum_variable_length'] = max(stats['maximum_variable_length'], len(tokval))
                stats['minimum_variable_length'] = min(stats['minimum_variable_length'], len(tokval))
            elif tokval == 'def' and previous_token is not None and previous_token.type in [tokenize.INDENT, tokenize.DEDENT, tokenize.NEWLINE, tokenize.NL]:
                
                stats['number_of_definitions'] += 1
        elif toknum == tokenize.COMMENT:
            stats['number_of_comment_lines'] += 1
        elif toknum == tokenize.STRING:
            stats['number_of_strings'] += 1
            constants[tokval] = constants.get(tokval, 0) + 1
        elif toknum == tokenize.NUMBER:
            stats['number_of_numbers'] += 1
            constants[tokval] = constants.get(tokval, 0) + 1
        
        previous_token = token

    
    if stats['minimum_variable_length'] == float('inf'):
        stats['minimum_variable_length'] = 0
    
    
    stats['number_of_repeated_constants'] = sum(1 for count in constants.values() if count > 1)
    
    return stats

def format_statistics(stats):
    
    return '\n'.join(f'<li>{key.replace("_", " ").capitalize()} = {value}</li>' for key, value in stats.items())


def apply_syntax_highlighting(file_content):
    """Apply syntax highlighting to Python code based on tokens and preserve spaces, including line numbers and indentation."""
    highlighted_code = ""
    line_number = 1
    current_line = ""  # Buffer to hold the contents of the current line
    last_end = (1, 0)  # Initial position (line 1, column 0)

    def space_needed_intext(current_start):
        if last_end[0] == current_start[0]:  # Same line
            space_needed = ' ' * (current_start[1] - last_end[1])
            return space_needed
        elif last_end[0] < current_start[0]:  # New line
            space_needed = ' ' * (current_start[1] - 1)
            return space_needed
        else:
            return ''  # Default, no space needed

    tokens = tokenize.tokenize(io.BytesIO(file_content.encode('utf-8')).readline)
    try:
        for tok_type, tok_string, start, end, line in tokens:
            if tok_type == tokenize.ENCODING:
                continue  # Skip encoding declaration

            # Adjust line number and handle multiline tokens
            while line_number < start[0]:
                highlighted_code += f'<span class="line-number">{line_number}{" "*(10-len(str(line_number)))}</span>{current_line}\n'
                current_line = ""  # Reset current line for the new line
                line_number += 1

            # Add the calculated space needed before the token
            space_needed = space_needed_intext(start)
            current_line += space_needed

            css_class = {
                tokenize.COMMENT: 'comment',
                tokenize.STRING: 'string',
                tokenize.NUMBER: 'number',
                tokenize.NAME: 'keyword' if keyword.iskeyword(tok_string) else 'variable',
                tokenize.OP: 'operator'
            }.get(tok_type, '')
            
            lines = tok_string.splitlines(True)
            # Append the current token to the current line with appropriate HTML formatting
            if '\n' in tok_string:
                lines = tok_string.splitlines(True)
                for i, line in enumerate(lines):
                    line_html = html.escape(line)
                    if i == 0:
                        current_line += f'<span class="{css_class}">{line_html}</span>'
                    else:
                        highlighted_code += f'<span class="line-number">{line_number}{" "*(10-len(str(line_number)))}</span>{current_line}'
                        current_line = f'<span class="{css_class}">{line_html}</span>'
                        line_number += 1
            else:
                tok_string_escaped = html.escape(tok_string)
                current_line += f'<span class="{css_class}">{tok_string_escaped}</span>'

            last_end = end

        # Append any remaining content after the last token
        if current_line:
            highlighted_code += f'<span class="line-number">{line_number}{" "*(10-len(str(line_number)))}</span>{current_line}\n'

    except tokenize.TokenError as e:
        print(f"Token error: {e}")

    return highlighted_code

# Note: This function should be called with Python code as a string.
# Example:
# file_content = "your_python_code_here"
# print(apply_syntax_highlighting(file_content))


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


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <filename>")
        sys.exit(1)
    main(sys.argv[1])
