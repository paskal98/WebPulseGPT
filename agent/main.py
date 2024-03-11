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
from agent.merge import MergeFile
from agent.modularity import Modularity, extract_file_paths, get_uncreated_files



API = os.environ['OPENAI_API_KEY']
project_id = str(uuid.uuid4().hex)


if __name__ == "__main__":
    # core = Core(API, project_id)
    # descr = None
    # dev_plan = None
    # impl = None
    #
    # try:
    #     print("START...\n\n")
    #     core.on_start()
    # except:
    #     print("Error on START")
    #
    # try:
    #     print("Description...\n\n")
    #     core.on_description()
    # except:
    #     print("Error on Description")
    #
    # try:
    #     print("Technologies...\n\n")
    #     core.on_technologies()
    # except:
    #     print("Error on Technologies")
    #
    # try:
    #     print("Tasks...\n\n")
    #     core.on_tasks()
    # except:
    #     print("Error on Tasks")
    #
    # try:
    #     print("Planing...\n\n")
    #     core.on_planing()
    # except:
    #     print("Error on Planing")
    #
    # try:
    #     print("Project Structure...\n\n")
    #     core.on_project_structure()
    # except:
    #     print("Error on Project Structure")
    #
    # try:
    #     print("Implementing Tasks..\n\n")
    #     core.on_developing_tasks()
    # except:
    #     print("Error on Implementing Tasks")
    #
    # try:
    #     print("Merge Files...\n\n")
    #     core.on_merge_files()
    # except:
    #     print("Error on Merge Files")
    #
    # try:
    #     print("Project Description Tasks Impl Summary..\n\n")
    #     descr, dev_plan, impl = core.save_project_impl()
    # except:
    #     print("Error Project Description Tasks Impl Summary")



    modularity = Modularity("bf116e84f80242449c53d083610949a4", OpenAI(api_key=API),API)
    print("Project Modularity Init...\n\n")
    modularity.init_module()
    modularity.project_structure()
    modularity.project_builder_init()


    try:
        print("Project Issues...\n\n")
        modularity.project_summary()
    except:
        print("Error Project Issues")

    try:
        print("Project Issues Solution...\n\n")
        modularity.project_issue_solution()
        modularity.project_builder_init()
    except:
        print("Error Project Issues Solution")

    while True:
        try:
            print("\n Write update that should be applied:\n")
            update = input()
            modularity.set_project_path("nen.txt")

            modularity.init_module()
            modularity.project_structure()
            modularity.project_user_updates(update)
            modularity.project_issue_solution()
            modularity.project_builder_init()
        except:
            print("Failed")

    # merge = MergeFile([{"script.js": code1}, {"script.js": code2}], OpenAI(api_key=API), "aaaaaaaaaa")
    #
    #
    # print(merge.merge_files(type="client")[0]["script.js"])






