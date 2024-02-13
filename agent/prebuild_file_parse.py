import re


def escape_snippet(file_name,input_text):
    pattern = r"```(.*?)```"
    matches = re.findall(pattern, input_text, re.DOTALL)

    if matches:
        extracted_code = "```" + matches[0] + "```"
        extracted_code = extracted_code.replace("```", "")
        extracted_code = extracted_code.replace(file_name + ":", "")
    else:
        extracted_code = input_text.replace("```", "")
        extracted_code = extracted_code.replace(file_name + ":", "")

    return extracted_code

