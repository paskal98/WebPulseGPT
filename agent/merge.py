from collections import defaultdict

from openai import OpenAI

from agent.JS_parser import get_ast_request, find_function_by_name, get_skeleton_method, find_arrow_function_by_name, \
    find_event_listeners_by_variable, count_event_listeners, split_event_listeners, parse_ast_conditionally


class MergeFile:
    def __init__(self, project_files, client):
        self.merged_files = []
        self.conversation = []
        self.project_files = project_files
        self.client = client

    def clear_conversation(self):
        self.conversation = []

    def get_keys(self):
        return {key for d in self.project_files for key in d.keys()}



    def ai_conversation(self):

        completion = self.client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            messages=self.conversation,
            temperature=0.9
        )
        ai_response = completion.choices[0].message.content
        return ai_response

    def merge_files(self):
        self.merge_js()

        with open("prompts/merge.prompt", "r") as file:
            merge = file.read().strip()

        all_keys = self.get_keys()
        print(all_keys)

        for key in all_keys:
            self.clear_conversation()
            self.conversation.append({"role": "system", "content": merge})

            versions = 0
            for dictionary in self.project_files:
                if key in dictionary:
                    file = f"```{key}: {dictionary[key]}```\n\n"
                    self.conversation.append({"role": "user", "content": file})
                    versions += 1

            if versions == 1:
                for dictionary in self.project_files:
                    if key in dictionary:
                        self.merged_files.append({key: dictionary[key]})
            else:
                result = self.ai_conversation()
                if "confirmed to be identical." in result or "Same" in result:

                    for dictionary in self.project_files:
                        if key in dictionary:
                            self.merged_files.append({key: dictionary[key]})
                else:
                    self.merged_files.append({key: result})

        with open('output/merged_files.txt', 'w', encoding="utf-8") as file:
            for dictionary in self.merged_files:
                for key, value in dictionary.items():
                    file.write(f"{key}: {value}\n\n")
                file.write("\n===========================================\n")
            file.write("\n\n\n\n")

            for dictionary in self.merged_files:
                for key in dictionary.keys():
                    file.write("- " + key + "\n")

        return self.merged_files

    def merge_js(self):
        key_counts = {}

        for dictionary in self.project_files:
            for key in dictionary.keys():
                if key.endswith('.js'):
                    if key in key_counts:
                        key_counts[key] += 1
                    else:
                        key_counts[key] = 1

        for key, count in key_counts.items():
            print(f"{key}: {count}")

        scripts = defaultdict(list)
        scripts_fun= defaultdict(list)

        for key in key_counts:

            if key_counts[key]>1:

                for dictionary in self.project_files:

                    if key in dictionary:
                        if not "require('express')" in dictionary[key] and not "require('mongoose')" in dictionary[key]:
                            code = dictionary[key]

                            ast = get_ast_request(code)
                            defined_v_f = parse_ast_conditionally(ast)
                            print(defined_v_f)

                            for key_vf in defined_v_f.keys():
                                if 'document' in defined_v_f[key_vf]:
                                    defined_v_f[key_vf].remove('document')

                            for function in defined_v_f["functions"]:
                                fun = find_function_by_name(code, function)
                                replacer = get_skeleton_method(fun)
                                if replacer is not None:
                                    code = code.replace(fun, replacer)
                                    if replacer not in scripts_fun[key]:
                                        scripts_fun[key].append(replacer)

                            for function in defined_v_f["arrow_functions"]:
                                fun = find_arrow_function_by_name(code, function)
                                replacer = get_skeleton_method(fun)
                                if replacer is not None:
                                    code = code.replace(fun, replacer)
                                    if replacer not in scripts_fun[key]:
                                        scripts_fun[key].append(replacer)

                            for function in defined_v_f["callbacks"]:
                                fun = find_event_listeners_by_variable(code, function)

                                if count_event_listeners(fun) > 1:
                                    event_listeners = split_event_listeners(fun, function)

                                    for event in event_listeners:
                                        replacer = get_skeleton_method(event)
                                        if replacer is not None:
                                            code = code.replace(event, replacer)
                                            if replacer not in scripts_fun[key]:
                                                scripts_fun[key].append(replacer)
                                else:
                                    replacer = get_skeleton_method(fun)
                                    if replacer is not None:
                                        code = code.replace(fun, replacer)
                                        if replacer not in scripts_fun[key]:
                                            scripts_fun[key].append(replacer)

                            scripts[key].append(code)



        with open("prompts/merge_byfile.prompt", "r") as file:
            merge = file.read().strip()


        merged_dict = {}
        response=[]
        for key, value_list in scripts.items():
            self.clear_conversation()
            merged_dict[key] = "\n".join(value_list)
            self.conversation.append({"role": "system", "content": merge})
            self.conversation.append({"role": "user", "content": merged_dict[key]})
            response.append(self.ai_conversation())








        with open('output/merged_files_js_structure.txt', 'w', encoding="utf-8") as file:
            for filename, contents in scripts.items():
                file.write(f"{filename}\n\n")
                for line in contents:
                    file.write(f"{line}\n")
                file.write("\n===========================================\n\n")

        with open('output/merged_files_js_structure_functions.txt', 'w', encoding="utf-8") as file:
            for filename, contents in scripts_fun.items():
                file.write(f"{filename}\n\n")
                for line in contents:
                    file.write(f"{line}\n")
                file.write("\n===========================================\n\n")

        with open('output/merged_files_js_structure_response_ai.txt', 'w', encoding="utf-8") as file:
            for contents in response:
                file.write(f"{contents}\n\n")
                file.write("\n===========================================\n\n")

