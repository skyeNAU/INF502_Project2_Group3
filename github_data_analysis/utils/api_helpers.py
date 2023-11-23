import requests

def get_repository_info(owner, repo_name):
    url = f"https://api.github.com/repos/{owner}/{repo_name}"
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()
    else:
        # Handle different HTTP statuses or log them
        print(f"Error fetching repository data: HTTP Status Code {response.status_code}")
        return None