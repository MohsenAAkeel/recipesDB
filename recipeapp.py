import re
import requests
from bs4 import BeautifulSoup
import readBa
from parseIngs import *
from sqlprep import *

sites = {'bonappetit':readBa.readBa}

def readForBa(obj):
    title = obj.find('title')
    if(title):
        read = re.search('Bon Appetit', title.text)
        if(read):
            return True
    return False


"""
Method for retrieval of url data in bs4 format
@params: 
	url - recipe source site
@return: 
	 parsed url and string containing the sites name

"""
def readUrl(url):
    page = requests.get(url)
    parsed = BeautifulSoup(page.content, 'html.parser')
    site = ''

    #check url source
    if(readForBa(parsed)):
        site = 'bonappetit'

    return parsed, site



def recipeApp(url, cat):
    parsedObj, site = readUrl(url)
    
    title, ingObj, steps = sites.get(site)(parsedObj)
    ings = parseIngs(ingObj)
    
    mysqlExport([title, url, cat, ings, steps])
    
    for x in ings:
        print(x)

    print()

    for x in steps:
        print(x)
    

    
    
    
