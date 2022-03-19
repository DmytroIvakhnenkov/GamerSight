import urllib
from bs4 import BeautifulSoup
URL = "https://en.wikipedia.org/wiki/List_of_beat_%27em_ups"
source = urllib.request.urlopen(URL)
data = source.read().decode().strip()
soup = BeautifulSoup(data, 'html.parser')
list_games = soup.find_all('i')
for elem in list_games:
    for string in elem.parent.strings:
        print(string, end = "")
    print("\n")
