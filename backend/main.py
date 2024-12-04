import os
import django
from GitHubApi.views import GitHubAPI
from ChatGPTAPI import ChatGPTAPI
import sqlite3

# Set the Django settings module (same as manage.py)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Automates.settings')
django.setup()


def process_data():
    # Connect to the SQLite database file
    db_path = 'db.sqlite3'  # Path to  SQLite database file
    connection = sqlite3.connect(db_path)
    
    try:
        # Create a cursor object to execute SQL queries
        cursor = connection.cursor()
        
        print("Fetching data from the database...")
        
        # Execute a SQL query to fetch all rows from a specific table
        cursor.execute("SELECT id, name FROM myapp_mymodel")  # Replace with your table name
        
        # Fetch all rows
        rows = cursor.fetchall()
        
        # Print each row
        for row in rows:
            print(f"Item ID: {row[0]}, Name: {row[1]}")
    except sqlite3.Error as e:
        print(f"Error interacting with the database: {e}")
    finally:
        # Close the connection to the database
        connection.close()


def run_github_api():
    print("Running GitHub API task...")
    github = GitHubAPI()
    # Example GitHub task
    auth_token = "your_personal_access_token"
    repos = github.getUserRepos(auth_token)
    print("Repositories:", repos)

def run_gpt_api():
    print("Running GPT API task...")
    chatgpt = ChatGPTAPI()
    user_prompt = "Create a professional LinkedIn post for my project."
    post = chatgpt.generateDescription(user_prompt)
    print("Generated LinkedIn Post:", post)

def main():
    print("Starting backend tasks...")
    process_data()
    run_github_api()
    run_gpt_api()
    print("All tasks completed!")

if __name__ == "__main__":
    main()