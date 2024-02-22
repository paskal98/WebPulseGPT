import json
import re

import requests


def get_ast_request(code):
    url = 'http://localhost:3210/parse'
    data = {'code': code}
    headers = {'Content-Type': 'application/json'}

    try:
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            parsed_ast = response.json()
            return parsed_ast
        else:
            print("Error:", response.text)
    except Exception as e:
        print("Error occurred:", e)


def parse_ast_conditionally(ast):
    # Initialize state variables
    has_dom_content_loaded = False
    top_level_variables = []
    top_level_functions = []
    nested_variables = []
    nested_functions = []
    callbacks = set()  # For capturing unique callback identifiers
    arrow_functions = []  # For capturing arrow function variable names

    # Helper function to add variables, including handling arrow functions
    def add_variables(declarations, is_nested):
        for decl in declarations:
            var_name = decl['id']['name']
            # Check if it's an arrow function
            if decl.get('init') and decl['init']['type'] == 'ArrowFunctionExpression':
                arrow_functions.append(var_name)
            if is_nested:
                nested_variables.append(var_name)
            else:
                top_level_variables.append(var_name)

    # Helper function to add functions, including handling addEventListener callbacks
    def add_functions(node, is_nested):
        func_name = ''
        if node['type'] == 'FunctionDeclaration':
            func_name = node['id']['name']
        elif (node['type'] == 'ExpressionStatement' and
              node['expression']['type'] == 'CallExpression' and
              node['expression']['callee']['type'] == 'MemberExpression' and
              node['expression']['callee']['property']['name'] == 'addEventListener'):
            event_type = node['expression']['arguments'][0]['value']
            callbacks.add(node['expression']['callee']['object']['name'])

        if func_name:
            if is_nested:
                nested_functions.append(func_name)
            else:
                top_level_functions.append(func_name)

    # Main node processing function
    def process_node(node, is_nested=False):
        if node['type'] == 'VariableDeclaration':
            add_variables(node['declarations'], is_nested)
        elif node['type'] in ['FunctionDeclaration', 'ExpressionStatement']:
            add_functions(node, is_nested)

    # Traverse the AST
    for node in ast['body']:
        if (node['type'] == 'ExpressionStatement' and
                node['expression']['type'] == 'CallExpression' and
                node['expression']['callee']['type'] == 'MemberExpression' and
                node['expression']['callee']['property']['name'] == 'addEventListener' and
                node['expression']['arguments'][0]['value'] == 'DOMContentLoaded'):
            has_dom_content_loaded = True
            # Process as top level before exploring nested content
            add_functions(node, is_nested=False)
            callback_body = node['expression']['arguments'][1]['body']['body']
            for nested_node in callback_body:
                process_node(nested_node, is_nested=True)
        else:
            process_node(node, is_nested=False)

    # Compile results, including callbacks and arrow functions in the output
    return {
        "variables": top_level_variables + (nested_variables if has_dom_content_loaded else []),
        "functions": top_level_functions + (nested_functions if has_dom_content_loaded else []),
        "callbacks": list(callbacks),  # Convert set to list
        "arrow_functions": arrow_functions,
    }


def parse_required_modules(ast):
    required_modules = {}
    stack = [ast]  # Initialize stack with the root AST node

    while stack:
        node = stack.pop()  # Get the next node to process

        # Check if this node is a variable declaration with a require call
        if node.get('type') == 'VariableDeclaration':
            for declarator in node.get('declarations', []):
                init = declarator.get('init', {})
                if init.get('type') == 'CallExpression' and init.get('callee', {}).get('name') == 'require':
                    var_name = declarator.get('id', {}).get('name')
                    module_name = init.get('arguments', [{}])[0].get('value')
                    required_modules[var_name] = module_name

        # Add child nodes to the stack to continue the traversal
        for key, value in node.items():
            if isinstance(value, dict):  # If the value is a dict, it's a single node
                stack.append(value)
            elif isinstance(value, list):  # If it's a list, extend the stack with all dict elements
                stack.extend([item for item in value if isinstance(item, dict)])

    return required_modules


