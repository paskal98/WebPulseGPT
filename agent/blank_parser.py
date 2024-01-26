import re


def parse(type_and_number):
    data_dict = {}

    pattern = r'([A-Z]+\d+):\s(.+)'

    with open("blanks/user_story.blank", "r") as file:
        text = file.read()

    matches = re.findall(pattern, text)

    for match in matches:
        label, value = match
        data_dict[label] = value

    return data_dict[type_and_number.upper()]



