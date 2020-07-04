import mysql.connector
from mysql.connector import errorcode
from config import *
#import sqlutils.py
#import utils.py


"""
Method for adding values to the "recipes" table
@params: recipeList - list containing 3 values: title, url, and catagory
@returns: integer value representing the error code generated
"""
def errorOut(errval):
    ERROR_CODES = {
        0 : "No error",
        'DUPLICATE_RECIPE_NAME' : "Recipe exists in DB",
        2 : ""
    }
    print(f"Error: {ERROR_CODES[errval]}")
    return



"""
Helper function
Method for returning associated recId attribute of the record
with the matching name.
@params: 
    name - the name of the recipe, matched against name attribute values
    cursor - the bs4 access point to the mysql CLI (from connect.cursor)
"""
def getRecId(name, cursor):
    try:
        query = "SELECT recId FROM recipes WHERE name = %s;"
        cursor.execute(query, (name,))
    except mysql.connector.Error as err:
        print( "ERROR: {}".format(err))
    return cursor.fetchall()[0][0]



"""
Method for adding values to the "recipes" table
@params: rList - recipe list containing 3 values: name, url, and catagory
@returns: integer value representing the error code generated
"""
def addRecipe(rList, cursor, cnx):
    data_recipe = {
        'name':rList[0],
        'source':rList[1],
        'cat':rList[2]
    }

    """
    Ensure this is not a duplicate by checking the database
    for the title
    """
    try:
        query = ("SELECT * FROM recipes WHERE name = %s;")
        cursor.execute(query, (rList[0],))
    except mysql.connector.Error as err:
        print( "ERROR: {}".format(err))
    
    if not cursor:
        return None, 'DUPLICATE_RECIPE_NAME'
    
    """
    The recipe name does not exist in the database
    
    Add the title, source url, and catagory into the recipes
    table.

    rList[0] is the name, rList[1] is the URL, rList[2] is
    the category
    """
    add_recipe = ("INSERT INTO recipes (name, source, cat) VALUES (%(name)s, %(source)s, %(cat)s);")

    try:
        cursor.execute(add_recipe, data_recipe)
        cnx.commit()
    except mysql.connector.Error as err:
        print( "ERROR: {}".format(err))

    return getRecId(rList[0], cursor), 0

"""
helper function
collects the itemId value from the :items: table for records with 
a matching name
"""
def getItemId(name, cursor):
    try:
        itemQuery = ("SELECT itemID FROM items WHERE name = %s;")
        cursor.execute(itemQuery, (name,))
    except mysql.connector.Error as err:
        print( "ERROR: {}".format(err))


    
"""
helper function
adds a record to the :items: table 
"""
def addItem(item, cursor, cnx):
    try:
        addAction = ("INSERT INTO items (name) VALUES (%s);")
        cursor.execute(addAction, (item,))
        cnx.commit()
    except mysql.connector.Error as err:
        print( "ERROR: {}".format(err))
        
    
"""
Method for adding values to the "recipes" table
@params: recipeList - list containing 3 values: title, url, and catagory
@returns: integer value representing the error code generated
"""
def addIngs(recId, ingList, cursor, cnx):

    ingRecs = []
    
    #Add the food/drink item to the database
    #ingList holds the ingredients
    for e in ingList:
        #e[0] = amount
        #e[1] = name
        getItemId(e[1], cursor)
        if cursor.rowcount == 0:
            addItem(e[1], cursor, cnx)
            getItemId(e[1], cursor)
            
        itemId = cursor.fetchall()[0][0]        

        data_ing = {
            'recId' : recId,
            'amt' : e[0],
            'itemId' : itemId
        }
            
        #itemId was collected and data can be input into "items" table
        ingRecs.append(["INSERT INTO ingredients (recId, amt, itemId)  VALUES (%(recId)s, %(amt)s, %(itemId)s);",
                        data_ing])

    for ing in ingRecs:
        try:
            cursor.execute(ing[0], ing[1])
            cnx.commit()
        except mysql.connector.Error as err:
            print( "ERROR: {}".format(err))
            
    return 0



"""
Method for adding values to the :recipes: table
@params: recipeList - list containing 3 values: title, url, and catagory
@returns: integer value representing the error code generated
"""
def addSteps(recId, steps, cursor, cnx):
    #will hold list of sql commands to execute
    instrRecs = []
    
    for i in range(len(steps)):
        instrRecs.append(["INSERT INTO process (recId, step, instr) VALUES (%s, %s, %s);", (recId, i, steps[i])])

    try:
        for e in instrRecs:
            cursor.execute(e[0], e[1])
            cnx.commit()
    except mysql.connector.Error as err:
        print( "ERROR: {}".format(err))
        
    return 0



"""
Method for adding values to the :recipes: table
@params: recipeList - list containing 3 values: title, url, and catagory
@returns: integer value representing the error code generated
"""
def mysqlExport(data):
    """
    structure of
    data [
        title,       #0
        site,        #1
        catagory,    #2
        ingredients, #3
        steps        #4
    ]

    """
    try:
        cnx = mysql.connector.connect(**config)
    except mysql.connector.Error as error:
        if err.errno == errorcode.ER_BAD_DB_ERROR:
            print("DB does not exist")
        elif err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Access to your DB was denied")
        else:
            print(err)

    #create the cursor - allows for execution of mysql commands
    #through python
    cursor = cnx.cursor(buffered = True)

    """
    add the record to the :recipes: table
    """
    recId, errval = addRecipe(data[:3], cursor, cnx)
    if errval != 0:
        errorOut[errval]
        return

    """
    Add the food/liquid items to the :items: table data[3] holds the 
    ingredients list. 
        data[3][0] holds the amount
        data[3][1] holds the name
    Want to only send a list of names to add
    """
    errval = addIngs(recId, data[3], cursor, cnx)
    if errval != 0:
        errorOut[errval]
        return

    errval = addSteps(recId, data[4], cursor, cnx)
    


        
