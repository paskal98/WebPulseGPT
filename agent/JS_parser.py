import json
import re

import requests


def parse_code_with_esprima_server(code):
    url = 'http://localhost:3000/parse'
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


def parse_ast_conditionally_old(ast):
    has_dom_content_loaded = False
    top_level_variables = []
    top_level_functions = []
    nested_variables = []
    nested_functions = []

    def add_variables(declarations, is_nested):
        for decl in declarations:
            var_name = decl['id']['name']
            if is_nested:
                nested_variables.append(var_name)
            else:
                top_level_variables.append(var_name)

    def add_functions(node, is_nested):
        func_name = ''
        if node['type'] == 'FunctionDeclaration':
            func_name = node['id']['name']
        elif node['type'] == 'ExpressionStatement' and node['expression']['type'] == 'CallExpression':
            callee = node['expression']['callee']
            if callee['type'] == 'MemberExpression' and callee['property']['name'] == 'addEventListener':
                event_type = node['expression']['arguments'][0]['value']
                func_name = f"{callee['object']['name']}.addEventListener(\"{event_type}\""

        if func_name:
            if is_nested:
                nested_functions.append(func_name)
            else:
                top_level_functions.append(func_name)

    def process_node(node, is_nested):
        if node['type'] == 'VariableDeclaration':
            add_variables(node['declarations'], is_nested)
        elif node['type'] in ['FunctionDeclaration', 'ExpressionStatement']:
            add_functions(node, is_nested)

    for node in ast['body']:
        if (node['type'] == 'ExpressionStatement' and
                node['expression']['type'] == 'CallExpression' and
                node['expression']['callee']['type'] == 'MemberExpression' and
                node['expression']['callee']['property']['name'] == 'addEventListener' and
                node['expression']['arguments'][0]['value'] == 'DOMContentLoaded'):
            has_dom_content_loaded = True
            # Add DOMContentLoaded as a top level function before processing nested content
            add_functions(node, is_nested=False)
            # Process the nested content within the DOMContentLoaded listener
            callback_body = node['expression']['arguments'][1]['body']['body']
            for nested_node in callback_body:
                process_node(nested_node, is_nested=True)
        else:
            process_node(node, is_nested=False)

    return {
        "variables": top_level_variables + (nested_variables if has_dom_content_loaded else []),
        "functions": top_level_functions + (nested_functions if has_dom_content_loaded else []),
    }


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


def find_callbacks(ast):
    callbacks = []

    def is_callback_function(node):
        # Check if the node is a dict and represents a function, which could be a callback
        return isinstance(node, dict) and node.get('type') in ['FunctionExpression', 'ArrowFunctionExpression']

    def traverse(node, path=[]):
        # Enhanced traversal of the AST, ensuring node is a dictionary before using .get()
        if isinstance(node, dict):
            for key, value in node.items():
                if is_callback_function(value):
                    # Capture the path to this callback as a string representation
                    callback_path = "->".join(path + [key])
                    callbacks.append(callback_path)
                else:
                    # Recursively traverse if value is a dict or list, without assuming .get() is available
                    traverse(value, path + [key])
        elif isinstance(node, list):
            for index, item in enumerate(node):
                if is_callback_function(item):
                    # Capture the path to this callback, including its position in a list
                    callback_path = "->".join(path + [str(index)])
                    callbacks.append(callback_path)
                else:
                    traverse(item, path + [str(index)])

    traverse(ast)

    return callbacks

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
        # Improved check for the function declaration
        if function_name in trimmed_line and "function" in trimmed_line and "(" in trimmed_line and "{" in trimmed_line:
            function_signature = trimmed_line[:trimmed_line.index('{')].strip()
            # Check if the function name exactly matches what we're looking for
            if function_signature.startswith("function") and function_name == \
                    function_signature.split(" ")[1].split("(")[0]:
                function_found = True
                parameters = trimmed_line.split('(')[1].split(')')[0]
                body += trimmed_line[trimmed_line.index('{'):].strip() + '\n'
                brace_counter += 1
                continue
        if function_found:
            # Record the body until the closing curly brace is found
            body += line + '\n'
            brace_counter += line.count('{') - line.count('}')
            if brace_counter == 0:
                break

    parameters = parameters.strip()
    body = body.strip()

    if not function_found:
        return "Function not found"
    else:
        return f'"{function_name}": "({parameters}) \n{body}\n"'


