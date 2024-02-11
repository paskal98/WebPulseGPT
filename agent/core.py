import msvcrt
import uuid

from openai import OpenAI

from agent.blank_parser import parse
from agent.consilidate_dict import consolidate_duplicates
from agent.implemented_parser import parse_file_contents
from agent.plan_parser import parse_development_plan, parse_development_plan_v2
from agent.tasks_parser import parse_tasks

client = OpenAI(api_key="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")

session_id = str(uuid.uuid4())


def phase_project_setup(request):
    with open("prompts/project_setup.prompt", "r") as file:
        project_setup = file.read().strip()
    request += "\n" + project_setup
    return request


def contains_only_letters(text):
    special_symbols = set("{};<>=>")

    for char in text:
        if char in special_symbols:
            return False
        elif not char.isalpha():
            return False
    return True


class Core:
    def __init__(self):
        self.merged_project = []
        self.project_files = []
        self.files = None
        self.implemented_project = []
        self.probably_structure = None
        self.development_plan = None
        self.implemented_tasks = None
        self.project_tech = None
        self.project_name = None
        self.project_descr = None
        self.project_tasks = None
        self.conversation_history = []
        self.conversation_history_roles = []
        self.full_stack_acting = None
        self.plan = None

    def print_history(self):
        for text in self.conversation_history:
            print(text)

    def print_tasks(self):
        for task, details in self.project_tasks.items():
            print(f"Task {task}:")
            for key, value in details.items():
                print(f"{key}: {value}")
            print()
        print("\n\n")

    def prepare_tasks_to_str(self):
        tasks_formatted = ""
        for task_number, details in self.project_tasks.items():
            tasks_formatted += f"Task {task_number}:\n"
            tasks_formatted += f"Description: {details['Description']}\n"
            tasks_formatted += f"Programmatic Goal: {details['Programmatic Goal']}\n"
            tasks_formatted += f"User-Review Goal: {details['User-Review Goal']}\n\n"
        return tasks_formatted

    def prepare_plan_to_str(self):
        tasks_formatted = ""
        for category, tasks in self.development_plan.items():
            tasks_formatted += f"{category}:\n"
            for task_number, task_description in tasks.items():
                tasks_formatted += f"- Task {task_number}: {task_description}\n"
            tasks_formatted += "\n"
        return tasks_formatted

    def clear_history_role(self):
        self.conversation_history_roles = []

    def ai_conversation(self, request=None, type='user'):

        conversation = None
        if type == 'user':
            self.conversation_history.append({"role": "user", "content": request})
            conversation = self.conversation_history
        elif type == 'role':
            conversation = self.conversation_history_roles
        elif type == 'extract':
            conversation = self.conversation_history_roles
            conversation.append({"role": "user", "content": request})

        completion = client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            messages=conversation,
            user=session_id,
            temperature=0.9
        )

        ai_response = completion.choices[0].message

        if type == 'user':
            self.conversation_history.append({"role": "system", "content": ai_response.content})
        elif type == 'role':
            self.conversation_history_roles.append({"role": "system", "content": ai_response.content})

        return ai_response

    def on_start(self):
        print("|AI| -> " + parse("b1"))
        # self.project_name = input()
        self.project_name = "ToDo"

    def on_description(self):
        print("|AI| -> " + parse("b2"))
        # self.project_descr = input()

        with open("blanks/user_project_details.blank", "r") as file:
            project_details = file.read().strip()
        self.project_descr = project_details

    def on_technologies(self):
        with open("prompts/technologies.prompt", "r") as file:
            tech_prompt = file.read().strip()

        final_prompt = (tech_prompt
                        .replace('{{ name }}', self.project_name)
                        .replace('{{ project_details }}', self.project_descr))

        self.project_tech = self.ai_conversation(final_prompt).content
        # print(self.project_tech)

    def on_tasks(self):
        with open("prompts/tech_lead.prompt", "r") as file:
            tech_lead_prompt = file.read().strip()

        project_tasks_raw = self.ai_conversation(tech_lead_prompt).content
        self.project_tasks = parse_tasks(project_tasks_raw)

        # self.print_tasks()

    def on_planing(self):
        self.clear_history_role()

        with open("prompts/plan.prompt", "r") as file:
            plan_prompt = file.read().strip()

        final_content = plan_prompt.replace("{{ name }}", self.project_name) \
            .replace("{{ project_details }}", self.project_descr) \
            .replace("{{ project_tech }}", self.project_tech) \
            .replace("{{ project_tasks }}", self.prepare_tasks_to_str())

        self.conversation_history_roles.append({"role": "user", "content": final_content})
        plan = self.ai_conversation(None, 'role').content
        self.development_plan = parse_development_plan_v2(plan)

        print("PLAN")
        print(plan)
        print("\n\n\n")

    def on_project_structure(self):
        self.clear_history_role()

        with open("prompts/tree_structure.prompt", "r") as file:
            tree_structure = file.read().strip()

        final_content = tree_structure.replace("{{ project_details }}", self.project_descr) \
            .replace("{{ project_plan }}", self.prepare_tasks_to_str().strip())

        self.conversation_history_roles.append({"role": "user", "content": final_content})
        self.probably_structure = self.ai_conversation(None, 'role').content

        print("Probably Structure")
        print(self.probably_structure)
        print("\n\n\n")

    # def on_developing_tasks(self):
    #     self.clear_history_role()
    #
    #     with open("prompts/full_stack_developer.prompt", "r") as file:
    #         full_stack_prompt = file.read().strip()
    #
    #     with open("prompts/extract.prompt", "r") as file:
    #         extract = file.read().strip()
    #
    #     final_content = full_stack_prompt.replace("{{ project_details }}", self.project_descr)
    #     self.conversation_history_roles.append({"role": "system", "content": final_content})
    #
    #     for phase, tasks in self.development_plan.items():
    #         request = f"Phase: {phase}\n"
    #
    #         for task_number, task_description in tasks.items():
    #             request += f"{task_number}: {task_description}\n"
    #
    #             if 'Project Setup' in phase:
    #                 request += ("\nWrite only command to execute, without comments and other highlights. I need only "
    #                             "commands")
    #
    #             self.conversation_history_roles.append({"role": "user", "content": request})
    #             self.implemented_tasks = self.ai_conversation(None, 'role').content
    #
    #             print("Now is " + request)
    #             print(self.implemented_tasks)
    #             print("\n\n\n")
    #
    #             # input("Press Enter to continue to the next task...")
    #             # print("Key pressed, continuing to next task...")
    #
    #             request = ''
    #
    #         if "Front" in phase or "Back" in phase or "Database" in phase or "Features" in phase:
    #             self.implemented_project.append(self.ai_conversation(extract, 'extract').content)
    #             extracted_content = "\n".join(self.implemented_project)
    #
    #             self.conversation_history_roles = []
    #             self.conversation_history_roles.append({"role": "system",
    #                                                     "content": final_content + "\n Code that have already implemented. Based on this code add or update implementation\n" +
    #                                                                extracted_content})
    #
    #     print("\nPROJECT RAW\n ")
    #     print("\n".join(self.implemented_project))

    def on_developing_tasks(self):
        self.clear_history_role()

        with open("prompts/full_stack_developer.prompt", "r") as file:
            full_stack_prompt = file.read().strip()

        with open("prompts/extract.prompt", "r") as file:
            extract = file.read().strip()

        final_content = full_stack_prompt.replace("{{ project_details }}", self.project_descr)
        self.conversation_history_roles.append({"role": "system", "content": final_content})

        for phase, tasks in self.development_plan.items():
            request = f"Phase: {phase}\n"

            for task_number, task_description in tasks.items():
                request += f"{task_number}: {task_description}\n"

                if 'Project' in phase:
                    request = phase_project_setup(request)

                self.conversation_history_roles.append({"role": "user", "content": request})
                self.implemented_tasks = self.ai_conversation(None, 'role').content

                # print("Now is " + request)
                # print(self.implemented_tasks)
                # print("\n\n\n")

                # input("Press Enter to continue to the next task...")
                # print("Key pressed, continuing to next task...")

                request = ''

                if "Front" in phase or "Back" in phase or "Database" in phase or "Features" in phase:
                    response = self.ai_conversation(extract, 'extract').content
                    self.implemented_project.append(response)
                    self.project_files.append(parse_file_contents(response))
                    print(response)

            if "Front" in phase or "Back" in phase or "Database" in phase or "Features" in phase:
                extracted_content = "\n".join(self.implemented_project)
                self.clear_history_role()
                self.conversation_history_roles.append({"role": "system",
                                                        "content": final_content + "\n Code that have already implemented. Based on this code add or update implementation\n" +
                                                                   extracted_content})

        consolidated_project_files = consolidate_duplicates(self.project_files)

        with open('output/project_files.txt', 'w') as file:

            for dictionary in self.project_files:
                for key, value in dictionary.items():
                    file.write(f"{key}: {value}\n\n")
                file.write("\n----------\n")

        with open('output/consolidated_project_files.txt', 'w') as file:
            for dictionary in consolidated_project_files:
                for key, value in dictionary.items():
                    file.write(f"{key}: {value}\n\n")
                file.write("\n----------\n")
            file.write("\n\n\n\n")
            for dictionary in consolidated_project_files:
                for key in dictionary.keys():
                    file.write("- " + key + "\n")

    def on_merge_updates(self):
        with open("prompts/merge.prompt", "r") as file:
            merge = file.read().strip()

        consolidated_project_files = consolidate_duplicates(self.project_files)

        for dictionary in consolidated_project_files:
            self.clear_history_role()
            for key, value in dictionary.items():
                file = f"{key}: {value}\n\n"
                self.conversation_history_roles.append({"role": "user", "content": merge + "\n" + file})
                response = self.ai_conversation(None, 'role').content

                if "IDENTICAL" in response:
                    merged_file = f"{value}\n\n"
                else:
                    merged_file = response

                self.merged_project.append({key: merged_file})

        with open('output/merged_project.txt', 'w') as file:
            for dictionary in self.merged_project:
                for key, value in dictionary.items():
                    file.write(f"{key}: {value}\n\n")
                file.write("\n----------\n")
            file.write("\n\n\n\n")

            for dictionary in self.merged_project:
                for key in dictionary.keys():
                    file.write("- " + key + "\n")

    def on_summary(self):
        self.clear_history_role()

        with open("prompts/summary.prompt", "r") as file:
            summary = file.read().strip()

        consolidated_project_files = consolidate_duplicates(self.project_files)

        implemented = ""
        for dictionary in consolidated_project_files:
            for key, value in dictionary.items():
                implemented += f"{key}: {value}\n\n"
            implemented += "\n----------\n"

        final_content = (summary.replace("{{ project_details }}", self.project_descr)
                         .replace("{{ project_plan }}", self.prepare_plan_to_str())
                         .replace("{{ implemented project }}", implemented))

        self.conversation_history_roles.append({"role": "user", "content": final_content})
        project_reviewed = self.ai_conversation(None, 'role').content

        with open('output/project_implemented_raw.txt', 'w') as file:
            file.write("\n<$$$>\n".join(self.implemented_project))

        with open('output/project_reviewed.txt', 'w') as file:
            file.write(project_reviewed)

        with open('output/final_content.txt', 'w') as file:
            file.write(final_content)

    def generate_bash(self):
        self.clear_history_role()

        with open("prompts/generate_bash_v2.prompt", "r") as file:
            generate_bash_prompt = file.read().strip()

        generated_bash = []
        for dictionary in self.merged_project:
            for key, value in dictionary.items():
                self.conversation_history_roles.append(
                    {"role": "user", "content": generate_bash_prompt + f"\n{key}: {value}\n"})
                generated_bash.append(self.ai_conversation(None, 'role').content)

        with open('output/generated_bash.txt', 'w') as file:
            for item in generated_bash:
                file.write(item)
                file.write("\n\n\n<<<--!!!-->>>\n\n\n")
