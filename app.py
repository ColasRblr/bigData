# app.py

from flask import Flask, jsonify, render_template
import json

app = Flask(__name__)

# Route pour afficher la page d'accueil
@app.route('/')
def dashboard():
    books = load_books()
    return render_template('dashboard.html', books=books)

# Chargement des données depuis le fichier JSON
def load_books():
    with open('books.json', 'r') as file:
        return json.load(file)

books_data = load_books()

# Analyse des données
def analyze_books():
    total_books = len(books_data)
    average_rating = sum(book['rating'] for book in books_data) / total_books
    return {
        'total_books': total_books,
        'average_rating': average_rating
    }

# Route pour obtenir les statistiques des livres
@app.route('/stats')
def get_stats():
    stats = analyze_books()
    return jsonify(stats)

# Manipulation des données (ajout, mise à jour, suppression)
# Ajoutez vos fonctions pour manipuler les données des livres ici

if __name__ == '__main__':
    app.run(debug=True)
