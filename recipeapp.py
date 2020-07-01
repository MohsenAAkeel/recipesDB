import regex
import requests
from bs4 import BeautifulSoup
import readBa
from parseIngs import *

sites = {'bonappetit':readBa.readBa}

def readUrlForBa(obj):
    title = obj.find('title')
    if(title):
        read = regex.search('Bon Appetit', title.text)
        if(read):
            return True
    return False
        
def readUrl(url):
    page = requests.get(url)
    parsed = BeautifulSoup(page.content, 'html.parser')
    site = ''
    #Check if url is to bonapetit
    if(readUrlForBa(parsed)):
        site = 'bonappetit'

    return parsed, site
    

def recipeApp(url):
    parsedObj, site = readUrl(url)

    title, ings, steps = sites.get(site)(parsedObj)

    ingObj = parseIngs(ings)

    pring(ingObj)
    
    
    