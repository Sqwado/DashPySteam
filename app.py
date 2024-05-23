from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

df = pd.read_csv('games.csv', encoding = 'utf-8')

def get_all_tags():
    tags = df['Tags']
    all_tags = []
    for i in range(len(tags)):
        if type(tags[i]) != str:
            continue
        this_tags = tags[i].split(',')
        for j in range(len(this_tags)):
            if this_tags[j] not in all_tags:
                all_tags.append(this_tags[j])
    all_tags.sort()
    return all_tags





@app.route('/')
def home():
    
    name = request.args.get('name')
    
    # Charger les données depuis un fichier CSV dans un DataFrame
    df = pd.read_csv('games.csv', encoding = 'utf-8')
    
    first = df.head()
    
    # Convertir le DataFrame en dictionnaire pour le passer au template
    data = first.to_dict(orient='records')
    
    tag = get_all_tags()
    
    return render_template('index.html', data=data, tag=tag)

if __name__ == '__main__':
    app.run(debug=True)
