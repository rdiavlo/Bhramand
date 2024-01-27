
from bs4 import BeautifulSoup


with open("website.html", "r+", encoding="utf8") as file:
    r = file.read()


soup = BeautifulSoup(r, "html.parser")

print(soup.title)
print(soup.li)



print()


k = soup.findAll(name="li", class_="6")
print([i.text for i in k])


