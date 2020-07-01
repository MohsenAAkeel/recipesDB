import mysql.connector
from mysql.connector import errorcode
import config.py


def mysqlExport(data)
	try:
            cnx = mysql.connector.connect(**config)
        except mysql.connector.Error as error:
            if err.errno == errorcode.ER_BAD_DB_ERROR:
                print("DB does not exist")
            elif err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Access to your DB was denied")
            else:
                print(err)

        cursor = cnx.cursor
        
        #data[0] is the title, data[1] is the URL, data[2] is
        #the category
        add_recipe = (f"INSERT INTO recipes VALUES"
                      "({data[0], data[1], data[2]})")

        #Need the recipe ID
        recipeIdQuery = ("SELECT recID FROM recipes WHERE name = %s")
        cursor.execute(recipeIdQuery, data[0])
        recId = cursor[0]

        

        
        #data[3] holds the ingredients
        addIngs = []
        for x in data[3]:
            #x[0] holds the amount, x[1] holds name, x[2] holds processing
            #Need the item ID if it exists. IF it doesn't we need to add
            #the ingredient to the item table
            itemQuery = ("SELECT itemID FROM items WHERE name = %s AND process = %s")
            cursor.execute(itemQuery, (x[1], x[2]))
            if not cursor:
                addItem = ("INSERT INTO items VALUES (%s, %s)")
                cursor.execute(addItem, (x[1], x[2]))
                itemQuery = ("SELECT itemID FROM items WHERE name = %s AND process = %s")
                cursor.execute(itemQuery, (x[1], x[2]))

            itemId = cursor[0]
            addIngs.append(("INSERT INTO ingredients VALUES (%i, %s, %i)", (recId, x[0], itemId)))

        for elem in addIngs:
            cursor.execute(elem[0], elem[1])


        #data[4] holds the instructions
        add_instr = []
        for x in data[4]:
            #x[0] has the step num, x[1] the instr
            add_instr.append(("INSERT INTO process VALUES (%i, %i, %s)", (recId, x[0], x[1])))

        for elem in add_instr:
            cursor.execute(elem[0], elem[1])

        
