import requests
from bs4 import BeautifulSoup
import re

user_list = list(pullrequest_count.keys())

def get_user_data(user_list):
    userdata_list = []
    for username in user_list:
      user_pull_request_count = pullrequest_count[username]

      result = requests.get('https://github.com/' + username)
      content = result.content
      soup = BeautifulSoup(content, "html.parser")

      # Extract the required information
      repositories_count_element = soup.find('span', {'class': 'Counter'})
      repositories_count = repositories_count_element.text.strip() if repositories_count_element else 'N/A'

      if '[bot]' in username:
        followers_count = 'NA'
        following_count = 'NA'
        contributions = 'NA'
      else:
        try:
          followers_following = soup.find_all('span', {'class':"text-bold color-fg-default"})#.text.strip()
          followers_count = followers_following[0].text.strip()
          following_count = followers_following[1].text.strip()
        except:
          followers_count = 'NA'
          following_count = 'NA'

        contributions = soup.find('h2', {'class':"f4 text-normal mb-2"}).text.strip()
        contributions= re.split("\s", contributions)[0]

      ud = UserList(username,user_pull_request_count,repositories_count,followers_count,following_count,contributions)
      userdata_list.append(ud)

      # Save this object to CSV
      save_as_csv('users.csv', userdata_list)
      

