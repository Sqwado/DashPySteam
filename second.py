# coding: utf-8
import cgi
form = cgi.FieldStorage()
print("Content-type: text/html; charset=utf-8\n")
html = """<!DOCTYPE html>
<head>
 <title>Mon programme</title>
</head>
<body>
<div>"""
html += form.getvalue("nom")+"<br>"+form.getvalue("prenom")+"\n"+form.getvalue("age")+"\n"+form.getvalue("adresse")+"\n"+form.getvalue("commentaire")
html += """
</div>
<button onclick="history.go(-1);">Retour</button>
</body>
</html>
"""
print(html)
