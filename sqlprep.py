import mysql.connector
from mysql.connector import errorcode
import config.py
import sqlutils.py
import utils.py


"""
Method for adding values to the "recipes" table
@params: recipeList - list containing 3 values: title, url, and catagory
@returns: integer value representing the error code generated
"""
def errorOut(errval):
    ERROR_CODES = {
        0 : "No error"
        'DUPLICATE_RECIPE_NAME' : "Recipe exists in DB"
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
        query = "SELECT recId FROM recipes WHERE name = %s;")
        cursor.execute(query, (name))
    except mysql.connector.Error as err:
        print( "ERROR: " + err)
    return cursor.fetchall()[0][0]



"""
Method for adding values to the "recipes" table
@params: rList - recipe list containing 3 values: name, url, and catagory
@returns: integer value representing the error code generated
"""
def addRecipe(rList):
    """
    Ensure this is not a duplicate by checking the database
    for the title
    """
    try:
        query = ("SELECT * FROM recipes WHERE name = %s;")
        cursor.execute(query, rList[0])
    except mysql.connector.Error as err:
        print( "ERROR: " + err)
    
    if not cursor:
        return None, 'DUPLICATE_RECIPE_NAME'
    
    """
    The recipe name does not exist in the database
    
    Add the title, source url, and catagory into the recipes
    table.

    rList[0] is the name, rList[1] is the URL, rList[2] is
    the category
    """
    try:
    	add_recipe = (f"INSERT INTO recipes VALUES (%s, %s, %s);")
    	cursor.execute(add_recipe, (rList[0], rList[1], rList[2]))
        return getRecId(rList[0], cursor), 0
    except mysql.connector.Error as err:
        print( "ERROR: " + err)



"""
helper function
collects the itemId value from the :items: table for records with 
a matching name
"""
def getItemId(name, cursor):
    try:
        itemQuery = ("SELECT itemID FROM items WHERE name = %s;")
        cursor.execute(itemQuery, (e))
    except mysql.connector.Error as err:
        print( "ERROR: " + err)


    
"""
helper function
adds a record to the :items: table 
"""
def addItem(item, cursor):
    try:
        addAction = ("INSERT INTO items (name) VALUES (%s);")
        cursor.execute(addAction, (item))
    except mysql.connector.Error as err:
        print( "ERROR: " + err)
        
    
"""
Method for adding values to the "recipes" table
@params: recipeList - list containing 3 values: title, url, and catagory
@returns: integer value representing the error code generated
"""
def addIngs(recId, ingList, cursor):

    ingRecs = []
    
    #Add the food/drink item to the database
    #ingList holds the ingredients
    for e in ingList:
        #e[0] = amount
        #e[1] = item
        if(not getItemId(e[1], cursor))
        itemId = cursor.fetchAll()

        if not itemId:
            addItem(e[1], cursor)
            getItemId(e[1], cursor)
            itemId = cursor.fetchAll()[0][0]
            
        #itemId was collected and data can be input into "items" table
        ingRecs.append(["INSERT INTO ingredients VALUES (%i, %s, %i);",
                        (recId, e, itemId)])

    for ing in ingRecs:
        try:
            cursor.execute(ing[0], ing[1])
        except mysql.connector.Error as err:
            print( "ERROR: " + err)
            
    return 0



"""
Method for adding values to the :recipes: table
@params: recipeList - list containing 3 values: title, url, and catagory
@returns: integer value representing the error code generated
"""
def addSteps(recId, steps, cursor):
    #will hold list of sql commands to execute
    instrRecs = []
    
    for i in range(len(steps)):
        instrRecs.append(["INSERT INTO process VALUES (%i, %i, %s);", (recId, i, steps[i])])

    try:
        for e in instr:
            cursor.execute(e[0], e[1])
    except mysql.connector.Error as err:
        print( "ERROR: " + err)
        
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
    cursor = cnx.cursor

    """
    add the record to the :recipes: table
    """
    recId, errval = addRecipe(data[:3])
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
    errval = addIngs(recId, data[3], cursor)
    if errval != 0:
        errorOut[errval]
        return

    errval = addSteps(recId, data[4], cursor)
    


        
