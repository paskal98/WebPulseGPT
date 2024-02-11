import re


def parse_file_contents(text):
    # General pattern to identify code blocks and extract contents
    code_block_pattern = re.compile(r"```(html|css|javascript)\n([\s\S]+?)\n```", re.MULTILINE)

    # Updated patterns to identify file names with directory paths within the content
    file_name_patterns = [
        re.compile(r"<!--\s*([\w./]+)\s*-->", re.MULTILINE),  # HTML comments for files with directories
        re.compile(r"/\*\s*([\w./]+)\s*\*/", re.MULTILINE),  # CSS comments for files with directories
        re.compile(r"//\s*([\w./]+)", re.MULTILINE)  # JavaScript comments for files with directories
    ]

    files_dict = {}

    code_blocks = code_block_pattern.finditer(text)
    for block in code_blocks:
        content = block.group(2).strip()
        file_name = None

        # Try to extract the file name using each pattern
        for fn_pattern in file_name_patterns:
            fn_match = fn_pattern.search(content)
            if fn_match:
                file_name = fn_match.group(1)
                break

        # If a file name is found, add it to the dictionary
        if file_name:
            # Handle potential duplicates by appending content if the filename already exists
            if file_name in files_dict:
                files_dict[file_name] += "\n\n" + content
            else:
                files_dict[file_name] = content

    return files_dict