from bs4 import BeautifulSoup
import lxml
import requests

r = requests.get('https://www.sudokuweb.org/')
soup = BeautifulSoup(r.text, 'lxml')
print(soup.table)
