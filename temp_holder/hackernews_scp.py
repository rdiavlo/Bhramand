import requests
from bs4 import BeautifulSoup

url="https://news.ycombinator.com/"
response = requests.get(url=url)

soup = BeautifulSoup(response.text, "html.parser")


# print(soup)

titles = soup.find_all("span", class_="titleline")
titles = [i.text for i in titles]
print(len(titles))
print(titles)
    
    
upvotes = soup.find_all("span", class_="score")
upvotes = [int(i.text.split(" ")[0]) for i in upvotes]
print(len(upvotes))
print(upvotes)


users = soup.find_all("a", class_="hnuser")
users = [i.text for i in users]
print(len(users))
print(users)


assert  len(titles) == len(upvotes) == len(users); "The counts do not match signore"