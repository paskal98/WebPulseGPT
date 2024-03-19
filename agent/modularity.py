import os
import shutil
import re

from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain_core.messages import SystemMessage, HumanMessage

from agent.core import add_to_build_script
from agent.merge import MergeFile
from agent.prebuild_file_parse import escape_snippet



def get_npm_pkg(input_text):
    in_backticks = False

    captured_text = []

    backtick_count = 0

    for char in input_text:
        if char == '`':
            backtick_count += 1
            if backtick_count == 3:
                if in_backticks:
                    break
                else:
                    in_backticks = True
                    backtick_count = 0
                    continue
        else:
            backtick_count = 0

        if in_backticks and backtick_count == 0:
            captured_text.append(char)

    return ''.join(captured_text).strip()


def parse_structure(string_to_parse):
    return [line.split('. ')[1] for line in string_to_parse.strip().split('\n')]


def parse_issues(text):
    issues_dict = {}
    current_issue = None
    lines = text.split('\n')

    for line in lines:
        line = line.strip()
        if line.endswith('Issue'):
            issue_number = line.split('.')[0]
            current_issue = issue_number
            issues_dict[current_issue] = []
        elif line.startswith('-'):
            if current_issue is not None:
                issues_dict[current_issue].append(line[1:].strip())
        elif line.startswith('File:') or line.startswith('Function:'):
            if current_issue is not None and issues_dict[current_issue]:
                issues_dict[current_issue][-1] += ' ' + line

    return issues_dict


def parse_content_by_key(text, key):
    pattern = re.compile(re.escape(key) + r'\s*```(.*?)```', re.DOTALL)

    match = pattern.search(text)
    if match:
        return match.group(1).strip()  # Return the content, stripping any leading/trailing whitespace
    else:
        return "No content found for the specified key."


def replace_content_by_key(text, key, new_content):
    type = ""
    if ".js" in key:
        type = "javascript"
    elif "html" in key:
        type = "html"
    elif "css" in key:
        type = "css"
    old_content = parse_content_by_key(text,key)
    new_content = new_content.replace(f"```{type}","").replace("```","")
    return text.replace(old_content, new_content)


def extract_file_paths(text):
    regex = r'\b[\w./-]+/\w+\.\w+\b|\b[\w-]+\.\w+\b'

    matches = re.findall(regex, text)

    unique_matches_ordered = []
    for match in matches:
        if match not in unique_matches_ordered:
            unique_matches_ordered.append(match)

    return unique_matches_ordered


def get_uncreated_files(created_files, text):
    def flatten_and_unique(list_of_lists):
        unique_elements = []
        for sublist in list_of_lists:
            for item in sublist:
                if item not in unique_elements:
                    unique_elements.append(item)
        return unique_elements

    def replace_similar_and_create_new_list(list1, list2):
        filtered_list2 = [item for item in list2 if item not in list1]

        return filtered_list2

    files_paths = [extract_file_paths(text)]
    unique_files = flatten_and_unique(files_paths)
    res = replace_similar_and_create_new_list(created_files, unique_files)
    return res


def update_summary_with_issues(project_total, files):
    uncreated_files = files
    project_total += "\n\n\n"
    for u_f in uncreated_files:
        comment = ""
        if ".js" in u_f:
            comment = "//" + u_f
        elif ".html" in u_f:
            comment = "<!-- " + u_f + " -->"
        elif ".css" in u_f:
            comment = "/* " + u_f + " */"
        project_total += u_f + ": ```\n" + comment + "\n\n```\n\n"
    return project_total


def remove_first_line_if_contains(text, search_text):
    lines = text.split('\n')

    if lines and search_text in lines[0]:
        return '\n'.join(lines[1:])
    else:
        return text


def extract_code_block(text):
    start_delimiter = "```"
    end_delimiter = "```"
    start_index = text.find(start_delimiter) + len(start_delimiter)
    end_index = text.rfind(end_delimiter)
    if start_index > -1 and end_index > -1:
        return text[start_index:end_index].strip()
    else:
        return "No code block found."


