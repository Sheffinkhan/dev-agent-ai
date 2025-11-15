import getpass
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_community.agent_toolkits.jira.toolkit import JiraToolkit
from langchain_community.utilities.jira import JiraAPIWrapper
from langgraph.prebuilt import create_react_agent
import re

# Load_DC environment variables
load_dotenv()

# Prompt for missing environment variables
if not os.environ.get("OPENAI_API_KEY"):
    os.environ["OPENAI_API_KEY"] = getpass.getpass("Enter API key for OpenAI: ")
print("Using OPENAI_API_KEY:", os.environ["OPENAI_API_KEY"][:10] + "..." + os.environ["OPENAI_API_KEY"][-4:])
if not os.environ.get("JIRA_API_TOKEN"):
    os.environ["JIRA_API_TOKEN"] = getpass.getpass("Enter Jira API token: ")
if not os.environ.get("JIRA_USERNAME"):
    os.environ["JIRA_USERNAME"] = input("Enter Jira username (email): ")
if not os.environ.get("JIRA_INSTANCE_URL"):
    os.environ["JIRA_INSTANCE_URL"] = input("Enter Jira instance URL (e.g., https://yourcompany.atlassian.net): ")

# Initialize OpenAI model
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

# Initialize Jira toolkit
jira = JiraAPIWrapper(
    jira_username=os.environ["JIRA_USERNAME"],
    jira_api_token=os.environ["JIRA_API_TOKEN"],
    jira_instance_url=os.environ["JIRA_INSTANCE_URL"]
)
toolkit = JiraToolkit.from_jira_api_wrapper(jira)

# Sanitize tool names to comply with OpenAI's requirements
def sanitize_tool_name(name):
    """Convert tool name to match pattern ^[a-zA-Z0-9_-]+$"""
    # Replace invalid characters with underscores and remove leading/trailing underscores
    sanitized = re.sub(r'[^a-zA-Z0-9_-]', '_', name)
    sanitized = re.sub(r'_+', '_', sanitized)  # Collapse multiple underscores
    return sanitized.strip('_')

# Modify tool names directly
sanitized_tools = toolkit.get_tools()
for tool in sanitized_tools:
    tool.name = sanitize_tool_name(tool.name)

# Print tool names for debugging
print("Sanitized tool names:", [tool.name for tool in sanitized_tools])

# Initialize the ReAct agent with sanitized tools
agent = create_react_agent(llm, tools=sanitized_tools)

# Run the agent
response = agent.invoke({"messages": [{"role": "user", "content": "List issues in project CustomerSync Todo"}]})
print("Agent response:", response["messages"][-1].content)