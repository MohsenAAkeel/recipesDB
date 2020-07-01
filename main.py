import pysftp
import recipeapp

'''
with pysftp.Connection('12.42.205.8', username='abuakeel', password='Meez!914802377') as sftp:
    print("connected")
    print(sftp.pwd)
'''

url = "https://www.bonappetit.com/recipe/old-school-tiramisu"

recipeapp.recipeApp(url)






