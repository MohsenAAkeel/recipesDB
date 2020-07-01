from bs4 import BeautifulSoup

fractions = {'¼':'.25', '½':'.5', '¾':'.75'}
measures = ['tbsp.', 'cups', 'cup', 'tsp.', 'pinch'] 

def readItem(item):
    amt = ''
    frac = ''
    ing = ''
    i = 0
    
    while i < len(item):
        if ord(item[i]) < 58 and ord(item[i]) > 47:
            amt += item[i]
        elif ord(item[i]) > 187 and ord(item[i]) < 191:
            frac += item[i]
        elif ord(item[i]) == 32:
            continue
        else:
            if i > 0:
                i+=1
            break
        i+=1
        
    #add the fractional value to the amount
    if len(frac) == 1:
        amt += fractions[frac]

    #collect the ingeredient
    while i < len(item):
        ing += item[i]
        if ing in measures:
            amt += ing
            ing = ''
        i+=1

    return [amt, ing]
        

def parseIngs(ingList):
    ingObj = []
    for item in ingList:
        print(item)
        ingObj.append(readItem(item))
        
    return ingObj
        
