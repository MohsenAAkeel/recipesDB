from bs4 import BeautifulSoup

fractions = {'¼':'.25', '½':'.5', '¾':'.75'}
measures = ['tbsp.', 'tbsp', 'tbsps', 'tbsps.',
            'tsp.', 'tsp', 'tsps', 'tsps.',
            'pinch',
            'oz.', 'oz', 'ozs',
            'lb', 'lb.', 'lbs', 'lbs.', 
            'cups', 'cup',] 

def readItem(item):
    amt = ''
    frac = ''
    ing = ''
    i = 0

    #get the amount and fraction (digits and unicode fractions)
    while i < len(item):
        if ord(item[i]) > 47 and ord(item[i]) < 58:
            amt += item[i]
        elif ord(item[i]) > 187 and ord(item[i]) < 191:
            frac += item[i]
        elif ord(item[i]) == 32:
            pass
        else: #breaks if the character is not a number or unicode fraction
            if ord(item[i]) == 46 and \
                (ord(item[i+1]) > 47 and ord(item[i+1]) < 58):
                amt += item[i]
            else:
                break
        i+=1
        
    if len(frac) == 1:
        amt += fractions[frac]

    iList = item[i:].split()
    i = 0

    if iList[0].lower() in measures:
        amt += iList[0].lower()
        i += 1

    return [amt, ' '.join(iList[i:])]
        

def parseIngs(ingList):
    ingObj = []
    for item in ingList:
        ingObj.append(readItem(item))
        
    return ingObj
        
