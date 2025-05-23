from ryoma_ai.agent.sql import SqlAgent
from ryoma_ai.datasource.postgres import PostgresDataSource
from langchain_google_genai import ChatGoogleGenerativeAI
import os

# load environment variables
from dotenv import load_dotenv
load_dotenv()

supabase_url = "postgresql://postgres:Seemeklobali@db.vnuxftuisohavexqicra.supabase.co:5432/postgres"
datasource = PostgresDataSource(supabase_url)

# Create a SQL agent
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")
sql_agent = SqlAgent(llm=llm).add_datasource(datasource)

# Step 4: Ask a question
sql_agent.stream(
    "Rate each student understanding from 1-100 based on chat history", display=True)
