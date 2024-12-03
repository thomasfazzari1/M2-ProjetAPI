-- DB Authentification
\c Authentification;

CREATE TABLE IF NOT EXISTS public.utilisateur (
    id SERIAL PRIMARY KEY,
    pseudo VARCHAR(255) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL UNIQUE,
    mdp_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    bookmaker BOOLEAN NOT NULL DEFAULT FALSE
);

-- DB Match
\c Match;

CREATE TABLE IF NOT EXISTS public.sport (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(255) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS public.evenement (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(255) NOT NULL,
    id_sport_associe INT NOT NULL REFERENCES public.sport (id)
);

CREATE TABLE IF NOT EXISTS public.equipe (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(255) NOT NULL,
    id_sport_associe INT NOT NULL REFERENCES public.sport (id)
);

CREATE TABLE IF NOT EXISTS public.rencontre (
    id SERIAL PRIMARY KEY,
    id_sport_associe INT NOT NULL REFERENCES public.sport (id),
    id_evenement_associe INT NOT NULL REFERENCES public.evenement (id),
    date DATE NOT NULL,
    heure_debut TIME NOT NULL,
    heure_fin TIME NOT NULL,
    id_eq_domicile INT NOT NULL REFERENCES public.equipe (id),
    valeur_cote_domicile DECIMAL(5, 2) NOT NULL,
    id_eq_exterieure INT NOT NULL REFERENCES public.equipe (id),
    valeur_cote_exterieure DECIMAL(5, 2) NOT NULL,
    valeur_cote_match_nul DECIMAL(5, 2) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    created_by INT,
    updated_by INT,
    est_mis_en_avant BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS public.bookmaker (
    id SERIAL PRIMARY KEY,
    id_utilisateur INT NOT NULL UNIQUE
);

-- DB Pari
\c Pari;

CREATE TABLE IF NOT EXISTS public.parieur (
    id SERIAL PRIMARY KEY,
    id_utilisateur INT NOT NULL UNIQUE,
    cagnotte NUMERIC(10, 2) NOT NULL DEFAULT 0.00
);

-- DB Paiement
\c Paiement;

CREATE TABLE IF NOT EXISTS public.payeur (
    id SERIAL PRIMARY KEY,
    id_utilisateur INT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS public.paiement (
    id SERIAL PRIMARY KEY,
    id_payeur INT NOT NULL REFERENCES public.payeur (id),
    montant NUMERIC(10, 2) NOT NULL,
    date TIMESTAMP NOT NULL DEFAULT NOW(),
    statut VARCHAR(50) NOT NULL DEFAULT 'en attente'
);
