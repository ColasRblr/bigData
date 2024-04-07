// app.js

// Code JavaScript pour récupérer les statistiques des livres et afficher des graphiques
fetch('/stats')
    .then(response => response.json())
    .then(data => {
        document.getElementById('stats').innerHTML = `
            <p>Total Books: ${data.total_books}</p>
            <p>Average Rating: ${data.average_rating}</p>
        `;
    })
    .catch(error => console.error('Error:', error));

// Code JavaScript pour créer et afficher des graphiques Plotly
// Ajoutez votre code de graphique ici
