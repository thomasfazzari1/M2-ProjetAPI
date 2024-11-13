function filtrerEvenements() {
    const filtreSport = document.getElementById('sport_filtre').value;
    const lignes = document.querySelectorAll('.event-row');

    lignes.forEach(ligne => {
        const sportId = ligne.getAttribute('data-sport-id');
        if (filtreSport === 'all' || filtreSport === sportId) {
            ligne.style.display = '';
        } else {
            ligne.style.display = 'none';
        }
    });
}