def find_first_function(code):
    # Initialize variables to store the function's parts
    parameters = ""
    body = ""
    function_name = ""

    lines = code.split('\n')  # Split the code into lines

    function_found = False
    brace_counter = 0

    for i, line in enumerate(lines):
        trimmed_line = line.strip()
        # Check for function declaration
        if "function" in trimmed_line and "(" in trimmed_line and "{" in trimmed_line or \
                "async" in trimmed_line and "(" in trimmed_line and "{" in trimmed_line:
            function_signature = trimmed_line[:trimmed_line.index('{')].strip()
            is_async = "async " in function_signature
            function_split = function_signature.split(" ")
            function_index = 1 if not is_async else 2
            function_name = function_split[function_index].split("(")[0]  # Extract function name

            # Check if the function name was successfully extracted
            if function_name:
                function_found = True
                parameters = trimmed_line.split('(')[1].split(')')[0]
                async_prefix = "async " if is_async else ""
                body = f"{async_prefix}function {function_name}({parameters}) " + "{\n"
                brace_counter += 1
                continue
        if function_found:
            if brace_counter > 0:
                body += line + '\n'
            brace_counter += line.count('{') - line.count('}')
            if brace_counter == 0:
                break

    if not function_found:
        return "Function not found"
    else:
        return body.strip()


def extract_function(js_code, function_start_line):
    lines = js_code.split('\n')
    start_index = None
    for i, line in enumerate(lines):
        if line.strip().startswith(function_start_line):
            start_index = i
            break

    if start_index is None:
        return None

    bracket_count = 0
    function_lines = []
    for line in lines[start_index:]:
        function_lines.append(line)
        bracket_count += line.count('{')
        bracket_count -= line.count('}')
        if bracket_count == 0:
            break  # Closing bracket found

    return '\n'.join(function_lines)


def find_function_by_name(code, function_name):
    # Initialize variables to store the function's parameters and body
    parameters = ""
    body = ""

    # Split the code by lines
    lines = code.split('\n')

    # Initialize a flag to indicate whether the function has been found
    function_found = False

    # Initialize a counter to keep track of the curly braces
    brace_counter = 0

    for i, line in enumerate(lines):
        trimmed_line = line.strip()
        # Improved check for the function declaration to include async functions
        if function_name in trimmed_line and "function" in trimmed_line and "(" in trimmed_line and "{" in trimmed_line or \
                "async" in trimmed_line and function_name in trimmed_line and "(" in trimmed_line and "{" in trimmed_line:
            function_signature = trimmed_line[:trimmed_line.index('{')].strip()
            # Check if the function name exactly matches what we're looking for, including async functions
            is_async = "async " in function_signature
            function_split = function_signature.split(" ")
            function_index = 1 if not is_async else 2
            if (is_async or function_signature.startswith("function")) and function_name == \
                    function_split[function_index].split("(")[0]:
                function_found = True
                parameters = trimmed_line.split('(')[1].split(')')[0]
                async_prefix = "async " if is_async else ""
                body = f"{async_prefix}function {function_name}({parameters}) " + "{\n"
                brace_counter += 1
                continue
        if function_found:
            # Record the body until the closing curly brace is found
            if brace_counter > 0:  # Adjust this condition to ensure it only appends body after the first brace
                body += line + '\n'
            brace_counter += line.count('{') - line.count('}')
            if brace_counter == 0:
                break

    if not function_found:
        return "Function not found"
    else:
        return body.strip()


