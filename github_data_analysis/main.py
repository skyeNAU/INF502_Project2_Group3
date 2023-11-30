from classes.github_repository import GitHubRepository
from datetime import datetime, timedelta
from utils.api_helpers import get_repository_info
from utils.csv_helpers import save_as_csv
from datetime import datetime
import csv
import requests
import os
import re
from bs4 import BeautifulSoup
import pandas as pd
from visualizations.repository_visualizations import (
    boxplot_commits, 
    boxplot_additions_deletions,
    boxplot_changed_files_author,
    scatterplot_additions_deletions,
    calculate_correlations
    )

from visualizations.user_visualizations import (
    line_graph_prs_per_day,
    line_graph_open_closed_prs_per_day,
    bar_plot_users_per_repository
)

def main_menu():
    while True:
        print("\nGitHub Data Analysis")
        print("1. Collect data for a specific repository")
        print("2. Show all repositories")
        print("3. Create visualizations")
        print("4. Calculate correlations")
        print("5. User Profile")
        print("6. Exit")
        
        choice = input("Enter your choice (1-5): ")

        if choice == '1':
            api_limit_warning()
        elif choice == '2':
            show_all_repositories()
        elif choice == '3':
            visualization_menu()
        elif choice == '4':
            calculate_correlations()
        elif choice == '5':
            get_user_profile()
        elif choice == '6':
            print("Exiting...")
            break
        else:
            print("Invalid choice, please try again.")
            
def get_user_profile():
     owner = input("Enter username of the GitHub Account: ")
     print("****************************************************************************")
     print("****************************************************************************")
     user_url = f"https://api.github.com/users/{owner}"
     contributions_url = f"https://api.github.com/users/{owner}/events"
    # Fetch user data
     user_response = requests.get(user_url)
     if user_response.status_code == 404:
        print(f"User '{owner}' not found.")
        print("****************************************************************************")
        print("****************************************************************************")
        return
     else:
         user_data = user_response.json()
         # Fetch contribution events
         contributions_response = requests.get(contributions_url)
         contributions_data = contributions_response.json()
         # Calculate contributions in the last year
         one_year_ago = datetime.now() - timedelta(days=365)
         contributions_last_year = [event for event in contributions_data if datetime.strptime(event['created_at'], "%Y-%m-%dT%H:%M:%SZ") >= one_year_ago]
         # Display user information
         print("USERNAME                 :     ",owner)
         print(f"NUMBER OF REPOSITORIES  : {user_data.get('public_repos', 0)}")
         print(f"NUMBER OF FOLLOWERS     : {user_data.get('followers', 0)}")
         print(f"NUMBER OF FOLLOWING     : {user_data.get('following', 0)}")
         print(f"CONTRIBUTIONS LAST YEAR : {len(contributions_last_year)}")
         print("****************************************************************************")
         print("****************************************************************************")
     
    
            
def visualization_menu():
    # Get repository details from the user
    owner = input("Enter the repository owner's username: ")
    repo = input("Enter the repository name: ")
    repo_csv_path = f"repos/{owner}-{repo}.csv"  # Construct the file path

    while True:
        print("\nVisualizations for Repository:", repo)
        print("1. Boxplot of Commits in Open vs Closed Pull Requests")
        print("2. Boxplot of Additions and Deletions in Pull Requests")
        print("3. Boxplot of Changed Files by Author Association")
        print("4. Scatterplot of Additions vs Deletions")
        print("5. Line Graph of Total PRs per Day")
        print("6. Line Graph of Open vs Closed PRs per Day")
        print("7. Bar Plot of Users per Repository")
        print("8. Calculate correlations")
        print("9. Go Back")

        choice = input("Enter your choice (1-8): ")

        if choice == '1':
            boxplot_commits(repo_csv_path)
        elif choice == '2':
            boxplot_additions_deletions(repo_csv_path)
        elif choice == '3':
            boxplot_changed_files_author(repo_csv_path)
        elif choice == '4':
            scatterplot_additions_deletions(repo_csv_path)
        elif choice == '5':
            line_graph_prs_per_day(repo_csv_path)
        elif choice == '6':
            line_graph_open_closed_prs_per_day(repo_csv_path)
        elif choice == '7':
            # For bar_plot_users_per_repository, you might use a different CSV
            bar_plot_users_per_repository('users.csv')
        elif choice == '8':
            calculate_correlations()
        elif choice == '9':
            break
        else:
            print("Invalid choice, please try again.")

