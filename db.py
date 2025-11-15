import getpass
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI  # Use ChatOpenAI instead of OpenAI
from langchain.chains import create_sql_query_chain
from langchain_community.utilities import SQLDatabase

load_dotenv()

# Check and prompt for missing critical environment variables
if not os.environ.get("OPENAI_API_KEY"):
    os.environ["OPENAI_API_KEY"] = getpass.getpass("Enter API key for OpenAI: ")
print("Using OPENAI_API_KEY:", os.environ["OPENAI_API_KEY"][:10] + "..." + os.environ["OPENAI_API_KEY"][-4:])

db = SQLDatabase.from_uri("sqlite:///Chinook.db")

# Use ChatOpenAI instead of OpenAI
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

from operator import itemgetter

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_community.tools import QuerySQLDatabaseTool

execute_query = QuerySQLDatabaseTool(db=db)
write_query = create_sql_query_chain(llm, db)
chain = write_query | execute_query
answer_prompt = PromptTemplate.from_template(
    """Given the following user question, corresponding SQL query, and SQL result, answer the user question.

Question: {question}
SQL Query: {query}
SQL Result: {result}
Answer: """
)

answer = answer_prompt | llm | StrOutputParser()
chain = (
    RunnablePassthrough.assign(query=write_query).assign(
        result=itemgetter("query") | execute_query
    )
    | answer
)

result = chain.invoke({"question": "How many employees are there"})
print("Result:", result)
