document.addEventListener("DOMContentLoaded", function () {
    const coteFields = document.querySelectorAll("#valeur_cote_eq_domicile, #valeur_cote_eq_exterieure, #valeur_cote_match_nul");

    // Valeurs négatives pour les cotes
    coteFields.forEach(field => {
        field.addEventListener("input", function () {
            if (parseFloat(this.value) < 0) {
                this.value = Math.abs(this.value);
            }
        });
    });

    // Filtres
    document.getElementById("sport_filtre").addEventListener("change", function () {
        const selectedSport = this.value;
        const matchRows = document.querySelectorAll("tbody tr");

        matchRows.forEach(row => {
            const sportId = row.getAttribute("data-sport-id");
            console.log("Row sport ID:", sportId);

            if (selectedSport === "all" || selectedSport == sportId) {
                row.style.display = "";
                console.log("Displaying row with sport ID:", sportId);
            } else {
                row.style.display = "none";
                console.log("Hiding row with sport ID:", sportId);
            }
        });
    });
});
