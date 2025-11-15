import os
import subprocess
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

# Load environment variables
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# Define local directory and repository URL
repo_url = "https://github.com/sheffin-khan/Demo.git"  # Your GitHub repo
repo_path = os.path.join(os.getcwd(), "Demo")  # Local repo path
html_file_path = os.path.join(repo_path, "demo.html")  # Path to HTML file

# Clone the repository if it does not exist
if not os.path.exists(repo_path):
    subprocess.run(["git", "clone", repo_url])

# Change to the repo directory
os.chdir(repo_path)

# Read the existing HTML content
with open(html_file_path, "r", encoding="utf-8") as file:
    existing_html = file.read()

# Initialize OpenAI LLM
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

# Define the prompt to modify the HTML file
prompt = f"""
Change the Click Here button to Click

{existing_html}
"""

# Generate the modified HTML
modified_html = llm.invoke(prompt).content  # Extract text from AIMessage

# Save the modified file
with open(html_file_path, "w", encoding="utf-8") as file:
    file.write(modified_html)

print("File updated successfully!")

# Git commands to commit and push changes
subprocess.run(["git", "add", "demo.html"])
subprocess.run(["git", "commit", "-m", prompt])
subprocess.run(["git", "push", "origin", "main"])  # Change 'main' if using a different branch

print("Changes pushed to the repository!")