def find_arrow_function_by_name(code, function_name):
    # Initialize variables to store the function's parameters and body
    parameters = ""
    body = ""
    async_prefix = ""
    function_found = False
    processing_body = False
    brace_counter = 0

    # Normalize the code to ensure consistent parsing
    code_lines = code.split('\n')
    for line in code_lines:
        stripped_line = line.strip()
        # Enhanced check to include async functions properly
        if "const " + function_name + " =" in stripped_line and "=>" in stripped_line:
            # Correctly determine if the function is async and adjust for its presence
            is_async = "= async (" in stripped_line or (
                    stripped_line.startswith("async") and function_name in stripped_line)
            async_prefix = "async " if is_async else ""

            # Handling for when the function definition starts (considering 'async ' length)
            function_definition_start = stripped_line.find("= ") + 2

            arrow_function_definition = stripped_line[function_definition_start:]

            # Split at the arrow to separate parameters from the body
            parts = arrow_function_definition.split('=>', 1)
            parameters = parts[0].strip().lstrip("async ").strip("()")
            body_part = parts[1].strip()

            if body_part.startswith('{'):
                # Handle multiline body beginning
                processing_body = True
                function_found = True
                brace_counter += body_part.count('{') - body_part.count('}')
                body += body_part[1:] + '\n' if brace_counter > 0 else body_part[1:-1]
            else:
                # Single-line body without braces
                function_found = True
                body = body_part
                break  # No further processing needed for single-line function
        elif function_found and processing_body:
            body += line + '\n'
            brace_counter += line.count('{') - line.count('}')
            if brace_counter == 0:
                body = body[:body.rfind('\n')].rstrip()  # Adjust for correct body end handling
                processing_body = False
                break

    if not function_found:
        return "Function not found"
    else:
        # Correctly handle the closure of the function body for multiline functions
        if processing_body and body.endswith('}'):
            body = body[:body.rfind('}')]
        # Ensure the async prefix is correctly included for async functions
        return f'const {function_name} = {async_prefix}({parameters}) => {{{body}'


def find_event_listeners_by_variable(code, variable_name):
    event_listeners = []

    # Split the code by lines
    lines = code.split('\n')

    # Flags to indicate when we are within an event listener block
    in_event_listener = False
    brace_count = 0
    event_listener_start = ""

    for line in lines:
        if f'{variable_name}.addEventListener(' in line and not in_event_listener:
            in_event_listener = True
            event_listener_start = line
            brace_count += line.count('{') - line.count('}')
            if brace_count == 0:  # Single line event listener
                event_listeners.append(event_listener_start)
                in_event_listener = False
            continue

        if in_event_listener:
            brace_count += line.count('{') - line.count('}')
            event_listener_start += '\n' + line
            if brace_count == 0:
                # We've reached the end of the event listener callback
                event_listeners.append(event_listener_start.strip())
                in_event_listener = False
                event_listener_start = ""

    if not event_listeners:
        return "Event listener not found"
    else:
        # Formatting the results
        formatted_output = "\n\n".join(event_listeners)
        return formatted_output


def find_express_app_variable(code):
    lines = code.split('\n')
    for line in lines:
        # Strip leading and trailing spaces from the line
        line = line.strip()
        # Looking for a line that assigns express() to a variable, considering various spacing
        if 'express()' in line and '=' in line:
            # Split the line at the '=' to isolate the variable name
            parts = line.split('=')
            if len(parts) > 1:
                # The variable name could be prefixed with 'const', 'let', or 'var', including spaces
                # We assume the variable name is the last word before the '='
                var_name = parts[0].strip().split()[-1]
                return var_name
    return None


def find_callback_bodies(code, variable_name):
    callbacks = []
    lines = code.split('\n')
    in_callback = False
    parenthesis_counter = 0
    current_callback = ""

    for line in lines:
        if f"{variable_name}." in line and "(" in line and not in_callback:
            in_callback = True
            parenthesis_counter += line.count('(') - line.count(')')
            current_callback += line + '\n'
            if parenthesis_counter == 0:
                callbacks.append(current_callback.strip())
                current_callback = ""
                in_callback = False
            continue

        if in_callback:
            parenthesis_counter += line.count('(') - line.count(')')
            current_callback += line + '\n'
            if parenthesis_counter == 0:
                callbacks.append(current_callback.strip())
                current_callback = ""
                in_callback = False

    return callbacks


def get_skeleton_method(code):
    lines = code.split('\n')
    if "=>" in lines[0] or "function" in lines[0]:
        return f'{lines[0]}\n\t\t//...\n{lines[-1]}'
    else:
        return None


