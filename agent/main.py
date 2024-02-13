import os
import re

from openai import OpenAI

from agent.core import Core
from agent.implemented_parser import  parse_file_contents

core = Core()


if __name__ == "__main__":
    print("START...\n\n")
    core.on_start()

    print("Description...\n\n")
    core.on_description()

    print("Technologies...\n\n")
    core.on_technologies()

    print("Tasks...\n\n")
    core.on_tasks()

    print("Planing...\n\n")
    core.on_planing()

    print("Project Structure...\n\n")
    core.on_project_structure()

    print("Implementing Tasks..\n\n")
    core.on_developing_tasks()

    print("Merge...\n\n")
    core.on_merge_updates()

    print("Summary...\n\n")
    core.on_summary()

    print("Generate Build File (build.sh)...\n\n")
    core.generate_bash()


