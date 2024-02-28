import uuid

from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader

load_dotenv()

class Modularity:
    def __init__(self, project_path):
        self.chat = ChatOpenAI()
        self.embeddings = OpenAIEmbeddings()
        self.chain = None
        self.project_path = project_path
        # self.emb_id = str(uuid.uuid4().hex)
        self.emb_id = "emb/"+str(uuid.uuid4().hex)

    def prepare_vector_db(self):
        text_splitter = CharacterTextSplitter(separator="\n", chunk_size=4000, chunk_overlap=0)
        loader = TextLoader(self.project_path)
        project = loader.load_and_split(text_splitter=text_splitter)
        Chroma.from_documents(project,persist_directory=self.emb_id,embedding=self.embeddings)

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

    def project_summary(self):
        res = self.chain.run("""
        
        Analyzing project implementation, provide a list of JavaScript code file names and extract all functions, event handlers, callback functions and asynchronous route handler from each file. Organize the results by file, clearly indicating the file name before the list of functions in the file. For each function and event handler, provide the first line of the declaration. The output format should be as follows:

        File name: file_name.js
        - function functionName(parameters) {
        - element.addEventListener('event', function(parameters) {
        - someFunction(function(parameters) {
        - fun.call(
        - foo.ball(
        - app.get('/path', async (req, res) => {

        Emphasize that it is important to maintain accurate structure and formatting for clarity and ease of analysis. Emphasize that the file name should be explicitly highlighted and precede the list of functions contained in the file.
        
        """)
        print(res)