def replace_function_bodies(code, definitions):
    # Replace normal functions
    for function_name in definitions['functions']:
        code = re.sub(r'(function\s+' + re.escape(function_name) + r'\s*\([^)]*\)\s*\{)[\s\S]*?(\})',
                      r'\1\n\t//...\n\2', code)

    # Replace arrow functions
    for function_name in definitions['arrow_functions']:
        code = re.sub(r'(const\s+' + re.escape(function_name) + r'\s*=\s*\([^)]*\)\s*=>\s*\{)[\s\S]*?(\};)',
                      r'\1\n\t//...\n\2', code)

    # Replace callbacks, assuming they are attached to variables directly
    for callback_name in definitions['callbacks']:
        pattern = re.escape(callback_name) + r'\.addEventListener\(\s*[\w\W]+?\s*\{'
        matches = re.findall(pattern, code, re.MULTILINE)
        for match in matches:
            start_pattern = re.escape(match)
            code = re.sub(start_pattern + r'[\s\S]*?(\}\);)', r'\1\n\t//...\n\2', code)

    return code


def count_event_listeners(js_code):
    # Regular expression to match both '.addEventListener' and '.removeEventListener'
    pattern = r'\.(add|remove)EventListener'
    # Find all occurrences of the pattern
    matches = re.findall(pattern, js_code)
    # Return the number of occurrences
    return len(matches)


def split_event_listeners(js_code, object_name):
    # Initialize an empty list to store the captured event listener strings
    event_listeners = []

    # Initialize a pointer to keep track of our position in the string
    index = 0

    # Loop through the code to find each event listener related to the specified object
    while index < len(js_code):
        # Find the next occurrence of the object name followed by '.addEventListener' or '.removeEventListener'
        event_listener_start = js_code.find(f'{object_name}.add', index)
        if event_listener_start == -1:
            event_listener_start = js_code.find(f'{object_name}.remove', index)
            if event_listener_start == -1:
                # If no more event listeners are found, break out of the loop
                break

        # Find the opening parenthesis of the event listener declaration
        start_parenthesis = js_code.find('(', event_listener_start)

        # Initialize counters for parentheses to identify the end of the event listener block
        open_parens = 1
        index = start_parenthesis + 1

        # Loop through the code starting after the opening parenthesis to find the matching closing parenthesis
        while index < len(js_code) and open_parens > 0:
            if js_code[index] == '(':
                open_parens += 1
            elif js_code[index] == ')':
                open_parens -= 1
            index += 1

        # Once the matching closing parenthesis is found, extract the event listener block
        if open_parens == 0:
            event_listener_block = js_code[event_listener_start:index]
            event_listeners.append(event_listener_block)

    return event_listeners


def replace_function_in_code(original_code, function_first_line, new_function_code):
    function_first_line = function_first_line.split("\n")[0]
    lines = original_code.split('\n')

    start_index = None
    open_braces = 0
    for i, line in enumerate(lines):
        # Find the start of the function to be replaced
        if function_first_line in line:
            start_index = i
            break

    if start_index is None:
        return original_code  # Function not found, return original code

    # Find the end of the function by matching braces
    for i in range(start_index, len(lines)):
        line = lines[i]
        open_braces += line.count('{')
        open_braces -= line.count('}')

        if open_braces == 0:
            end_index = i
            break
    else:
        # If we never hit 0 braces, something went wrong, return original
        return original_code

    # Replace the old function with the new function code
    new_code_lines = lines[:start_index] + new_function_code.split('\n') + lines[end_index + 1:]

    # Return the new code as a single string
    return '\n'.join(new_code_lines)


def compare_js_functions(js_code):
    functions = js_code.split("<|-|>")

    normalized_functions = [func.strip() for func in functions]

    first_function = normalized_functions[0]
    for func in normalized_functions[1:]:
        if func != first_function:
            return False
    return True


def extract_functions_file(list_files, function):
    function = function.split("\n")[0]
    functions_to_update = []
    for file in list_files:
        extracted = extract_function(file, function)
        functions_to_update.append(extracted)
    try:
        non_none_items = filter(None, functions_to_update)
        joined = "\n<|-|>\n".join(non_none_items)
    except:
        joined = None
    print(joined)
    return joined