def api_limit_warning():
    print()
    print('Warning: Rate limits exist for GitHub API')
    print('To avoid 403 Error/ rate limit exceeded, it is recommended to limit your')
    print('repository pull request to the 10 most recent pulls. How would you like to ')
    print('proceed?')
    while True:
        print("1. Retrieve last 10 pull requests (recommended)")
        print("2. Retrieve all pull requests")
        print("3. Go back")

        choice = input("Enter your choice (1-3): ")

        if choice == '1':
            collect_repository_data()
        elif choice == '2':
            collect_ALL_repository_data()
        elif choice == '3':
            break
        else:
            print("Invalid choice, please try again.")

def get_repository_info(owner, repo_name):
    url = f"https://api.github.com/repos/{owner}/{repo_name}"
    response = requests.get(url)
    return response.json()

def collect_repository_data():
    owner = input("Enter the repository owner's username: ")
    repo_name = input("Enter the repository name: ")

    try:
        # Fetch repository data from GitHub API
        repo_info = get_repository_info(owner, repo_name)
        print(repo_info)
        
        if repo_info is None:
            print("Failed to fetch repository data. The repository may not exist or there was an API error.")
            return
        
        fetch_and_save_pull_requests(owner, repo_name)

        usernames = extract_usernames_from_prs(f"repos/{owner}-{repo_name}.csv")
        print(f"Usernames extracted: {usernames}")

        if usernames:
            fetch_and_save_user_data(usernames)
        else:
            print("No user data to fetch.")

        # Extract necessary information
        description = repo_info.get('description', 'No description')
        print(f"Description: {description}")
        homepage = repo_info.get('homepage', 'No homepage')
        print(f"Homepage: {homepage}")
        license_info = 'No license'
        if repo_info.get('license'):
            license_info = repo_info['license'].get('name', 'No license')
        forks = repo_info.get('forks_count', 0)
        print(f"Forks: {forks}")
        watchers = repo_info.get('watchers_count', 0)
        print(f"watchers:" , {watchers})
        date_of_collection = repo_info.get('updated_at', 'No date')
        print(f"Date of Collection: {date_of_collection}")
        
        print("Creating GitHubRepository object...")
        my_repo = GitHubRepository(repo_name, owner, description, homepage, license_info, forks, watchers, date_of_collection)
        print("GitHubRepository object created.")

        repo_headers = ['Name', 'Owner', 'Description', 'Homepage', 'License', 'Forks', 'Watchers', 'Date of Collection']
        # Save this object to CSV
        save_as_csv('repositories.csv', my_repo, repo_headers)

        print("Repository data collected and saved successfully.")

    except Exception as e:
        print(f"An error occurred {e}")


def collect_ALL_repository_data():
    owner = input("Enter the repository owner's username: ")
    repo_name = input("Enter the repository name: ")

    try:
        # Fetch repository data from GitHub API
        repo_info = get_repository_info(owner, repo_name)

        if repo_info is None:
            print("Failed to fetch repository data. The repository may not exist or there was an API error.")
            return

        fetch_and_save_ALL_pull_requests(owner, repo_name)

        usernames = extract_usernames_from_prs(f"repos/{owner}-{repo_name}.csv")
        print(f"Usernames extracted: {usernames}")

        if usernames:
            fetch_and_save_user_data(usernames)
        else:
            print("No user data to fetch.")

        # Extract necessary information
        description = repo_info.get('description', 'No description')
        print(f"Description: {description}")
        homepage = repo_info.get('homepage', 'No homepage')
        print(f"Homepage: {homepage}")
        license_info = 'No license'
        if repo_info.get('license'):
            license_info = repo_info['license'].get('name', 'No license')
        forks = repo_info.get('forks_count', 0)
        print(f"Forks: {forks}")
        watchers = repo_info.get('watchers_count', 0)
        print(f"watchers:", {watchers})
        date_of_collection = repo_info.get('updated_at', 'No date')
        print(f"Date of Collection: {date_of_collection}")

        print("Creating GitHubRepository object...")
        my_repo = GitHubRepository(repo_name, owner, description, homepage, license_info, forks, watchers,
                                   date_of_collection)
        print("GitHubRepository object created.")

        repo_headers = ['Name', 'Owner', 'Description', 'Homepage', 'License', 'Forks', 'Watchers',
                        'Date of Collection']
        # Save this object to CSV
        save_as_csv('repositories.csv', my_repo, repo_headers)

        print("Repository data collected and saved successfully.")

    except Exception as e:
        print(f"An error occurred {e}")



