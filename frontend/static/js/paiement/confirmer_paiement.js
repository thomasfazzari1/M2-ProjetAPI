document.addEventListener("DOMContentLoaded", function () {
    const numeroCarteInput = document.getElementById("numero_carte");
    const expirationInput = document.getElementById("expiration");

    if (numeroCarteInput) {
        numeroCarteInput.addEventListener("input", function (e) {
            let value = e.target.value.replace(/\s+/g, "");
            value = value.replace(/\D/g, "");
            value = value.match(/.{1,4}/g)?.join(" ") || value;
            e.target.value = value.slice(0, 19);
        });
    }

    if (expirationInput) {
        expirationInput.addEventListener("input", function (e) {
            let value = e.target.value.replace(/\D/g, "");
            if (value.length > 2) {
                value = value.slice(0, 2) + "/" + value.slice(2, 4);
            }
            e.target.value = value.slice(0, 5);

            const [mois, annee] = value.split("/").map(Number);
            const now = new Date();
            const moisCourant = now.getMonth() + 1;
            const anneeCourante = now.getFullYear() % 100;

            if (
                (annee < anneeCourante) ||
                (annee === anneeCourante && mois < moisCourant)
            ) {
                e.target.setCustomValidity("La date d'expiration est déjà passée.");
            } else {
                e.target.setCustomValidity("");
            }
        });
    }
});
