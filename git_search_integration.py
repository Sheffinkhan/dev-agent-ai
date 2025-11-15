import os
import getpass
from dotenv import load_dotenv
from git import Repo, GitCommandError
from langchain_openai import OpenAI

# Load environment variables from .env file
load_dotenv()

# Prompt for missing GitHub credentials
if not os.environ.get("GITHUB_ACCESS_TOKEN"):
    os.environ["GITHUB_ACCESS_TOKEN"] = getpass.getpass("Enter GitHub Access Token: ")

if not os.environ.get("GITHUB_REPO_URL"):
    os.environ["GITHUB_REPO_URL"] = input("Enter GitHub Repo URL (e.g., https://github.com/username/repo.git): ")

if not os.environ.get("GITHUB_BRANCH"):
    os.environ["GITHUB_BRANCH"] = input("Enter GitHub Branch Name (e.g., main): ")

# Define repo path
repo_path = os.path.expanduser("Demoproject")

# Clone or update the repository
try:
    if os.path.exists(os.path.join(repo_path, ".git")):
        print("Repository already exists. Pulling latest changes...")
        repo = Repo(repo_path)
        repo.remotes.origin.pull()
    else:
        print("Cloning repository...")
        repo = Repo.clone_from(os.environ["GITHUB_REPO_URL"], repo_path, branch=os.environ["GITHUB_BRANCH"])
except GitCommandError as e:
    print("Error handling Git repository:", e)
    exit(1)

# Get search term from user
search_text = input("\nEnter the text to search for: ")

# Function to search for text in repository files
def search_text_in_files(repo_path, search_text):
    matching_files = []
    for root, _, files in os.walk(repo_path):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    if search_text in f.read():
                        matching_files.append(file_path)
            except Exception as e:
                print(f"Skipping file {file_path} due to error: {e}")
    
    return matching_files

# Search for the text in files
files_with_text = search_text_in_files(repo_path, search_text)


# Display results
if files_with_text:
    print("\nFiles containing the searched text:")
    for file in files_with_text:
        print(f"- {file}")
else:
    print("\nNo matching files found.")
