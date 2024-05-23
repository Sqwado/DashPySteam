from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

@app.route('/')
def home():
    # Charger les données depuis un fichier CSV dans un DataFrame
    df = pd.read_csv('games.csv', encoding = 'utf-8')
    
    df = df.head(10)
    
    # Convertir le DataFrame en dictionnaire pour le passer au template
    data = df.to_dict(orient='records')
    
    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)
