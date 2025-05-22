from langchain.chat_models import init_chat_model
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
import bs4
from langchain_core.prompts import PromptTemplate
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.document_loaders import TextLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langgraph.graph import START, StateGraph
from typing_extensions import List, TypedDict
import os
from dotenv import load_dotenv


load_dotenv()

# get api key from environment
api_key = os.environ["GOOGLE_API_KEY"]

llm = init_chat_model("gemini-2.0-flash", model_provider="google_genai")

embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
vector_store = InMemoryVectorStore(embeddings)
folder_path = "./data"
docs = []
for filename in os.listdir(folder_path):
    if filename.endswith(".txt"):
        loader = TextLoader(os.path.join(folder_path, filename))
        docs.extend(loader.load())

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000, chunk_overlap=200)
all_splits = text_splitter.split_documents(docs)
# Index chunks
_ = vector_store.add_documents(documents=all_splits)

# Define prompt for conversational question-answering
template = """אתה דוד בן גוריון, ראש הממשלה הראשון של ישראל. אתה מדבר עם תלמידי בית ספר יסודי בגילאי 8-12.
דבר איתם בצורה חמה, ידידותית וחינוכית, כאילו אתה באמת דוד בן גוריון שחוזר לחיים כדי לספר להם על עצמך.

הנחיות חשובות:
- דבר בגוף ראשון ("אני הייתי", "עשיתי", "חלמתי")
- השתמש בשפה פשוטה ומובנת לילדים
- היה נלהב ומעורר השראה
- עודד אותם לשאול שאלות נוספות
- ספר סיפורים אישיים וחוויות
- קשר את העבר להווה כדי שיבינו את הרלוונטיות
- אל תמציא מידע - השתמש רק במידע מהקונטקסט הנתון
- אם אתה לא יודע משהו, תגיד בכנות "זה לא כתוב כאן, אבל תוכל לשאול את המורה שלך"

מידע מהמסמכים:
{context}

השיחה עד כה:
{chat_history}

השאלה הנוכחית: {question}

תשובתך כדוד בן גוריון:"""
prompt = PromptTemplate.from_template(template)

# Define state for application with conversation history


class State(TypedDict):
    question: str
    context: List[Document]
    answer: str
    chat_history: str


# Define application steps
def retrieve(state: State):
    retrieved_docs = vector_store.similarity_search(state["question"])
    return {"context": retrieved_docs}


def generate(state: State):
    docs_content = "\n\n".join(doc.page_content for doc in state["context"])

    # Get existing chat history or initialize empty
    chat_history = state.get("chat_history", "")

    messages = prompt.invoke({
        "question": state["question"],
        "context": docs_content,
        "chat_history": chat_history
    })
    response = llm.invoke(messages)

    if chat_history:
        updated_history = f"{chat_history}\n\nQ: {state['question']}\nA: {response.content}"
    else:
        updated_history = f"Q: {state['question']}\nA: {response.content}"

    return {
        "answer": response.content,
        "chat_history": updated_history
    }


# Compile application
graph_builder = StateGraph(State).add_sequence([retrieve, generate])
graph_builder.add_edge(START, "retrieve")
graph = graph_builder.compile()

# Create a conversation session class to maintain state


class ConversationSession:
    def __init__(self, graph):
        self.graph = graph
        self.current_state = {"chat_history": ""}

    def ask(self, question):
        # Update state with new question while keeping chat history
        input_state = {
            "question": question,
            "chat_history": self.current_state.get("chat_history", "")
        }

        # Invoke the graph
        result = self.graph.invoke(input_state)

        # Update current state with the result
        self.current_state = result

        return result["answer"]

    def get_history(self):
        return self.current_state.get("chat_history", "")


# Usage example
session = ConversationSession(graph)

# First question
answer1 = session.ask("מה קורה?")
print("Answer 1:", answer1)
