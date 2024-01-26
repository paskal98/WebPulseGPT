import re


def parse_tasks(text):
    # Regex pattern to match each task and its details
    pattern = r"Task (\d+):\s+Description: (.*?)\s+Programmatic Goal: (.*?)\s+User-Review Goal: (.*?)\s*(?=Task \d+:|$)"

    tasks = {}
    for match in re.finditer(pattern, text, re.DOTALL):
        task_number, description, programmatic_goal, user_review_goal = match.groups()
        tasks[task_number] = {
            'Description': description.strip(),
            'Programmatic Goal': programmatic_goal.strip(),
            'User-Review Goal': user_review_goal.strip()
        }


    return tasks


