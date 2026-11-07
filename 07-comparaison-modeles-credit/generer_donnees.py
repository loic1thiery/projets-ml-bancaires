"""Génère le fichier fictif demandes_credit.csv du projet 07.

Le script contient la mécanique (fictive) du défaut et la liste des pièges
glissés volontairement dans les données : doublons, valeurs impossibles,
libellés incohérents et une colonne qui provoque une fuite de données.

Lancement : python generer_donnees.py
"""

import numpy as np
import pandas as pd

rng = np.random.default_rng(2026)
n = 12_000

# --- Profil de l'emprunteur -------------------------------------------------
situation = rng.choice(
    ["CDI", "Fonctionnaire", "CDD", "Indépendant", "Retraité", "Sans emploi"],
    size=n, p=[0.46, 0.14, 0.13, 0.10, 0.13, 0.04],
)
age = np.where(
    situation == "Retraité",
    rng.integers(60, 86, n),
    np.clip(rng.normal(41, 11, n).round(), 19, 66),
).astype(int)

base_revenu = {"CDI": 2700, "Fonctionnaire": 2500, "CDD": 1800, "Indépendant": 3000,
               "Retraité": 2000, "Sans emploi": 1000}
revenu = np.array([base_revenu[s] for s in situation]) * rng.lognormal(0, 0.35, n)
revenu = (revenu * (1 + (age - 40).clip(-15, 20) * 0.008)).round(-1)

anciennete_emploi = np.where(
    np.isin(situation, ["Retraité", "Sans emploi"]),
    np.nan,
    np.clip(rng.exponential(6, n), 0, age - 18).round(1),
)

logement = rng.choice(["Propriétaire", "Locataire", "Hébergé"], size=n, p=[0.48, 0.42, 0.10])
logement = np.where((age < 25) & (rng.random(n) < 0.5), "Hébergé", logement)
nb_enfants = rng.choice([0, 1, 2, 3, 4], size=n, p=[0.40, 0.22, 0.25, 0.10, 0.03])

# --- Caractéristiques du prêt -----------------------------------------------
objet = rng.choice(["Auto", "Travaux", "Consommation", "Rachat de crédits", "Études"],
                   size=n, p=[0.32, 0.24, 0.26, 0.12, 0.06])
objet = np.where((age < 27) & (rng.random(n) < 0.35), "Études", objet)
montant = np.clip(rng.lognormal(np.log(12_000), 0.6, n), 1_000, 75_000).round(-2)
montant = np.where(objet == "Rachat de crédits", montant * 1.6, montant).round(-2)
duree = rng.choice([12, 24, 36, 48, 60, 72, 84], size=n, p=[0.06, 0.14, 0.22, 0.20, 0.20, 0.10, 0.08])
taux = (3.2 + duree / 40 + rng.normal(0, 0.5, n)).clip(1.5, 9).round(2)

nb_credits = rng.choice([0, 1, 2, 3, 4], size=n, p=[0.42, 0.30, 0.17, 0.08, 0.03])
nb_credits = np.where(objet == "Rachat de crédits", nb_credits + 2, nb_credits)
charges_credits = (nb_credits * rng.uniform(90, 320, n)).round(0)

incidents = rng.poisson(0.25, n)
decouvert_jours = np.clip(rng.exponential(12, n) * (1 + incidents), 0, 365).round().astype(int)
epargne = (rng.lognormal(np.log(4_000), 1.2, n) * (revenu / 2500)).round(-1)

# Mensualité réelle (formule d'annuité) et taux d'endettement après le prêt.
# Ces deux variables ne sont pas fournies : elles sont à construire dans l'analyse.
t = taux / 100 / 12
mensualite = montant * t / (1 - (1 + t) ** -duree)
endettement = (mensualite + charges_credits) / revenu

