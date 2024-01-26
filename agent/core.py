import uuid

from openai import OpenAI

from agent.blank_parser import parse
from tasks_parser import parse_tasks

client = OpenAI(api_key="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")

session_id = str(uuid.uuid4())

class Core:
    def __init__(self):
        self.implemented_tasks = None
        self.project_tech = None
        self.project_name = None
        self.project_descr= None
        self.project_tasks = None
        self.conversation_history = []
        self.conversation_history_roles = []
        self.full_stack_acting = None


    def print_history(self):
        for text in self.conversation_history:
            print(text)


    def aiConversation(self, request=None, type='user'):

        conversation = None
        if type == 'user':
            self.conversation_history.append({"role": "user", "content": request})
            conversation = self.conversation_history
        elif type == 'role':
            conversation = self.conversation_history_roles

        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=conversation,
            user=session_id
        )

        ai_response = completion.choices[0].message
        self.conversation_history.append({"role": "system", "content": ai_response.content})

        return ai_response

    def onStart(self):
        print("|AI| -> "+parse("b1"))
        self.project_name = input()

    def onDescription(self):
        print("|AI| -> "+parse("b2"))
        self.project_descr = input()

    def onTechnologies(self):
        with open("prompts/technologies.prompt", "r") as file:
            tech_prompt = file.read().strip()

        final_prompt = tech_prompt.replace('{{ name }}', self.project_name)
        final_prompt = final_prompt.replace('{{ project_details }}', self.project_descr)

        self.project_tech = self.aiConversation(final_prompt).content


    def onTasks(self):
        with open("prompts/tech_lead.prompt", "r") as file:
            tech_lead_prompt = file.read().strip()

        project_tasks_raw = self.aiConversation(tech_lead_prompt).content

        self.project_tasks = parse_tasks(project_tasks_raw)

        for task, details in self.project_tasks.items():
            print(f"Task {task}:")
            for key, value in details.items():
                print(f"{key}: {value}")
            print()


    def onDevelopingTasks(self):
        with open("prompts/full_stack_developer.prompt", "r") as file:
            full_stack_prompt = file.read().strip()

        self.conversation_history_roles.append({"role": "system", "content": full_stack_prompt})

        for task, details in self.project_tasks.items():
            request = f"Task: {task}\n"
            self.conversation_history_roles = []

            for key, value in details.items():
                request = request + f"{key}: {value}"

            self.conversation_history_roles.append({"role": "user", "content": request})
            self.implemented_tasks = self.aiConversation(None, 'role').content
            print(self.implemented_tasks)
            print("\n\n\n")





    def generateBash(self):


        output = self.aiConversation("create me terminal command to execute this steps as shell file. Always write me only code of shell file, other information remove from your response").content
        print(output)


