import re
import csv
import requests
from bs4 import BeautifulSoup

def scrapefam():
    def firstrow(row, dic):
        dic['id'] = row['id'].replace('_', ' ').replace(".27", "'")
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
        dic['agility'] = data[2].find('b').text
        for index, skill in enumerate(data[3:]):
            dic['skills'][index]['values'] = skill.text

    result = {}
    response = requests.get('http://bit-heroes.wikia.com/wiki/Familiar?action=render')
    html = response.content
    soup = BeautifulSoup(html, "html.parser")
    for table in soup.findAll('table', attrs={'data-collapsetext': 'Hide'}):
        rows = table.findAll('tr')
        i = 1 # skip table name
        while i < len(rows):
            dic = {}
            firstrow(rows[i], dic)
            secondrow(rows[i+1], dic)
            thirdrow(rows[i+2], dic)
            pattern = re.compile('[\W_]+', re.UNICODE)
            result[pattern.sub('', dic['id']).lower()] = dic # for case and whitespace and symbol-insensitive searching
            i += 3
    return result

def scrapefus():
    def firstrow(row, dic):
        dic['id'] = row['id'].replace('_', ' ').replace(".27", "'")
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

    result = {}
    response = requests.get('http://bit-heroes.wikia.com/wiki/Fusion?action=render')
    html = response.content
    soup = BeautifulSoup(html, "html.parser")
    for table in soup.findAll('table', attrs={'data-collapsetext': 'Hide'}):
        rows = table.findAll('tr')
        i = 1 # skip table name
        while i < len(rows):
            dic = {}
            firstrow(rows[i], dic)
            secondrow(rows[i+1], dic)
            thirdrow(rows[i+2], dic)
            pattern = re.compile('[\W_]+', re.UNICODE)
            result[pattern.sub('', dic['id']).lower()] = dic # for case and whitespace and symbol-insensitive searching
            i += 3
    return result
    
if __name__ == "__main__":
    print(scrapefus())