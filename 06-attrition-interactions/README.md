# 06 · Attrition client avec historique d'interactions

**Question métier** : l'historique de relation (appels, connexions, réclamations, visites) améliore-t-il la détection des clients sur le départ ?

## Données
Deux fichiers CSV fictifs :
- `clients.csv` : environ 4 000 clients (profil, carte, produits, frais, revenu, solde), **12 % de départs**
- `interactions_12_mois.csv` : environ **210 000 interactions** sur 12 mois

## Démarche
1. **`1_attrition_profil_seul.ipynb`** : modèle de référence sur le profil client seul (ancienneté calculée à partir de la date d'ouverture)
2. **`2_attrition_avec_interactions.ipynb`** :
   - agrégation par client : nombre d'interactions par type (`crosstab`), note moyenne, **récence** (jours depuis la dernière interaction), **tendance** d'usage de l'appli (3 derniers mois vs moyenne)
   - jointure contrôlée : `merge(how="left", validate="one_to_one")`, repérage des 40 identifiants orphelins et des 120 clients sans interaction
   - valeurs manquantes informatives : `SimpleImputer(add_indicator=True)`
   - choix du seuil selon les coûts (hypothèses : 50 € par action de fidélisation, 400 € par départ manqué)

## Résultats
| Modèle | Rappel | Précision | AUC |
|---|---|---|---|
| Profil seul | 59 % | 18 % | 0,65 |
| Profil + interactions | 62 % | 22 % | **0,74** |

Avec les interactions, le coût total minimal baisse de 31 200 € à 26 750 € sous ces hypothèses.

## Ce que j'en retiens
Les données comportementales apportent plus que le profil statique. Pistes : courbes ROC comparées, validation croisée, forêt aléatoire, taux de réussite des actions de fidélisation dans le calcul de coût.

> Les fichiers `clients.csv` et `interactions_12_mois.csv` sont fournis dans ce dossier.
