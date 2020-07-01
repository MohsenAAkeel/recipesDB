import regex
import requests
from bs4 import BeautifulSoup

def readBa(obj):
    #Get the recipe name
    titleObj = obj.find('title')
    title = regex.search('((\D*\d*)\s*)*(?= | Bon Appetit)', titleObj.text)
    title = title.group(0)
    
    #Get the ingredients
    block = obj.find('ul', class_='ingredients__group')
    itList = block.find_all('li', class_='ingredient')
    ings = [x.text for x in [y.find('div', class_="ingredients__text") for y in itList]]

    #Get the instructions
    block = obj.find('ul', class_='steps')
    itList = block.find_all('li')
    steps = []

    for x in itList:
        steps.append(x.find('div').find('p').text)

    return title, ings, steps
