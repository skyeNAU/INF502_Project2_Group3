# GitHub Data Analytics Project
**NAU informatics 502: Software Development Methodologies**

This project aims to collect and analyze open source project data from GitHub to gain useful insights.That uses Python structures, file input and output, exceptions, and API usage. It focuses on writing a complex program that collects and analyzes data from GitHub repositories and developers' profiles.

## Overview
GitHub hosts a vast collection of open source software projects and their evolution histories. This rich trove of metadata presents an opportunity to study software development trends, community dynamics and technologies over time through a data-driven lens.
This project extracts real data from GitHub to understand the dynamics of repositories and the developers who contribute to them using GitHub REST API and Python libraries. It stores the retrieved information in structured SQL and NoSQL databases for efficient querying and retrieval. Analytics are then performed to glean insights, spot patterns, and enable databased decision making.
The goals are to:
- Systematically archive metadata from GitHub projects
- Understand project characteristics and relationships
- Analyze contributor activities and networks
- Identify emerging topics and technologies
- Support research through easily accessible datasets
- Enable exploratory analyses and hypothesis testing

## Requirements

The primary objective of this project is to develop a comprehensive application that collects and analyzes data from GitHub repositories and developers' profiles. By working with real data, you will gain practical experience in Python programming, including working with APIs, handling JSON data, file input/output, and data analysis using libraries such as Pandas.
To ensure a well-rounded approach, the project requirements are designed to cover various aspects:

1. **Unit Tests**: Write at least 5 unit tests to validate the functionality of your application. This will demonstrate your ability to implement robust test cases and ensure the reliability of your code.

2. **Object-Oriented Programming (OOP)**: Utilize the principles of OOP to structure your code effectively. Use classes and objects to represent and manipulate the data collected from GitHub. This approach will enhance code organization and maintainability.

3. **Data Collection - Repositories**: Collect crucial information about repositories from GitHub, including the repository name, owner, description, homepage, license, number of forks, number of watchers, and the date of data collection itself. When printing the object representing a repository, it should be displayed in the format '<owner>/<repository_name>: <description> (<watchers>)'.

4. **Data Collection - Pull Requests**: Retrieve the pull requests from the first page of a specific query for each repository. For each pull request, gather pertinent information such as the title, number, body, state, creation date, closing date (if applicable), user, and statistics related to commits, additions, deletions, and changed files. To collect this information, utilize the query format: `https://api.github.com/repos/<owner>/<repository>/pulls/<number>`.

5. **Data Collection - User Profiles**: For each author (user) found in the pull requests, collect their username and determine the number of pull requests they have made. Additionally, scrape the user's GitHub profile to obtain further details such as the number of repositories, number of followers, number of following, and number of contributions in the last year.

6. **CSV Data Storage**: Develop a reusable function called `save_as_csv` that converts any object into a CSV entry (row). This function should take the file name and the object as parameters. If the file doesn't exist, it should create the file with a header. If the file already exists, it should append a new line with the object's data in CSV format. Each class should have a method with the same name (`save_as_csv`) that returns a string with the data structured as CSV. The data should be stored in the following files:
   - Repositories: `repositories.csv`
   - Pull Requests for each repository: `repos/<owner>-<repository>.csv`
   - Users: `users.csv`

7. **Console Application**: Implement a menu-driven console application that allows users to interact with the program. The menu should offer options such as:
   - Collect data for a specific repository
   - Display all collected repositories (with submenu options for each repository)
   - Show all pull requests from a specific repository
   - Provide a summary of a repository (including the number of open and closed pull requests, number of users, and date of the oldest pull request)
   - Generate visual representations of repository data using Pandas, such as boxplots comparing closed vs. open pull requests in terms of commits and additions/deletions, boxplots comparing the number of changed files grouped by author association, and scatterplots showing the relationship between additions and deletions.
   - Calculate the correlation between all numeric data in the pull requests for a repository.

## Implementation

### 1. Importing modules
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

### 2. Define a class for GitHub Repository

We will also find a class definition for GitHubRepository. This class represents a GitHub repository and contains attributes such as repo_name, owner, description, homepage, license, forks, watchers, and date_of_collection. Here is an example of how to define an instance of this class:

```python
class GitHubRepository:
    # Class definition goes here
```

### 3. Define a class for Pull Requests

There is another class definition called PullRequest, which represents a GitHub pull request. It has attributes like title, number, body, state, date_of_creation, closing_date, and user. Here's an example of how to use this class:

```python
class PullRequest:
    # Class definition goes here
```

### 4. Extract user and pull request count

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

