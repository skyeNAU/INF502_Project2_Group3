# GitHub Data Analytics Project
**NAU informatics 502: Software Development Methodologies**

This project aims to collect and analyze open source project data from GitHub to gain useful insights.That uses Python structures, file input and output, exceptions, and API usage. It focuses on writing a complex program that collects and analyzes data from GitHub repositories and developers' profiles.

## Overview
This console uses webscraping packages BeautifulSoup, pandas as pd, seaborn, and json.
GitHub hosts a vast collection of open source software projects and their evolution histories. This rich trove of metadata presents an opportunity to study software development trends, community dynamics and technologies over time through a data-driven lens.
This project extracts real data from GitHub to understand the dynamics of repositories and the developers who contribute to them using GitHub REST API and Python libraries. It stores the retrieved information into file. Analytics are then performed to glean insights, spot patterns, and enable databased decision making.
The goals are to:
- Systematically archive metadata from GitHub projects
- Understand project characteristics and relationships
- Analyze contributor activities and networks
- Identify emerging topics and technologies
- Support research through easily accessible datasets
- Enable exploratory analyses and hypothesis testing

## Implementation

### 1. Modules to Import
This includes importing necessary packages for a smooth program.
```python
import requests
import csv
import pandas as pd
import matplotlib.pyplot as mp
import seaborn as sb
import numpy as np
import json
from datetime import datetime
from bs4 import BeautifulSoup
import re
```

### 2. Defining a Repository Class

We define a class GitHubRepository for a Git Hub Repository. It contains attributes such as repo_name, owner, description, homepage, license, forks, watchers, and date_of_collection.

```python
class GitHubRepository:
    def __init__(self, name, owner, description, homepage, license, forks, watchers, date_of_collection):
        self.name = name
        self.owner = owner
        self.description = description
        self.homepage = homepage
        self.license = license
        self.forks = forks
        self.watchers = watchers
        self.date_of_collection = date_of_collection

    def __str__(self):
        return f"{self.owner}/{self.name}: {self.description} ({self.watchers})"

    def to_csv_row(self):
        return [self.name, self.owner, self.description, self.homepage, self.license, self.forks, self.watchers, self.date_of_collection]
```

### 3. Defining a Pull Request Class

There is another class definition called PullRequest, which represents a GitHub pull request. It has attributes like title, number, body, state, created_at, closed_at, and user.

```python
class PullRequest:
    def __init__(self, title, number, body, state, created_at, closed_at, user):
        self.title = title
        self.number = number
        self.body = body
        self.state = state
        self.created_at = created_at
        self.closed_at = closed_at
        self.user = user

    def __str__(self):
        return f"PR: {self.title}, Number: {self.number}, State: {self.state}, Created At: {self.created_at}, Closed At: {self.closed_at}, User: {self.user}"

    def to_csv_row(self):
        return f"{self.title},{self.number},{self.body},{self.state},{self.created_at},{self.closed_at},{self.user}"
```
### 4. Console

Our program functions through in a console which prompts the user with several options. In each of these choices, there are further menus with more specific options. The user has the choice to 1.) Collect data for a specific repository, 2.) Show all repositories, 3.) Create visualizations, 4.) Calculate correlations, 5.) Access the user profile, or 6.) Exit the program.

Each of these options functionality comes from defined functions which are detailed below.

### 5. Collected Repository Data

To collect repository data, a function api_limit_warning is initialized and prompts the user further with options that distinguish between retrieving the last 10 pull requests or retrieving all pull requests.

```python
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
```

The functions collect_repository_data and collect_ALL_repository_datause several subroutine functions:

get_repository_info(),
fetch_and_save_pull_requests(),
extract_usernames_from_prs(), and
fetch_and_save_user_data().

An object is created for the GitHub Repository, and the headers and appropriate data are saved in a CSV file.

### 6. Show All Repositories 

For the second option in the console, a function show_all_repositories reads the respositories.csv file and allows the user to enter the repository number to perform actions on.A function perform_actions_on repository allows the user to show pull requests or see a summary of the repository. The show_pull_requests function reads the saved repository csv file and prints the number of pull requests.



