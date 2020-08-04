import requests
from bs4 import BeautifulSoup as bs
import json
import re


def pars_str(str):
    outstr = ''
    for i, c in enumerate(str):
        if c != ' ' or str[i-1] != ' ':
            outstr = outstr + c
    outstr1 = ''
    for c in outstr:
        if c != '\n' and c != '\r':
            outstr1 = outstr1 + c
    return outstr1

week_chisl = []
req = requests.get(url = 'http://pnu.edu.ru/rasp/groups/62172/?semester_id=21')
soup = bs(req.content, 'html.parser')


table = soup.find_all('table', attrs = {'class': 'rasp'})
tr = table[0].find_all('tr', attrs = {'class' : ['firstline weektype-1', 'firstline lastline']})
tr2 = table[0].find_all('tr', attrs = {'class' : ['lastline', 'firstline']})
for i in tr2:
    if not i.find('td', attrs = {'class' : 'time-weektype weektype-0'}):
        tr2.remove(i)
tr.extend(tr2)
td = tr[4].find_all('td', attrs = {'class' : 'time-discipline'})


print(td[0])
