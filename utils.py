import os
import numpy as np
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import json

def generer_chemin_fichier(book, filename):
    directory = 'static/{}'.format(book)
    if not os.path.exists(directory):
        os.makedirs(directory)
    return os.path.join(directory, filename)

def generer_nuage_mots(book_directory, mots_occurrence_file):
    nuage_mots_file = generer_chemin_fichier(book_directory, 'nuage_mots.png')

    if not os.path.exists(nuage_mots_file):
        with open(mots_occurrence_file, 'r') as file:
            mots_occurrence = file.read().split('\n')

        frequences = {}
        for mot in mots_occurrence:
            if ':' in mot:
                mot_split = mot.split(':')
                frequences[mot_split[0]] = int(mot_split[1].strip())

        wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(frequences)

        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.tight_layout(pad=0)
        plt.savefig(nuage_mots_file)
        plt.close()

    return nuage_mots_file

def generer_graphique_tendance(book, mots_poids_file):
    diagramme_tendance_file = generer_chemin_fichier(book, 'diagramme_tendance.png')

    if not os.path.exists(diagramme_tendance_file):
        with open(mots_poids_file, 'r') as file:
            poids_scores = json.load(file)

        neg = poids_scores['neg']
        neu = poids_scores['neu']
        pos = poids_scores['pos']

        colors = ['red', 'gray', 'green']

        categories = ['Négatif', 'Neutre', 'Positif']
        counts = [neg, neu, pos]

        plt.figure(figsize=(8, 6))
        plt.bar(categories, counts, color=colors)
        plt.title('Tendance des Mots')
        plt.xlabel('Sentiment')
        plt.ylabel('Proportion')
        plt.savefig(diagramme_tendance_file)
        plt.close()


    return diagramme_tendance_file