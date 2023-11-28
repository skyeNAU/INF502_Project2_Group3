import requests

def get_repository_info(owner, repo_name):     
    token = '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'
    headers = {'Authorization': f'token {token}'} if token else {}
    url = f"https://api.github.com/repos/{owner}/{repo_name}"

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching repository data: {e}")
        return None
