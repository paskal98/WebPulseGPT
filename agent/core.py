import msvcrt
import uuid

from openai import OpenAI

from agent.blank_parser import parse
from agent.plan_parser import parse_development_plan, parse_development_plan_v2
from agent.tasks_parser import parse_tasks

client = OpenAI(api_key="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")

session_id = str(uuid.uuid4())


class Core:
    def __init__(self):
        self.implemented_project = []
        self.structure = None
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
        self.project_name = input()

    def on_description(self):
        print("|AI| -> " + parse("b2"))
        # self.project_descr = input()

        with open("blanks/user_project_details.blank", "r") as file:
            project_details = file.read().strip()
        self.project_descr = project_details

    def on_technologies(self):
        with open("prompts/technologies.prompt", "r") as file:
            tech_prompt = file.read().strip()

        final_prompt = tech_prompt.replace('{{ name }}', self.project_name)
        final_prompt = final_prompt.replace('{{ project_details }}', self.project_descr)

        self.project_tech = self.ai_conversation(final_prompt).content
        print(self.project_tech)

    def on_tasks(self):
        with open("prompts/tech_lead.prompt", "r") as file:
            tech_lead_prompt = file.read().strip()

        project_tasks_raw = self.ai_conversation(tech_lead_prompt).content

        self.project_tasks = parse_tasks(project_tasks_raw)

        for task, details in self.project_tasks.items():
            print(f"Task {task}:")
            for key, value in details.items():
                print(f"{key}: {value}")
            print()
        print("\n\n")

    def on_planing(self):
        self.conversation_history_roles = []
        with open("prompts/plan.prompt", "r") as file:
            plan_prompt = file.read().strip()

        tasks_formatted = ""
        for task_number, details in self.project_tasks.items():
            tasks_formatted += f"Task {task_number}:\n"
            tasks_formatted += f"Description: {details['Description']}\n"
            tasks_formatted += f"Programmatic Goal: {details['Programmatic Goal']}\n"
            tasks_formatted += f"User-Review Goal: {details['User-Review Goal']}\n\n"

        final_content = plan_prompt.replace("{{ name }}", self.project_name) \
            .replace("{{ project_details }}", self.project_descr) \
            .replace("{{ project_tech }}", self.project_tech) \
            .replace("{{ project_tasks }}", tasks_formatted)

        self.conversation_history_roles.append({"role": "user", "content": final_content})
        plan = self.ai_conversation(None, 'role').content
        print("PLAN")
        print(plan)
        print("\n\n\n")

        self.development_plan = parse_development_plan_v2(plan)
        # print(self.development_plan)
        # print("\n\n\n")

    def on_project_structure(self):
        self.conversation_history_roles = []
        with open("prompts/tree_structure.prompt", "r") as file:
            tree_structure = file.read().strip()

        tasks_formatted = ""
        for category, tasks in self.development_plan.items():
            tasks_formatted += f"{category}:\n"
            for task_number, task_description in tasks.items():
                tasks_formatted += f"- Task {task_number}: {task_description}\n"
            tasks_formatted += "\n"

        final_content = tree_structure.replace("{{ project_details }}", self.project_descr) \
            .replace("{{ project_plan }}", tasks_formatted.strip())

        self.conversation_history_roles.append({"role": "user", "content": final_content})
        self.structure = self.ai_conversation(None, 'role').content

        print("Structure")
        print(self.structure)
        print("\n\n\n")

    def on_developing_tasks(self):

        self.conversation_history_roles = []
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

                if 'Project Setup' in phase:
                    request += ("\nWrite only command to execute, without comments and other highlights. I need only "
                                "commands")

                self.conversation_history_roles.append({"role": "user", "content": request})
                self.implemented_tasks = self.ai_conversation(None, 'role').content
                print("Now is " + request)
                print(self.implemented_tasks)
                print("\n\n\n")

                # input("Press Enter to continue to the next task...")
                # print("Key pressed, continuing to next task...")

                request = ''

            if "Front" in phase or "Back" in phase or "Database" in phase or "Features" in phase:
                self.implemented_project.append(self.ai_conversation(extract, 'extract').content)
                extracted_content = "\n".join(self.implemented_project)
                self.conversation_history_roles = []
                self.conversation_history_roles.append({"role": "system",
                                                        "content": final_content + "\n Code that have already implemented. Based on this code add or update implementation\n" +
                                                                   extracted_content})
                print("\nExtracted\n ")
                print(extracted_content)

        extracted_content = "\n".join(self.implemented_project)
        print("\nPROJECT RAW\n ")
        print(extracted_content)


    def on_summary(self):
        self.conversation_history_roles = []
        with open("prompts/summary.prompt", "r") as file:
            summary = file.read().strip()

        tasks_formatted = ""
        for category, tasks in self.development_plan.items():
            tasks_formatted += f"{category}:\n"
            for task_number, task_description in tasks.items():
                tasks_formatted += f"- Task {task_number}: {task_description}\n"
            tasks_formatted += "\n"

        implemented = "\n".join(self.implemented_project)
        final_content =(summary.replace("{{ project_details }}", self.project_descr)
                        .replace("{{ project_plan }}",tasks_formatted)
                        .replace("{{ implemented project }}",implemented))


        self.conversation_history_roles.append({"role": "user", "content": final_content})
        project_reviewed = self.ai_conversation(None, 'role').content

        print("\nREVIEW\n ")
        print(project_reviewed)

        with open('output/project_implemented_raw.txt', 'w') as file:
            file.write(implemented)

        with open('output/project_reviewed.txt', 'w') as file:
            file.write(project_reviewed)

    def generate_bash(self):
        self.conversation_history_roles = []

        with open("prompts/generate_bash_v2.prompt", "r") as file:
            generate_bash_prompt = file.read().strip()

        with open("prompts/tree_structure_after.prompt", "r") as file:
            tree_structure_after = file.read().strip()

        implemented = "\n".join(self.implemented_project)
        final_content = (tree_structure_after.replace("{{ implemented project }}", implemented))

        self.conversation_history_roles.append({"role": "user", "content": final_content})
        tree_structure = self.ai_conversation(None, 'role').content

        self.conversation_history_roles.append({"role": "user", "content": generate_bash_prompt})
        generated_bash = self.ai_conversation(None, 'role').content

        print("\nTREE STRUCTURE\n ")
        print(tree_structure)

        print("\nBASH\n ")
        print(generated_bash)

        with open('output/tree_structure.txt', 'w') as file:
            file.write(tree_structure)

        with open('output/generated_bash.txt', 'w') as file:
            file.write(generated_bash)
