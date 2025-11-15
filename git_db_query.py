import getpass
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.chains import create_sql_query_chain
from langchain_community.utilities import SQLDatabase
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_community.tools import QuerySQLDatabaseTool

# Load environment variables
load_dotenv()

# Check and prompt for missing critical environment variables
if not os.environ.get("OPENAI_API_KEY"):
    os.environ["OPENAI_API_KEY"] = getpass.getpass("Enter API key for OpenAI: ")
print("Using OPENAI_API_KEY:", os.environ["OPENAI_API_KEY"][:10] + "..." + os.environ["OPENAI_API_KEY"][-4:])

# Connect to SQLite database containing Git details
db = SQLDatabase.from_uri("sqlite:///GitDetails.db")

# Use ChatOpenAI instead of OpenAI
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

# Define tools for query execution
execute_query = QuerySQLDatabaseTool(db=db)
write_query = create_sql_query_chain(llm, db)

# Define prompt for answering questions
answer_prompt = PromptTemplate.from_template(
    """Given the following user question, corresponding SQL query, and SQL result, answer the user question.

Question: {question}
SQL Query: {query}
SQL Result: {result}
Answer: """
)

# Function to generate and execute SQL query
def execute_single_query(question):
    query = write_query.invoke({"question": question})  # Generate SQL query
    result = execute_query.run(query)  # Execute the query safely
    return answer_prompt.format(question=question, query=query, result=result)

# Process the query and generate an answer
question = "Which commits have been made by Alice Johnson?"
formatted_input = execute_single_query(question)
answer = llm.invoke(formatted_input)
parsed_answer = StrOutputParser().invoke(answer)

print("Result:", parsed_answer)
