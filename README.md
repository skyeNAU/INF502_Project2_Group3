# GitHub Data Analytics Project
NAU informatics 502: Software Development Methodologies
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