def find_arrow_function_by_name(code, function_name):
    # Initialize variables to store the function's parameters and body
    parameters = ""
    body = ""
    function_found = False
    processing_body = False
    brace_counter = 0

    # Normalize the code to ensure consistent parsing
    code_lines = code.split('\n')
    for line in code_lines:
        stripped_line = line.strip()
        if f"const {function_name} =" in stripped_line and "=>" in stripped_line and not function_found:
            function_found = True
            # Extract parameters
            parts = stripped_line.split('=>', 1)
            parameters_part = parts[0].split('=')[1].strip()
            parameters = parameters_part.strip("()")

            body_part = parts[1].strip()
            if body_part.startswith('{'):
                # Handle potentially multiline body starting on the same line
                processing_body = True
                brace_counter += body_part.count('{') - body_part.count('}')
                if brace_counter > 0:
                    body += body_part[1:] + '\n'  # Remove the opening brace for consistency in output
                else:
                    body = body_part[1:-1]  # Single-line function body
                    break
            else:
                # Single-line arrow function without braces
                body = body_part
                break
        elif function_found and processing_body:
            # Accumulate body lines for multiline arrow functions
            body += line + '\n'
            brace_counter += line.count('{') - line.count('}')
            if brace_counter == 0:
                # Once all braces are closed, remove the last line's newline and trailing brace
                body = body.rstrip()  # Remove trailing whitespace and newline
                processing_body = False
                break

    if not function_found:
        return "Function not found"
    else:
        # Correcting the body's ending in case of multiline functions
        if body.endswith('}'):
            body = body[:body.rfind('}')]  # Corrected to use 'rfind' to remove the last closing brace
        # Formatting the output
        return f'"{function_name}": ({parameters}) => {{\n{body}\n}}'


def find_event_listeners_by_variable(code, variable_name):
    event_listeners = []

    # Split the code by lines
    lines = code.split('\n')

    # Flags to indicate when we are within an event listener block
    in_event_listener = False
    brace_count = 0
    current_listener = {'event_type': '', 'body': ''}

    for line in lines:
        if f'{variable_name}.addEventListener(' in line:
            in_event_listener = True
            # Extract the event type from the line
            event_type_start = line.find('("') + 2
            event_type_end = line.find('",', event_type_start)
            event_type = line[event_type_start:event_type_end]
            current_listener['event_type'] = event_type
            # Find the start of the callback function
            function_start = line.find('function', event_type_end)
            if function_start != -1:
                brace_count += line.count('{') - line.count('}')
                current_listener['body'] += line[function_start:] + '\n'
            continue

        if in_event_listener:
            brace_count += line.count('{') - line.count('}')
            current_listener['body'] += line + '\n'
            if brace_count == 0:
                # We've reached the end of the event listener callback
                in_event_listener = False
                # Cleanup the captured body
                body_cleaned = current_listener['body'].strip()
                if body_cleaned.endswith('}'):
                    body_cleaned = body_cleaned[:body_cleaned.rfind('}')]
                current_listener['body'] = body_cleaned
                event_listeners.append(current_listener)
                current_listener = {'event_type': '', 'body': ''}

    if not event_listeners:
        return "Event listener not found"
    else:
        # Formatting the results
        formatted_output = ""
        for listener in event_listeners:
            formatted_output += f'Event Type: {listener["event_type"]}, Callback Function: {{\n{listener["body"]}\n}}\n\n'
        return formatted_output.strip()
