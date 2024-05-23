# coding: utf-8

import pandas as pd
import cgi

df = pd.read_csv('games.csv', encoding = 'utf-8')


form = cgi.FieldStorage()
print("Content-type: text/html; charset=utf-8\n")
html = """<!DOCTYPE html>
<head>
 <title>Mon programme</title>
 <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="w-screen h-screen bg-[#1B2838]">
<header class="w-screen h-1/6 bg-[#171D25] flex">
    <div class="w-1/6 h-full">
        <img src="logo_steam.png" alt="logo steam"/>
    </div>
    <nav class="w-4/6 h-full flex items-center justify-center">
       <input class="h-2/6 w-2/6 rounded p-2 text-white bg-[#1B2838]" placeholder="Recherchez le nom d'un jeu..."/>
    </nav>
    <div class="w-1/6 h-full">
         <div class="w-full h-1/6 flex justify-end text-white pr-2">
             <a href="#">CRUD </a>
             <a href="#"> | Text |</a>
             <a href="#">Courbe</a>
         </div>
    </div>
</header>
<main class="w-screen h-5/6 flex ">
    <aside class="w-1/6 h-full bg-[#171D25] "></aside>
    <article class="w-4/6 h-full bg-blue-500"></article>
    <div class="w-1/6 h-full bg-blue-600"></div>
</main>
</body>
</html>
"""
print(html)
