import os
import logging
from flask import Flask, flash, redirect, render_template, request
from utils import generer_nuage_mots, generer_graphique_tendance
from nltk.sentiment import SentimentIntensityAnalyzer
import json
from werkzeug.utils import secure_filename

books = []

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = 'votre_clé_secrète_ici'

sia = SentimentIntensityAnalyzer()

def analyser_sentiment(occurrence_file):
    with open(occurrence_file, 'r') as file:
        text = file.read()
    score = sia.polarity_scores(text)
    return score

@app.route('/')
def accueil():
    books_directory = 'books'

    book_directories = sorted(os.listdir(books_directory))
    
    temp_books = []

    for book_directory in book_directories:
        if os.path.isdir(os.path.join(books_directory, book_directory)):
            logger.debug("Livre trouvé : %s", book_directory)
            
            mots_occurrence_file = os.path.join(books_directory, book_directory, 'mots_occurrence.txt')
            logger.debug("Chemin du fichier mots_occurrence : %s", mots_occurrence_file)

            if os.path.isfile(mots_occurrence_file):
                logger.debug("Fichier mots_occurrence existant pour le livre %s", book_directory)
            
                book_title = book_directory
                logger.debug("Titre du livre : %s", book_title)

                sentiment_score = analyser_sentiment(mots_occurrence_file)
                logger.debug("Score de sentiment analysé pour le livre %s : %s", book_directory, sentiment_score)

                nuage_mots_file = generer_nuage_mots(book_directory, mots_occurrence_file)
                logger.debug("Nuage de mots généré : %s", nuage_mots_file)

                mots_poids_file = os.path.join(books_directory, book_directory, 'mots_poids.json')
                with open(mots_poids_file, 'w') as file:
                    json.dump(sentiment_score, file)
                logger.debug("Fichier de poids de mots généré : %s", mots_poids_file)

                diagramme_tendance_file = generer_graphique_tendance(book_directory, mots_poids_file)
                logger.debug("Graphique de tendance généré : %s", diagramme_tendance_file)

                book_info = {
                    'title': book_title,
                    'nuage_mots_file': nuage_mots_file,
                    'diagramme_tendance_file': None
                }

                temp_books.append(book_info)
    
    for temp_book in temp_books:
        if temp_book not in books:
            books.append(temp_book)

    return render_template('accueil.html', books=books)


@app.route('/details/<book>')
def details(book):
    mots_occurrence_file = 'books/{}/mots_occurrence.txt'.format(book)
    mots_poids_file = 'books/{}/mots_poids.txt'.format(book)

    nuage_mots_file = generer_nuage_mots(book, mots_occurrence_file)

    diagramme_tendance_file = generer_graphique_tendance(book, mots_poids_file)

    return render_template('details.html', book=book, nuage_mots_file=nuage_mots_file, diagramme_tendance_file=diagramme_tendance_file)

ALLOWED_EXTENSIONS = {'txt'}
app.config['UPLOAD_FOLDER'] = 'upload_folder'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        try:
            mots_poids_file = os.path.join(app.config['UPLOAD_FOLDER'], 'mots_poids_' + filename)
            sentiment_score = analyser_sentiment(file_path)
            with open(mots_poids_file, 'w') as f:
                json.dump(sentiment_score, f)
                
            book_title = filename.split('.')[0]  
            nuage_mots_file = generer_nuage_mots(book_title, file_path)
            diagramme_tendance_file = generer_graphique_tendance(book_title, mots_poids_file)
                
            existing_book = next((book for book in books if book['title'] == book_title), None)
            if existing_book:
                existing_book['nuage_mots_file'] = nuage_mots_file
                existing_book['diagramme_tendance_file'] = diagramme_tendance_file
            else:
                books.append({
                    'title': book_title,
                    'nuage_mots_file': nuage_mots_file,
                    'diagramme_tendance_file': diagramme_tendance_file
                })
                
            flash('File uploaded and processed successfully')
            return redirect('/')
        except Exception as e:
            flash('Error processing file: {}'.format(str(e)))
            return redirect(request.url)
    else:
        flash('Invalid file extension')
        return redirect(request.url)

if __name__ == "__main__":
    app.run(debug=True)
