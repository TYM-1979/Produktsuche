from flask import Flask, request, render_template, jsonify
import pandas as pd
import os
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, Render!"

if __name__ == "__main__":
    # Render gibt den PORT über die Umgebungsvariable vor
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

app = Flask(__name__)

# Google Sheet Daten laden
def get_google_sheet():
    url = 'https://docs.google.com/spreadsheets/d/1U1zEsvrKYusXVxwShOfXIOv90pl5g4fD/export?format=csv'
    df = pd.read_csv(url)
    return df

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    search_term = request.json.get('searchTerm', '').lower()
    df = get_google_sheet()
    results = df[df.apply(lambda row: search_term in row.astype(str).str.lower().to_string(), axis=1)]
    return jsonify(results.to_dict(orient='records'))

if __name__ == '__main__':
    app.run(debug=True)
