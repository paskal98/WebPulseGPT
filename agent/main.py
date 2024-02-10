import os

from openai import OpenAI

from agent.core import Core

core = Core()



if __name__ == "__main__":
    core.on_start()
    core.on_description()
    core.on_technologies()
    core.on_tasks()
    core.on_planing()
    core.on_project_structure()
    core.on_developing_tasks()
    core.on_summary()
    core.generate_bash()
