# coding: utf-8

import pandas as pd
import cgi

df = pd.read_csv('games.csv', encoding = 'utf-8')


form = cgi.FieldStorage()
print("Content-type: text/html; charset=utf-8\n")
html = """<!DOCTYPE html>
<head>
 <title>Mon programme</title>
</head>
<body>
 <form action="/second.py" method="post">
 <input type="text" name="nom" value="Votre nom" />
 <input type="text" name="prenom" value="Votre prenom" />
 <input type="number" name="age" value="18" />
 <input type="text" name="adresse" value="Votre adresse" />
 <input type="text" name="commentaire" value="Votre commentaire" />
 <input type="submit" name="send" value="Envoyer information au
serveur">
 </form>
</body>
</html>
"""
print(html)
