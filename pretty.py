import tokenize
import sys
import keyword
# this is a test jbj
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
               {stats}
           </div>
           <div id="code">
               <h2>Python code</h2>
               {code}
           </div>
    </body>
</html>"""

# if len(sys.argv) < 2:
#     print("Usage: python script.py <filename>")
#     sys.exit(1)

# try:
#     with tokenize.open(sys.argv[1]) as file:
#         tokens = tokenize.generate_tokens(file.readline)

# except FileNotFoundError:
#     print(f"File '{sys.argv[1]}' not found.")
#     sys.exit(1)

    #Number of lines
def numline():
    line_count = 0 # Initialize a variable to keep track of the highest line number seen so far
    for token in tokens:# Iterate over each token in the tokens list
        if token.start[0] > line_count: # Check if the line number of the current token is greater than the highest line number seen so far
            n_lines = token.start[0] - 1 # Update the highest line number seen so far. Subtract 1 because line numbers in tokens start from 1, not 0.
    
    return f"Number of lines = {n_lines}"

#Maximum line length
def maxline():
    max_line_len = 0 # Initialize a variable to store the maximum line length
    for line in file:   # Iterate through each line in the file
        cur_line_len = len(line.rstrip("\n\r\f\v\f ")) # Remove any trailing whitespace or line break characters from the line
        max_line_len = max(max_line_len, cur_line_len) # Update the maximum line length if the current line is longer

    return f"Maximum line length = {max_line_len}"   # Return a string stating the maximum line length

#Maximum variable length
def maxvar():
    max_var_len = 0 # Initialize a variable to store the maximum variable length
    for token in tokens: # Iterate through each token in the tokens list
        if token.type == tokenize.NAME and not keyword.iskeyword(token.string):  # Check if the token is a variable name (not a keyword)
            cur_var_len_1 = len(token.string)  # Calculate the length of the variable name
            max_var_len = max(max_var_len, cur_var_len_1) # Update the maximum variable length if the current variable is longer
    return f"Maximum variable length = {max_var_len}"  # Return a string stating the maximum variable length

#Minimum variable length
def minvar():
    min_var_len = float("inf") # Set it to infinity initially to ensure that any variable length will be smaller
    for token in tokens: # Iterate through each token in the tokens list
        if token.type == tokenize.NAME and not keyword.iskeyword(token.string):  # Check if the token is a variable name (not a keyword)
            cur_var_len_2 = len(token.string) # Calculate the length of the variable name
            min_var_len = min(min_var_len, cur_var_len_2) # Update the minimum variable length if the current variable is shorter
    return f"Minimum variable length = {min_var_len}" # Return a string stating the minimum variable length

#Number of comment lines
def numcom():
    n_com = 0 # Initialize a variable to count the number of comments
    for token in tokens: # Iterate through each token in the tokens list
        if token.type == tokenize.COMMENT: # Check if the token is a comment
            n_com += 1 # Increment the comment count
    return f"Number of comment lines = {n_com}" # Return a string stating the number of comment lines

#Number of definitions
def numdef():
    def_count = 0  # Initialize a variable to count the number of function definitions
    for token in tokens: # Iterate through each token in the tokens list
        if token.type == tokenize.NAME and token.string in ("def",): # Check if the token is the keyword 'def' which is used to define functions in Python
            def_count += 1 # Increment the definition count
    return f"Number of definitions = {def_count}"  # Return a string stating the number of function definitions

#Number of strings
def numstr():
    str_count = 0
    for token in tokens:
        if token.type == tokenize.STRING:
            str_count += 1
    return f"Number of strings = {str_count}"

#Number of numbers
def numnum():
    num_count = 0 # Initialize a variable to count the number of string literals
    for token in tokens: # Iterate through each token in the tokens list
        if token.type == tokenize.NUMBER: # Check if the token is a string literal
            num_count += 1  # Increment the string count
    return f"Number of numbers = {num_count}"  # Return a string stating the number of string literals

#Number of repeated constants
def numrep():
    rep_set = set()  # Set to store encountered constants
    rep_count = set()  # Set to store repeated constants
    for token in tokens:
        if token.type in (tokenize.STRING, tokenize.NUMBER):
            rep = token.string # Get the string representation of the constant
            if rep in rep_set:
                rep_count.add(rep)  # Add the constant to repeated_constants set
            else:
                rep_set.add(rep)
    return f"Number of repeated constants = {len(rep_count)}"
    

with tokenize.open(sys.argv[1]) as file:
    tokens = list(tokenize.generate_tokens(file.readline))
    stats_list = [
        numline(),
        maxline(),
        maxvar(),
        minvar(),
        numcom(),
        numdef(),
        numstr(),
        numnum(),
        numrep(),
    ]
    stat_output = "</ul>\n" # Initialize a string to hold the HTML output for a list of statistics
    for s in stats_list: # Iterate through each statistic in the stats_list
        stat_output += "<li>" + s + "</li>\n" # Append an HTML list item element containing the statistic to the output string
    

# Format the HTML template with the statistics list and an empty code section
html_output = HTML_TEMPLATE.format(stats = stat_output + "</ui>", code = "")
print(html_output)