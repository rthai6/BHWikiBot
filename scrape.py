import re
import csv
import requests
from bs4 import BeautifulSoup

def scrapefamiliar(result={}):
    def firstrow(row, dic):
        dic['name'] = row['id'].replace('_', ' ').replace(".27", "'")
        data = row.findAll('td')
        dic['rarity'] = data[0]['class'][0].capitalize()

        dic['image'] = data[0].find('span').find('img')['data-src']
        dic['power'] = data[3].find('b').text
        dic['skills'] = []
        for skill in data[4:]:
            dic['skills'].append({'name': skill.text})
        
    def secondrow(row, dic):
        data = row.findAll('td')
        dic['stamina'] = data[1].find('b').text
        for index, skill in enumerate(data[2:]):
            dic['skills'][index]['target'] = skill.text
        
    def thirdrow(row, dic):
        data = row.findAll('td')
        dic['location'] = data[0].text
        dic['agility'] = data[2].find('b').text
        for index, skill in enumerate(data[3:]):
            dic['skills'][index]['values'] = skill.text

    response = requests.get('http://bit-heroes.wikia.com/wiki/Familiar?action=render')
    html = response.content
    soup = BeautifulSoup(html, "html.parser")
    for table in soup.findAll('table', attrs={'data-collapsetext': 'Hide'}):
        rows = table.findAll('tr')
        i = 1 # skip table name
        while i < len(rows):
            dic = {'type':'familiar'}
            firstrow(rows[i], dic)
            secondrow(rows[i+1], dic)
            thirdrow(rows[i+2], dic)
            pattern = re.compile('[\W_]+', re.UNICODE)
            result[pattern.sub('', dic['name']).lower()] = dic # for case and whitespace and symbol-insensitive searching
            i += 3
    return result

def scrapefusion(result={}):
    def firstrow(row, dic):
        dic['name'] = row['id'].replace('_', ' ').replace(".27", "'")
        data = row.findAll('td')
        dic['rarity'] = data[0]['class'][0].capitalize()
        if data[0].find('span'):
            dic['image'] = data[0].find('span').find('img')['data-src']
        dic['power'] = data[3].find('b').text
        dic['skills'] = []
        for skill in data[4:]:
            dic['skills'].append({'name': skill.text})

    def secondrow(row, dic):
        data = row.findAll('td')
        dic['bonus'] = data[0].text
        dic['stamina'] = data[2].find('b').text
        for index, skill in enumerate(data[3:]):
            dic['skills'][index]['target'] = skill.text
        
    def thirdrow(row, dic):
        data = row.findAll('td')
        dic['recipe'] = data[0].text
        dic['agility'] = data[2].find('b').text
        for index, skill in enumerate(data[3:]):
            dic['skills'][index]['values'] = skill.text

    response = requests.get('http://bit-heroes.wikia.com/wiki/Fusion?action=render')
    html = response.content
    soup = BeautifulSoup(html, "html.parser")
    for table in soup.findAll('table', attrs={'data-collapsetext': 'Hide'}):
        rows = table.findAll('tr')
        i = 1 # skip table name
        while i < len(rows):
            dic = {'type':'fusion'}
            firstrow(rows[i], dic)
            secondrow(rows[i+1], dic)
            thirdrow(rows[i+2], dic)
            pattern = re.compile('[\W_]+', re.UNICODE)
            result[pattern.sub('', dic['name']).lower()] = dic # for case and whitespace and symbol-insensitive searching
            i += 3
    return result

def scrapemythic(result={}):
    def firstrow(row, dic):
        data = row.findAll('td')
        if data[0].find('span'):
            dic['image'] = data[0].find('span').find('img')['data-src']
        dic['name'] = data[1].find('b').text.replace('_', ' ').replace(".27", "'")
        dic['type'] = data[2].find('b').text
        dic['tier'] = data[3].find('b').text
#        pattern = re.compile('[(].+[)]')
        if data[4].find('b'):
            dic['power'] = data[4].find('b').text
        if data[5].find('b'):
            dic['stamina'] = data[5].find('b').text
        if data[6].find('b'):
            dic['agility'] = data[6].find('b').text

    def secondrow(row, dic):
        data = row.findAll('td')
        dic['location'] = data[0].text
        
    response = requests.get('https://bit-heroes.wikia.com/wiki/List_of_mythic_equipment')
    html = response.content
    soup = BeautifulSoup(html, "html.parser")
    tables = soup.findAll('table')
    rows = tables[2].findAll('tr')
    i = 1 # skip table name
    # first item is special case...
    # image from src instead of data-src
    dic = {}
    row = rows[i]
    data = row.findAll('td')
    if data[0].find('span'):
        dic['image'] = data[0].find('span').find('img')['src']
    dic['name'] = data[1].find('b').text.replace('_', ' ').replace(".27", "'")
    dic['type'] = data[2].find('b').text
    dic['tier'] = data[3].find('b').text
    if data[4].find('b'):
        dic['power'] = data[4].find('b').text
    if data[5].find('b'):
        dic['stamina'] = data[5].find('b').text
    if data[6].find('b'):
        dic['agility'] = data[6].find('b').text
    row = rows[i+1]
    data = row.findAll('td')
    dic['location'] = data[0].text
    pattern = re.compile('[\W_]+', re.UNICODE)
    result[pattern.sub('', dic['name']).lower()] = dic # for case and whitespace and symbol-insensitive searching
    result['pewpew'] = dic # nickname for laser
    i += 2
    while i < len(rows):
        dic = {}
        firstrow(rows[i], dic)
        secondrow(rows[i+1], dic)
        pattern = re.compile('[\W_]+', re.UNICODE)
        result[pattern.sub('', dic['name']).lower()] = dic # for case and whitespace and symbol-insensitive searching
        i += 2
    return result
    
if __name__ == "__main__":
#    scrapemythic()
    print(scrapemythic())
    pass
