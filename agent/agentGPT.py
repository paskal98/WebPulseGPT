import os
import re
import uuid
from pathlib import Path

from openai import OpenAI

from agent.core import Core
from agent.modularity import Modularity, extract_file_paths, get_uncreated_files


class Agent:
    def __init__(self, API, name, description):
        self.agentpath = os.getcwd() + "/agent"
        self.API = API
        self.project_id = str(uuid.uuid4().hex)
        self.modularity = Modularity(self.project_id, OpenAI(api_key=self.API),self.API,self.agentpath )
        self.name = name
        self.description = description


    def get_project_id(self):
        return self.project_id

    def set_project_id(self, project_id):
        self.project_id = project_id
        self.modularity = Modularity(self.project_id, OpenAI(api_key=self.API), self.API, self.agentpath)

    def update_project_summary(self, content):
        project_path = f'output/projects/{self.project_id}/project_summary.txt'
        path = Path(project_path)

        if path.exists():
            path.unlink()

        path.write_text(content)

    def remove_project_dir(self):
        project_dir = f'output/projects/{self.project_id}'
        project_emb_dir = f'output/projects_embeddings/{self.project_id}'

        paths = [project_dir,project_emb_dir]

        for path in paths:
            if os.path.exists(path):
                os.rmdir(path)

    def agent_start_impl(self):
        core = Core(self.API, self.project_id, self.agentpath)
        descr = None
        dev_plan = None
        impl = None

        try:
            print("START...\n\n")
            core.on_start(self.name)
        except:
            self.remove_project_dir()
            return "Error on START"

        try:
            print("Description...\n\n")
            core.on_description(self.description)
        except:
            self.remove_project_dir()
            return "Error on Description"

        try:
            print("Technologies...\n\n")
            core.on_technologies()
        except:
            self.remove_project_dir()
            return "Error on Technologies"

        try:
            print("Tasks...\n\n")
            core.on_tasks()
        except:
            self.remove_project_dir()
            return "Error on Tasks"

        try:
            print("Planing...\n\n")
            core.on_planing()
        except:
            self.remove_project_dir()
            return "Error on Planing"

        try:
            print("Project Structure...\n\n")
            core.on_project_structure()
        except:
            self.remove_project_dir()
            return "Error on Project Structure"

        try:
            print("Implementing Tasks..\n\n")
            core.on_developing_tasks()
        except:
            self.remove_project_dir()
            return "Error on Implementing Tasks"

        try:
            print("Merge Files...\n\n")
            core.on_merge_files()
        except:
            self.remove_project_dir()
            return "Error on Merge Files"

        try:
            print("Project Description Tasks Impl Summary..\n\n")
            descr, dev_plan, impl = core.save_project_impl()
        except:
            self.remove_project_dir()
            return "Error Project Description Tasks Impl Summary"

        return self.modularity_check()

    def modularity_check(self):
        print("Project Modularity Init...\n\n")
        self.modularity.init_module()
        self.modularity.project_structure()
        self.modularity.project_builder_init()

        try:
            print("Project Issues...\n\n")
            self.modularity.project_summary()
        except:
            return "Error Project Issues"

        try:
            print("Project Issues Solution...\n\n")
            self.modularity.project_issue_solution()
            self.modularity.project_builder_init()
        except:
            return "Error Project Issues Solution"

        return 'OK'

    def on_users_update(self, user_issue):
        project_path = f'output/projects/{self.project_id}/project_summary.txt'
        try:
            self.modularity.set_project_path(project_path)
            self.modularity.init_module()
            self.modularity.project_structure()
            self.modularity.project_user_updates(user_issue)
            self.modularity.project_issue_solution()
            self.modularity.project_builder_init()
        except:
            return "Failed"

        return 'OK'
