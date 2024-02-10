def parse_development_plan(text):

    plan_dict = {}
    current_section = None

    output_str = text.split('\n', 1)[-1].strip()

    for line in output_str.split('\n'):
        if line.endswith(':'):
            current_section = line[:-1]
            plan_dict[current_section] = {}
        elif line.strip().startswith('- Task'):
            task_number, task_description = line.strip().split(': ', 1)
            task_number = task_number[2:]
            if current_section is not None:
                plan_dict[current_section][task_number] = task_description

    return plan_dict


def parse_development_plan_v2(text):
    plan_dict = {}
    current_section = None

    for line in text.split('\n'):
        line = line.strip()
        if line.startswith('- Task'):
            task_number, task_description = line.split(': ', 1)
            task_number = task_number[2:]
            if current_section is not None:
                plan_dict[current_section][task_number] = task_description
        elif line and not line.startswith('- Task'):
            current_section = line.rstrip(':')
            plan_dict[current_section] = {}

    return plan_dict
