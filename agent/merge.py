from collections import defaultdict

from openai import OpenAI

from agent.JS_parser import get_ast_request, find_function_by_name, get_skeleton_method, find_arrow_function_by_name, \
    find_event_listeners_by_variable, count_event_listeners, split_event_listeners, parse_ast_conditionally, \
    parse_required_modules, find_express_app_variable, find_callback_bodies, extract_function, replace_function_in_code, \
    compare_js_functions, extract_functions_file
from agent.prebuild_file_parse import escape_snippet


def remove_keys(all_keys, keys_to_remove):
    all_keys = [key for key in all_keys if key not in keys_to_remove]
    return all_keys


class MergeFile:
    def __init__(self, project_files, client, project_id, root_path):
        self.merged_files = []
        self.conversation = []
        self.project_files = project_files
        self.client = client
        self.project_id = project_id
        self.root_path = root_path

    def clear_conversation(self):
        self.conversation = []

    def get_keys(self):
        return {key for d in self.project_files for key in d.keys()}

    def get_key_counts(self):
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

        return key_counts

    def get_client_js_structure(self, key_counts, project_files):

        scripts = defaultdict(list)
        scripts_fun = defaultdict(list)
        scripts_request_ai = defaultdict(list)
        defined_v_f = None

        for key in key_counts:

            if key_counts[key] > 1:

                for dictionary in project_files:

                    if key in dictionary:
                        if not "require('express')" in dictionary[key] and not "require('mongoose')" in dictionary[key]:
                            code = dictionary[key]
                            scripts_request_ai[key].append(code)

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

        return scripts, scripts_fun, scripts_request_ai

    def get_server_js_structure(self,key_counts, project_files):

        scripts = defaultdict(list)
        scripts_fun = defaultdict(list)
        scripts_request_ai = defaultdict(list)
        defined_v_f = None

        for key in key_counts:

            if key_counts[key] > 1:

                for dictionary in project_files:

                    if key in dictionary:
                        if "require('express')" in dictionary[key]:
                            code = dictionary[key]
                            scripts_request_ai[key].append(code)

                            ast = get_ast_request(code)
                            defined_v_f = parse_required_modules(ast)
                            print(defined_v_f)

                            variable_name = find_express_app_variable(code)

                            callback_bodies = find_callback_bodies(code, variable_name)
                            for i, body in enumerate(callback_bodies):
                                replacer = get_skeleton_method(body)
                                if replacer is not None:
                                    code = code.replace(body, replacer)
                                    if replacer not in scripts_fun[key]:
                                        scripts_fun[key].append(replacer)

                            scripts[key].append(code)

        return scripts, scripts_fun, scripts_request_ai

    def ai_conversation(self):

        completion = self.client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            messages=self.conversation,
            temperature=0.9
        )
        ai_response = completion.choices[0].message.content
        return ai_response

    def merge_files(self, type="default"):
        with open(f"{self.root_path}/prompts/merge.prompt", "r") as file:
            merge = file.read().strip()

        merged_js_client={}
        merged_js_server={}

        if type == "default" or type == "client":
            client_scripts, client_scripts_fun, client_scripts_request_ai = self.get_client_js_structure(self.get_key_counts(), self.project_files)
            merged_js_client = self.merge_js(client_scripts, client_scripts_fun,client_scripts_request_ai,"client")

        if type == "default" or type == "server":
            server_scripts, server_scripts_fun, server_scripts_request_ai = self.get_server_js_structure(self.get_key_counts(), self.project_files)
            merged_js_server = self.merge_js(server_scripts, server_scripts_fun, server_scripts_request_ai,"server")

        merged_js = {**merged_js_client, **merged_js_server}

        for key in merged_js.keys():
            self.merged_files.append({key : merged_js[key]})

        all_keys = remove_keys(self.get_keys(), merged_js.keys())

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

        # with open(f'output/projects/{self.project_id}/merged_files.txt', 'w', encoding="utf-8") as file:
        #     for dictionary in self.merged_files:
        #         for key, value in dictionary.items():
        #             if "```" in value:
        #                 value.replace("```","")
        #             file.write(f"{key}: ```{key}: {value}```\n\n")
        #
        #         file.write("\n===========================================\n")
        #     file.write("\n\n\n\n")
        #
        #     for dictionary in self.merged_files:
        #         for key in dictionary.keys():
        #             file.write("- " + key + "\n")

        return self.merged_files



    def merge_js(self, scripts, scripts_fun, scripts_request_ai, prefix="default"):
        merged_js = {}

        with open(f"{self.root_path}/prompts/merge_byfile.prompt", "r") as file:
            merge_file = file.read().strip()

        with open(f"{self.root_path}/prompts/merge_byfun.prompt", "r") as file:
            merge_fun = file.read().strip()

        merged_dict = {}
        response = {}
        for key, value_list in scripts.items():
            self.clear_conversation()
            merged_dict[key] = "\n".join(value_list)
            self.conversation.append({"role": "system", "content": merge_file})
            self.conversation.append({"role": "user", "content": merged_dict[key]})
            response[key] = self.ai_conversation()

        updated_fun = defaultdict(list)
        updated_structure = {}

        for key in response.keys():
            self.clear_conversation()
            updated_structure[key] = response[key]
            for fun in scripts_fun[key]:

                functions = extract_functions_file(scripts_request_ai[key], fun)
                if not compare_js_functions(functions):
                    prompt = (merge_fun
                              .replace("{{ function }}", fun.split("\n")[0])
                              .replace("{{ codes }}", functions)
                              )
                    self.conversation.append({"role": "user", "content": prompt})
                    answer = self.ai_conversation()
                    res = escape_snippet("javascript", answer).replace("javascript", "")

                    if not "{" and not "}" in res:
                        res = "//Reverted to last version\n" + functions.split("<|-|>")[-1]
                else:
                    res = "//Reverted to first version\n" + functions.split("<|-|>")[0]

                updated_fun[key].append(res)
                updated_structure[key] = replace_function_in_code(updated_structure[key], fun, res)

            # add possibility to add to structure not added function before
            for fun in scripts_fun[key]:
                if fun.split("\n")[0] not in updated_structure[key]:
                    for up_fun in updated_fun[key]:
                        try:
                            if fun.split("\n")[0] in up_fun.split("\n")[0] or fun.split("\n")[0] in up_fun.split("\n")[1]:
                                updated_structure[key] = updated_structure[key][:updated_structure[key].rfind('```')]
                                updated_structure[key] += "\n" + up_fun + "\n```"
                        except:
                            continue

            merged_js[key] = updated_structure[key]

        # with open(f'output/projects/{self.project_id}/merged_files_js_structure_{prefix}_updatedstruct.txt', 'w', encoding="utf-8") as file:
        #     for key in updated_structure.keys():
        #         file.write(f"{key}\n\n")
        #         file.write(f"{updated_structure[key]}\n")
        #         file.write("\n===========================================\n\n")
        #
        # with open(f'output/projects/{self.project_id}/merged_files_js_structure_{prefix}_updatedfun.txt', 'w', encoding="utf-8") as file:
        #     for filename, contents in updated_fun.items():
        #         file.write(f"{filename}\n\n")
        #         for line in contents:
        #             file.write(f"{line}\n")
        #         file.write("\n===========================================\n\n")
        #
        # with open(f'output/projects/{self.project_id}/merged_files_js_structure_{prefix}.txt', 'w', encoding="utf-8") as file:
        #     for filename, contents in scripts.items():
        #         file.write(f"{filename}\n\n")
        #         for line in contents:
        #             file.write(f"{line}\n")
        #         file.write("\n===========================================\n\n")
        #
        # with open(f'output/projects/{self.project_id}/merged_files_js_structure_functions_{prefix}.txt', 'w', encoding="utf-8") as file:
        #     for filename, contents in scripts_fun.items():
        #         file.write(f"{filename}\n\n")
        #         for line in contents:
        #             file.write(f"{line}\n")
        #         file.write("\n===========================================\n\n")
        #
        # with open(f'output/projects/{self.project_id}/merged_files_js_structure_response_ai_{prefix}.txt', 'w', encoding="utf-8") as file:
        #     for key in response.keys():
        #         file.write(f"{response[key]}\n\n")
        #         file.write("\n===========================================\n\n")

        return merged_js

