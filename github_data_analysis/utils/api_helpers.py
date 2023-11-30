import requests

def get_repository_info(owner, repo_name):     
    token = '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'
    headers = {'Authorization': f'token {token}'} if token else {}
    url = f"https://api.github.com/repos/{owner}/{repo_name}"

    try:
        response = requests.get(url)
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching repository data: {e}")
        return None

def get_user_profile(owner):
     user_url = f"https://api.github.com/users/{owner}"
     try:
      user_response = requests.get(user_url)
      if user_response.status_code == 404:
        return
      else:
         user_data = user_response.json()
         return user_data
     except requests.RequestException as e:
        print(f"Error fetching repository data: {e}")
        return None