class Modularity:
    def __init__(self, project_id, client, API, root_path):
        self.chat = ChatOpenAI(model_name="gpt-3.5-turbo-1106",openai_api_key=API)
        self.embeddings = OpenAIEmbeddings(openai_api_key=API)
        self.chain = None
        self.project_path = f"output/projects/{project_id}/project_summary.txt"
        self.emb_id = "output/projects_embeddings/" + project_id
        self.project_id = project_id
        self.client = client
        self.root_path = root_path

        if os.path.exists(self.emb_id):
            shutil.rmtree(self.emb_id)

        self.project_structure_files = []
        self.project_files = {}
        self.issues = {}
        self.issues_request = {}

    def prepare_vector_db(self):
        text_splitter = CharacterTextSplitter(separator="\n", chunk_size=4000, chunk_overlap=0)
        loader = TextLoader(self.project_path)
        project = loader.load_and_split(text_splitter=text_splitter)
        Chroma.from_documents(project, persist_directory=self.emb_id, embedding=self.embeddings)

    def prepare_chain(self):
        db = Chroma(
            persist_directory=self.emb_id,
            embedding_function=self.embeddings
        )
        retriever = db.as_retriever()
        self.chain = RetrievalQA.from_chain_type(llm=self.chat, retriever=retriever, chain_type="stuff")

    def init_module(self):
        self.prepare_vector_db()
        self.prepare_chain()

    def get_new_files(self):
        text_issues = ""
        for key in self.issues.keys():
            text_issues += "\n" + '\n'.join(self.issues[key])
        uncreated_files = get_uncreated_files(self.project_structure_files, text_issues)
        self.project_structure_files = list(set(uncreated_files + self.project_structure_files))
        return uncreated_files

    def set_project_path(self, new_path):
        self.project_path = new_path

    def project_structure(self):
        request = self.chain.run("""
        
        Analyzing project that described with plan, details and implementation, give me project structure in list format where files names rerpresented
        Format:
        1. file.one
        2. file.two
        ...
        
        """)

        self.project_structure_files = parse_structure(request)
        print(parse_structure(request))

    def project_summary(self):
        res = self.chain.run("""
        Based on project plan, project details and implemented code. Check if all implementation didnt skip requirements or something forgotten to added
        If any has forgotten, write file name, where was updates needed. Output format provided this
        Format:
        1. Issue
        - description about what should be done
        - files that should be used to solve issue
        - files that should be created
        2. ...
        """)

        self.issues = parse_issues(res)
        for issue, details in self.issues.items():
            print(f"Issue {issue}:")
            for detail in details:
                print(f"- {detail}")
            print()


    def project_user_updates(self, request):
        res = self.chain.run(f"""
        Based on project plan, project details, implemented code and user. Write issue or issues based on user request ` {request} `
        If any has forgotten, write file name, where was updates needed. Output format provided this
        Format:
        1. Issue
        - description about what should be done
        - files that should be used to solve issue
        - files that should be created
        2. ...
        """)

        self.issues = parse_issues(res)
        for issue, details in self.issues.items():
            print(f"Issue {issue}:")
            for detail in details:
                print(f"- {detail}")
            print()

    def project_issue_solution(self):

        with open(self.project_path, "r", encoding="utf-8") as file:
            project_total = file.read().strip()

        project_total = update_summary_with_issues(project_total, self.get_new_files())
        print(self.project_structure_files)

        for key in self.issues.keys():
            file_key=[]
            files = []
            request = "Based on Issue, provide me whole updated function if it js or whole html or css file\n\n"
            is_issue_added = False
            for file in self.project_structure_files:
                if file in '\n'.join(self.issues[key]):
                    files.append("```\n"+parse_content_by_key(project_total, file + ":")+"\n```\n\n")

                    if not is_issue_added:
                        request += f"Issue {key}:\n"
                        for detail in self.issues[key]:
                            request += f"- {detail}\n\n\n"
                        is_issue_added = True
                    file_key.append(file)

            request += '\n'.join(files) + "\n\n\n"

            for f_k in file_key:
                request+="\nReturn now only whole code of "+f_k +" file, other updates in other files dont provide. I need updated "+f_k+" file back"
                messages = [
                    SystemMessage(
                        content="You are a helpful developer, that make all task that you provide. "
                                "You always write whole code back after applying updates"
                                "Start you response in this format:"
                                "here filepath.type:"
                                "here comment of how file path and type of file like nameOfFile.type"
                                "here code..."
                                "filepath.type can be any name and type, its example"
                                "You always send one updated function back if it javascript or whole file of index or css. This file is "+f_k
                    ),
                    HumanMessage(
                        content=request
                    )
                ]
                res = self.chat(messages)


                code_response = (extract_code_block(res.content))
                code_response = remove_first_line_if_contains(code_response, "javascript")
                code_response = remove_first_line_if_contains(code_response, "html")
                code_response = remove_first_line_if_contains(code_response, "css")

                code_old = parse_content_by_key(project_total, f_k + ":")

                print("\n\n\n======================================================\n\n\n")
                print(code_response)


                #preparse ast tree for better merging
                if ".js" in f_k and len(code_old) != len("//"+f_k):
                    code_old = remove_first_line_if_contains(code_old, "javascript")
                    merge = MergeFile([{f_k:code_old},{f_k:code_response}], self.client, self.project_id, self.root_path)

                    if "require('express" in code_old:
                        response = merge.merge_files(type="server")[0][f_k]
                    else:
                        response = merge.merge_files(type="client")[0][f_k]

                    code_response = extract_code_block(response.replace(f_k+":","\n"))
                    code_response = remove_first_line_if_contains(code_response,"javascript")
                    code_response=code_response.replace(f_k+":","\n")



                project_total = replace_content_by_key(project_total, f_k + ":", code_response)

                request = request.replace(code_old, code_response)
                request = request.replace("\nReturn now only whole code of "+f_k +" file, other updates in other files dont provide. I need updated "+f_k+" file back",'')




        with open(self.project_path, "w", encoding="utf-8") as file:
             file.write(project_total)


    def project_builder_init(self):
        with open(self.project_path, "r", encoding="utf-8") as file:
            project_total = file.read().strip()

        file_path = f'output/projects/{self.project_id}/build.sh'

        if os.path.exists(file_path):
            os.remove(file_path)

        for file in self.project_structure_files:
            content = parse_content_by_key(project_total, file + ":")

            content = remove_first_line_if_contains(content, "javascript")
            content = remove_first_line_if_contains(content, "html")
            content = remove_first_line_if_contains(content, "css")

            add_to_build_script(file, content, self.project_id)

        npm_pkg = self.project_init_pkg()
        with open(f'output/projects/{self.project_id}/build.sh', 'a', encoding="utf-8") as script_file:
            script_file.write(f'\n{npm_pkg}\n')



    def project_init_pkg(self):
        res = self.chain.run("""
                        Based on Project implementation
                        Create me command to install all required packages that used in project
                        Output format should be in format:
                        npm install package1 package2 ...

                        """)

        print(res)

        if len(get_npm_pkg(res)) == 0:
            return res
        else:
            return get_npm_pkg(res)