# --- Mécanique du défaut (non linéaire, avec interactions) -------------------
fragile = (epargne < 1500) & (endettement > 0.35)  # peu d'épargne ET fort endettement
logit = (
    -3.9
    + 1.5 * (endettement > 0.35)                       # effet de seuil au-delà de 35 %
    + 1.6 * fragile
    + 0.6 * np.minimum(incidents, 2)
    + 1.2 * ((decouvert_jours > 45) & (logement != "Propriétaire"))
    + 1.5 * ((situation == "CDD") & (age < 30))         # interaction jeune + CDD
    + 0.7 * (situation == "Sans emploi")
    + 0.6 * ((situation == "Indépendant") & (np.nan_to_num(anciennete_emploi) < 3))
    - 0.4 * (situation == "Fonctionnaire")
    + 1.2 * ((age < 25) | (age > 72))                  # risque plus élevé aux deux extrêmes
    + 0.25 * (logement == "Locataire")
    + 0.3 * (objet == "Rachat de crédits")
    + rng.normal(0, 0.5, n)                            # part imprévisible du défaut
)
defaut = rng.random(n) < 1 / (1 + np.exp(-logit))

# Relances de recouvrement : connues APRÈS le défaut → fuite de données.
relances = np.where(defaut, rng.poisson(3.2, n), rng.poisson(0.15, n))

dates = pd.Timestamp("2023-01-01") + pd.to_timedelta(rng.integers(0, 3 * 365, n), unit="D")

df = pd.DataFrame({
    "ID_Demande": [f"D{100000 + i}" for i in range(n)],
    "Date_Demande": dates.strftime("%d/%m/%Y"),
    "Age": age,
    "Situation_Pro": situation,
    "Anciennete_Emploi_Ans": anciennete_emploi,
    "Statut_Logement": logement,
    "Nb_Enfants": nb_enfants,
    "Revenu_Mensuel_EUR": revenu,
    "Epargne_EUR": epargne,
    "Objet_Pret": objet,
    "Montant_EUR": montant,
    "Duree_Mois": duree,
    "Taux_Annuel_Pct": taux,
    "Nb_Credits_En_Cours": nb_credits,
    "Charges_Credits_Mensuelles_EUR": charges_credits,
    "Nb_Incidents_24M": incidents,
    "Jours_Decouvert_12M": decouvert_jours,
    "Nb_Relances_Recouvrement": relances,
    "Defaut": np.where(defaut, "Oui", "Non"),
})

# --- Pièges de saisie ---------------------------------------------------------
# 1. Valeurs manquantes non informatives
for col, part in [("Epargne_EUR", 0.06), ("Revenu_Mensuel_EUR", 0.015), ("Statut_Logement", 0.02)]:
    df.loc[rng.random(n) < part, col] = np.nan

# 2. Valeurs impossibles
idx = rng.choice(n, 25, replace=False)
df.loc[idx[:12], "Age"] = rng.choice([0, 150, 999], 12)
df.loc[idx[12:], "Revenu_Mensuel_EUR"] = -df.loc[idx[12:], "Revenu_Mensuel_EUR"].abs()
df.loc[rng.choice(n, 8, replace=False), "Duree_Mois"] = 0

# 3. Libellés incohérents
idx = rng.choice(np.flatnonzero(df["Situation_Pro"] == "CDI"), 150, replace=False)
df.loc[idx, "Situation_Pro"] = rng.choice(["cdi", "CDI ", "C.D.I."], 150)
idx = rng.choice(np.flatnonzero(df["Statut_Logement"] == "Locataire"), 80, replace=False)
df.loc[idx, "Statut_Logement"] = "locataire"

# 4. Doublons exacts
df = pd.concat([df, df.sample(70, random_state=1)]).sample(frac=1, random_state=2).reset_index(drop=True)

df.to_csv("demandes_credit.csv", sep=";", decimal=",", index=False, encoding="utf-8")
print(df.shape, "| taux de défaut :", round((df["Defaut"] == "Oui").mean(), 3))
