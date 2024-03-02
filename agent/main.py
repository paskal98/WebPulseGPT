import os
import re
import uuid

import requests
from openai import OpenAI

from agent.JS_parser import parse_ast_conditionally, find_function_by_name, \
    find_arrow_function_by_name, find_event_listeners_by_variable, get_ast_request, \
    parse_required_modules, find_callback_bodies, find_express_app_variable, get_skeleton_method, count_event_listeners, \
    split_event_listeners, extract_function
from agent.core import Core
from agent.implemented_parser import parse_file_contents
from agent.modularity import Modularity, extract_file_paths, get_uncreated_files

API = os.environ['OPENAI_API_KEY']
project_id = str(uuid.uuid4().hex)


if __name__ == "__main__":
    # core = Core(API, project_id)
    #
    # print("START...\n\n")
    # core.on_start()
    #
    # print("Description...\n\n")
    # core.on_description()
    #
    # print("Technologies...\n\n")
    # core.on_technologies()
    #
    # print("Tasks...\n\n")
    # core.on_tasks()
    #
    # print("Planing...\n\n")
    # core.on_planing()
    #
    # print("Project Structure...\n\n")
    # core.on_project_structure()
    #
    # print("Implementing Tasks..\n\n")
    # core.on_developing_tasks()
    #
    # print("Merge Files...\n\n")
    # core.on_merge_files()
    #
    # print("Generate Build File (build.sh)...\n\n")
    # core.generate_bash()
    #
    # core.save_project_impl()

    modularity = Modularity("4d2da4e256f14efabe16689fb6144e22", OpenAI(api_key=API))
    modularity.init_module()
    modularity.project_structure()
    modularity.project_summary()



    modularity.project_issue_solution()



    # print("Modularity Files HTML JS...\n\n")
    # core.on_modularity_html_js()
    #
    # print("Modularity...\n\n")
    # core.on_check_modularity()
    #
    # print("Summary...\n\n")
    # core.on_summary()