```python
def show_pull_requests(owner, repo_name):
    try:
        with open(f'repos/{owner}-{repo_name}.csv', mode='r', newline='', encoding='utf-8') as file:
            reader = pd.read_csv(file)
            print(f"Pull Requests for {repo_name}:")
            pd.set_option('display.max_columns', None)
            print(reader)
    except Exception as e:
        print(f"An error occurred: {e}")
```

### 7. Getting Profile Data

A function get_user_profile allows the user to serach GitHub Accounts by username and returns various statistics about the profile including number of repositories, follower count, number of contributions, and more. 

```python
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
         try:
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
         except:
             print('API Rate Limit Exceeded. Please wait and try again.')
    ``` 



### 8. Visualizations Menu

The implementation of function called visulaization_menu allows the user to access a number of visualization creation features. The function prompts the user for a respository owner's username as well as the name of the respository, at which point a csv file path is constructed. Now the user is able to choose among but not limited too the options of creating a box plot of commits in open and closed pull requests, a box plot of additions and deletions in pull requests, line graphs of PR's per day, bar plots of users per repository, and calculating correlations.
The subroutines of this function implement visualization functions that read the csv from the defined file path and construct the figures. These functions are stored in respository_visualizations.py and will return error messages if the csv files are empty.
The calculate_correlations function in particular returns a heat map visualization of a correlation matrix.


# 9. Calculating Correlations

```python
def calculate_correlations():
    try:
        # Load data
        df = pd.read_csv('users.csv')

        # Select only the numerical columns
        numerical_data = df.select_dtypes(include=['int64', 'float64'])

        # Calculate correlation matrix
        correlation_matrix = numerical_data.corr()

        # Display the correlation matrix
        print("Correlation matrix:")
        print(correlation_matrix)

        # plotting correlation heatmap
        dataplot = sb.heatmap(correlation_matrix, cmap="YlGnBu", annot=True)

        # displaying heatmap
        plt.show()

    except FileNotFoundError:
        print("The repositories.csv file does not exist. Please collect data first.")
    except Exception as e:
        print(f"An error occurred: {e}")
``` 

### 10. Extract user and pull request count

A function called extract_user_pull_request_count is provided to extract the number of pull requests for each user. It takes a list of PullRequest objects as input and returns a dictionary with user as the key and the count of pull requests as the value.

```python
def extract_user_pull_request_count(pull_requests):
    # Function definition goes here

pull_request_count = extract_user_pull_request_count(pull_requests)
```

### 5. Scrape data from user profile page on GitHub

This section demonstrates how to scrape data from a user's profile page on GitHub. It uses the BeautifulSoup library to parse the HTML content and extract information such as the number of repositories, followers, following, and contributions.

```python
result = requests.get('https://github.com/username')
content = result.content
soup = BeautifulSoup(content, "html.parser")

# Extract required information
repositories_count = soup.find('span', {'class': 'Counter'}).text.strip()
followers_count = soup.find_all('span', {'class':"text-bold color-fg-default"})[0].text.strip()
following_count = soup.find_all('span', {'class':"text-bold color-fg-default"})[1].text.strip()
contributions = soup.find('h2', {'class':"f4 text-normal mb-2"}).text.strip().split()[0]
```

## Usage

To use the project, first clone the GitHub repository:

```
# Example
git clone https://github.com/your-repo/github-data-analysis
```

Install required packages:

```
# File that contains all packages
pip install -r packages.py
```

Then run the app.py file:

```
python app.py
``` 

This launches an interactive menu driven CLI interface. The main options are:

- Collect Data: Enter repo owner and name, data is fetched and stored
- List Repositories: View summary of stored repos  
- List Pull Requests: For a selected repo
- Show Repository Summary: Stats for a repo
- Run Analyses: Various plots and stats are generated
- Save Outputs: Figures and DataFrames to files

## Conclusion
 This GitHub repository serves as a comprehensive guide for working with GitHub using Python. It provides code and explanations for various functionalities, allowing users to interact with GitHub repositories and pull requests effectively.

By following the instructions provided in this repository, users can gain a better understanding of how to leverage Python to interact with GitHub programmatically. They will be equipped with the knowledge and tools to analyze repository data, manage pull requests, and scrape user profiles for valuable insights.

We encourage users to explore the source code, experiment with different functionalities, and adapt the examples to suit their specific needs.

We hope that this GitHub repository serves as a valuable resource for developers, researchers, and anyone interested in utilizing Python to enhance their GitHub experience. Happy coding!

