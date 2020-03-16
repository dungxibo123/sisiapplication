from bs4 import BeautifulSoup
import requests

url = 'https://en.wikipedia.org/wiki/Member_states_of_the_United_Nations'

respondURL = requests.get(url)

soup = BeautifulSoup(respondURL.text,'html.parser')

table = soup.find('body').find('div', attrs = {'id': 'content','class': 'mw-body','role': 'main'}).find('div', attrs = {'id': 'bodyContent', 'class': 'mw-body-content'}).find('div', attrs = {'id': 'mw-content-text'}).find('div', attrs = {'class': 'mw-parser-output'}).find('table',attrs = {'class': 'wikitable sortable'})
#s = soup.find('body').find('div', attrs = {'id': 'content','class': 'mw-body','role': 'main'}).find('div', attrs = {'id': 'bodyContent', 'class': 'mw-body-content'}).find('div', attrs = {'class': 'mw-parser-output'})
#print(s)
infoList = table.find('tbody').find_all('tr')
countryList = []
#print(infoList[1])
for member in infoList:
    if member == infoList[0]: continue
    countryList.append(member.find_all('td')[1].find('a').get_text())

with open('nation.txt', 'w') as fp:
    for member in countryList:
        fp.write('{}\n'.format(member))
    
    



