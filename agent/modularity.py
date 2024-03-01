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

from agent.prebuild_file_parse import escape_snippet

load_dotenv()


def parse_structure(string_to_parse):
    return [line.split('. ')[1] for line in string_to_parse.strip().split('\n')]


def parse_issues(text):
    issues_dict = {}
    current_issue = None
    lines = text.split('\n')

    for line in lines:
        line = line.strip()
        if line.endswith('Issue'):
            # Extract the issue number and start a new issue entry
            issue_number = line.split('.')[0]
            current_issue = issue_number
            issues_dict[current_issue] = []
        elif line.startswith('-'):
            # This is a primary list item for the current issue
            if current_issue is not None:
                issues_dict[current_issue].append(line[1:].strip())
        elif line.startswith('File:') or line.startswith('Function:'):
            # This is a sub-item related to the last primary list item, append it to the last item if exists
            if current_issue is not None and issues_dict[current_issue]:
                issues_dict[current_issue][-1] += ' ' + line

    return issues_dict


def parse_content_by_key(text, key):
    """
    Extracts content from text wrapped in triple backticks following a specific key.

    :param text: The text to search through.
    :param key: The key indicating the start of the content to extract.
    :return: The extracted content or None if not found.
    """
    # Pattern to find the content wrapped in triple backticks following the key
    # The key is escaped to handle special regex characters, and re.escape is used for that purpose.
    # The pattern uses non-greedy matching (.*?) to capture the content until the first closing backticks.
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

class Modularity:
    def __init__(self, id):
        self.chat = ChatOpenAI(model_name="gpt-3.5-turbo-1106")
        self.embeddings = OpenAIEmbeddings()
        self.chain = None
        self.project_path = f"output/projects/{id}/project_summary.txt"
        self.emb_id = "output/projects_embeddings/" + id

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

    def project_issue_solution(self):

        with open(self.project_path, "r", encoding="utf-8") as file:
            project_total = file.read().strip()

        for key in self.issues.keys():
            file_key=[]
            files = []
            request = "Based on Issue, provide me whole updated function if it js or whole html or css file"
            for file in self.project_structure_files:
                if file in '\n'.join(self.issues[key]):
                    files.append(parse_content_by_key(project_total, file + ":"))

                    request += f"Issue {key}:\n"
                    for detail in self.issues[key]:
                        request += f"- {detail}\n"

                    request += '\n'.join(files) + "\n\n\n"
                    file_key.append(file)

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
                                "You always send one updated whole file back. This file is "+f_k
                    ),
                    HumanMessage(
                        content=request
                    )
                ]
                res = self.chat(messages)

                project_total = replace_content_by_key(project_total, f_k + ":", res.content)


                print("\n\n\n======================================================\n\n\n")
                print(res.content)

        with open("nen.txt", "w", encoding="utf-8") as file:
             file.write(project_total)




    def project_init_pckg(self):
        res = self.chain.run("""
                        Create me command to install all required packages that used in project
                        it should be in format:
                        npm install package1 package2 ...

                        """)
        print(res)