def show_all_repositories():
    try:
        with open('repositories.csv', mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            repositories = list(reader)
            print("Repositories:")
            for idx, repo in enumerate(repositories):
                print(f"{idx + 1}. {repo[0]}")  # Assuming the first column is the repository name

            repo_choice = int(input("Select a repository for more actions (enter the number, or 0 to go back): "))
            if repo_choice == 0:
                return

            selected_repo = repositories[repo_choice - 1]
            perform_actions_on_repository(selected_repo)

    except Exception as e:
        print(f"An error occurred: {e}")

def perform_actions_on_repository(repo):
    while True:
        print(f"\nSelected Repository: {repo[0]}")
        print("1. Show pull requests")
        print("2. Show repository summary")
        print("3. Go back")
        
        choice = input("Enter your choice (1-3): ")

        if choice == '1':
            show_pull_requests(repo[1], repo[0])  # Assuming the second column is the owner's username
        elif choice == '2':
            show_repository_summary(repo[1], repo[0])
        elif choice == '3':
            break
        else:
            print("Invalid choice, please try again.")
        
def show_repository_summary(owner, repo_name):
    try:
        with open(f'repos/{owner}-{repo_name}.csv', mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            open_prs = closed_prs = 0
            oldest_date = datetime.now()
            users = set()

            for row in reader:
                if row['State'] == 'open':
                    open_prs += 1
                elif row['State'] == 'closed':
                    closed_prs += 1
                users.add(row['User'])
                # Update datetime parsing format to match your CSV file format
                pr_date = datetime.strptime(row['Created_At'], '%Y-%m-%dT%H:%M:%SZ')
                if pr_date < oldest_date:
                    oldest_date = pr_date

            print(f"Open PRs: {open_prs}, Closed PRs: {closed_prs}, Users: {len(users)}, Oldest PR Date: {oldest_date.strftime('%Y-%m-%d')}")
    except Exception as e:
        print(f"An error occurred: {e}")
        
def show_pull_requests(owner, repo_name):
    try:
        with open(f'repos/{owner}-{repo_name}.csv', mode='r', newline='', encoding='utf-8') as file:
            reader = pd.read_csv(file)
            print(f"Pull Requests for {repo_name}:")
            pd.set_option('display.max_columns', None)
            print(reader)
    except Exception as e:
        print(f"An error occurred: {e}")

def show_pull_requests_for_repository(owner, repo_name):
    show_pull_requests(owner, repo_name)

def show_repository_summary_input():
    owner = input("Enter the repository owner's username: ")
    repo_name = input("Enter the repository name: ")
    show_repository_summary(owner, repo_name)
    
def fetch_and_save_pull_requests(owner, repo_name):
    os.makedirs('repos', exist_ok=True)  # Create 'repos/' directory if it doesn't exist
    prs_url = f"https://api.github.com/repos/{owner}/{repo_name}/pulls"
    prs_response = requests.get(prs_url)
    print("API Response:", prs_response.json()) 
    pull_requests = prs_response.json()
    print(pull_requests)
#    pull_requests = pull_requests[-15:]

    # Open the CSV file for writing
    with open(f'repos/{owner}-{repo_name}.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Write the header
        writer.writerow(['Title', 'PR_Number', 'Body', 'State', 'Created_At', 'Closed_At', 'User', 'Commits', 'Additions', 'Deletions', 'Changed_Files'])

        for pr in pull_requests[-10:]:
            # Fetch additional details for each PR
            pr_detail_url = pr['url']
            pr_detail_response = requests.get(pr_detail_url)
            pr_detail = pr_detail_response.json()

            # Fetch commit data
            commits_url = pr_detail['commits_url']
            commits_response = requests.get(commits_url)
            commits_data = commits_response.json()
            num_commits = len(commits_data)

            # Fetch additions, deletions, and changed files data (if available)
            additions = pr_detail.get('additions', 0)
            deletions = pr_detail.get('deletions', 0)
            changed_files = pr_detail.get('changed_files', 0)

            # Write data to CSV
            writer.writerow([
                pr_detail.get('title'), pr_detail.get('number'), pr_detail.get('body'), 
                pr_detail.get('state'), pr_detail.get('created_at'), pr_detail.get('closed_at'), 
                pr_detail.get('user', {}).get('login'), num_commits, additions, deletions, changed_files
            ])


def fetch_and_save_ALL_pull_requests(owner, repo_name):
    os.makedirs('repos', exist_ok=True)  # Create 'repos/' directory if it doesn't exist
    prs_url = f"https://api.github.com/repos/{owner}/{repo_name}/pulls"
    prs_response = requests.get(prs_url)
    print("API Response:", prs_response.json())
    pull_requests = prs_response.json()
    print(pull_requests)
    print("*************")

    # Open the CSV file for writing
    with open(f'repos/{owner}-{repo_name}.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Write the header
        writer.writerow(['Title', 'PR_Number', 'Body', 'State', 'Created_At', 'Closed_At', 'User', 'Commits', 'Additions', 'Deletions', 'Changed_Files'])

        for pr in pull_requests:
            # Fetch additional details for each PR
            pr_detail_url = pr['url']
            pr_detail_response = requests.get(pr_detail_url)
            pr_detail = pr_detail_response.json()

            # Fetch commit data
            commits_url = pr_detail['commits_url']
            commits_response = requests.get(commits_url)
            commits_data = commits_response.json()
            num_commits = len(commits_data)

            # Fetch additions, deletions, and changed files data (if available)
            additions = pr_detail.get('additions', 0)
            deletions = pr_detail.get('deletions', 0)
            changed_files = pr_detail.get('changed_files', 0)

            # Write data to CSV
            writer.writerow([
                pr_detail.get('title'), pr_detail.get('number'), pr_detail.get('body'),
                pr_detail.get('state'), pr_detail.get('created_at'), pr_detail.get('closed_at'),
                pr_detail.get('user', {}).get('login'), num_commits, additions, deletions, changed_files
            ])


def fetch_and_save_user_data(usernames):
    csv_file = "users.csv"

    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Username', 'Repositories', 'Followers', 'Following', 'Contributions'])

        for username in usernames[-10:]:
            user_url = f"https://api.github.com/users/{username}"
            user_response = requests.get(user_url)
            user_data = user_response.json()

            if '[bot]' in username:
                followers = 'NA'
                following = 'NA'
                repos = 'NA'
            else:
                followers = user_data.get('followers')
                following = user_data.get('following')
                repos = user_data.get('public_repos')

            # Extract needed data w/ web scraping
            result = requests.get(f'https://github.com/{username}')
            content = result.content
            soup = BeautifulSoup(content, "html.parser")

            found_contributions = soup.find('h2', {'class': "f4 text-normal mb-2"})  # .text.strip()
            if found_contributions is not None:
                found_contributions = str(found_contributions.text.strip())
                contributions = re.split("\s", found_contributions)[0]
            else:
                contributions = 'NA'

            writer.writerow([
                username,
                repos,
                followers,
                following,
                contributions
            ])

def extract_usernames_from_prs(csv_file):
    usernames = set()
    try:
        with open(csv_file, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Assuming the username column is labeled 'User' in your CSV
                usernames.add(row['User'])
    except FileNotFoundError:
        print(f"File not found: {csv_file}")
    except Exception as e:
        print(f"An error occurred: {e}")

    return list(usernames)

if __name__ == "__main__":
    main_menu()
