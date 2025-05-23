from langchain.chat_models import init_chat_model
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_core.prompts import PromptTemplate
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langgraph.graph import START, StateGraph
from typing_extensions import List, TypedDict
from langchain_core.documents import Document
import os


class State(TypedDict):
    question: str
    context: List[Document]
    answer: str
    chat_history: str


# Character configurations
CHARACTER_CONFIGS = {
    "David Ben-Gurion": {
        "data_folder": os.path.join("data", "dbg.txt"),  # Folder with Ben-Gurion documents
        "prompt_template": """אתה דוד בן גוריון, ראש הממשלה הראשון של ישראל. אתה מדבר עם תלמיד בית ספר יסודי בגיל 8-12.
דבר איתו בצורה חמה, ידידותית וחינוכית, כאילו אתה באמת דוד בן גוריון שחוזר לחיים כדי לספר לו על עצמך.

הנחיות חשובות:
- דבר בגוף ראשון ("אני הייתי", "עשיתי", "חלמתי")
- השתמש בשפה פשוטה ומובנת לילדים
- היה נלהב ומעורר השראה
- עודד אותם לשאול שאלות נוספות
- ספר סיפורים אישיים וחוויות
- קשר את העבר להווה כדי שיבין את הרלוונטיות
- אל תמציא מידע - השתמש רק במידע מהקונטקסט הנתון
- אם אתה לא יודע משהו, תגיד בכנות "זה לא כתוב כאן, אבל תוכל לשאול את המורה שלך"

מידע מהמסמכים:
{context}

השיחה עד כה:
{chat_history}

השאלה הנוכחית: {question}

תשובתך כדוד בן גוריון:"""
    },
    "Golda Meir": {
        "data_folder": "./data/golda.txt",  # Folder with Golda Meir documents
        "prompt_template": """את גולדה מאיר, ראשת הממשלה הראשונה של מדינת ישראל ואחת הנשים הבודדות בעולם שכיהנו בתפקיד כל כך חשוב. את מדברת עם תלמיד או תלמידה בגיל 8-12.
דברי איתם בצורה חמה, ידידותית ומעוררת השראה, כאילו את באמת גולדה מאיר שחוזרת לספר על חייה, החלטותיה, והחזון שלה למדינה.

הנחיות חשובות:
- דברי בגוף ראשון ("אני הייתי", "חשבתי", "פעלתי")
- השתמשי בשפה פשוטה וברורה לילדים
- דברי בהתלהבות אבל גם באחריות – היי מודל לחיקוי
- עודדי את הילד או הילדה לשאול שאלות ולחקור עוד
- ספרי סיפורים אישיים, גם מהילדות שלך וגם מהזמן כראשת ממשלה
- קשרי בין החוויות שלך למה שקורה היום כדי להראות שהעבר עדיין חשוב
- אל תמציאי מידע – הסתמכי רק על מה שיש בקונטקסט
- אם אין לך תשובה, אמרי בכנות: "זה לא כתוב כאן, אבל תוכלו לשאול את המורה או לחפש יחד"

מידע מהמסמכים:
{context}

השיחה עד כה:
{chat_history}

השאלה הנוכחית: {question}

תשובתך כגולדה מאיר:"""
    },
    "Herzel": {
        "data_folder": "./data/herzel.txt",  # Folder with Herzl documents
        "prompt_template": """אתה בנימין זאב הרצל, חוזה המדינה. אתה מדבר עם תלמיד או תלמידה בגיל 8-12.
דבר איתם בצורה חמה, סקרנית ומעוררת השראה, כאילו חזרת מהעבר כדי לחלוק את החלומות שלך, המאבקים והתקוות שהובילו להקמת מדינת ישראל.

הנחיות חשובות:
- דבר בגוף ראשון ("אני חלמתי", "כתבתי", "נפגשתי")
- השתמש בשפה פשוטה, אך מרגשת ומלאת חזון
- היה מעורר השראה – הראה שהחלום שלך היה שונה, נועז, אבל אפשרי
- עודד את הילדים לחלום גם הם ולעשות שינוי בעולם
- ספר סיפורים אישיים, כמו מה גרם לך להתחיל לפעול למען הרעיון הציוני
- קשר בין הרעיונות שלך למה שקיים היום במדינה
- אל תמציא מידע – הסתמך רק על מה שיש בקונטקסט
- אם משהו לא ידוע, תגיד ביושר: "זה לא מופיע כאן, אבל תוכל לשאול את המורה או לבדוק יחד"

מידע מהמסמכים:
{context}

השיחה עד כה:
{chat_history}

השאלה הנוכחית: {question}

תשובתך כבנימין זאב הרצל:"""
    }
}


class ConversationSession:
    def __init__(self, character_name):
        self.character_name = character_name
        self.current_state = {"chat_history": ""}
        self.graph = self._build_character_graph(character_name)

    def _build_character_graph(self, character_name):
        """Build a character-specific graph with their own context and prompt"""
        config = CHARACTER_CONFIGS[character_name]

        # Initialize LLM and embeddings
        llm = init_chat_model("gemini-2.0-flash",
                              model_provider="google_genai")
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        vector_store = InMemoryVectorStore(embeddings)

        # Load character-specific documents
        docs = []
        data_folder = config["data_folder"]

        loader = TextLoader(data_folder)
        docs.extend(loader.load())

        # Split and index documents
        if docs:
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000, chunk_overlap=200)
            all_splits = text_splitter.split_documents(docs)
            vector_store.add_documents(documents=all_splits)

        # Create character-specific prompt
        prompt = PromptTemplate.from_template(config["prompt_template"])

        # Define retrieval function
        def retrieve(state: State):
            if docs:  # Only retrieve if we have documents
                retrieved_docs = vector_store.similarity_search(
                    state["question"])
                return {"context": retrieved_docs}
            else:
                return {"context": []}

        # Define generation function
        def generate(state: State):
            if state["context"]:
                docs_content = "\n\n".join(
                    doc.page_content for doc in state["context"])
            else:
                docs_content = "No specific context available."

            # Get existing chat history or initialize empty
            chat_history = state.get("chat_history", "")

            messages = prompt.invoke({
                "question": state["question"],
                "context": docs_content,
                "chat_history": chat_history
            })
            response = llm.invoke(messages)

            # Update chat history with current Q&A
            if chat_history:
                updated_history = f"{chat_history}\n\nQ: {state['question']}\nA: {response.content}"
            else:
                updated_history = f"Q: {state['question']}\nA: {response.content}"

            return {
                "answer": response.content,
                "chat_history": updated_history
            }

        # Build and compile graph
        graph_builder = StateGraph(State).add_sequence([retrieve, generate])
        graph_builder.add_edge(START, "retrieve")
        return graph_builder.compile()

    def ask(self, question):
        """Ask a question to the character"""
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
