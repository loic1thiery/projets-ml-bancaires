# 01 · Churn – premier modèle

**Question métier** : quels clients risquent de quitter la banque, pour cibler une action de fidélisation ?

## Données
1 000 clients **générés dans le notebook** (âge, revenu, ancienneté, nombre de produits, usage digital, région, contacts, solde), environ 9 % de départs. Valeurs manquantes et doublons ajoutés volontairement pour l'exercice de nettoyage.

## Démarche
- Audit et nettoyage : `describe`, `isna`, `duplicated`, `drop_duplicates`
- Découpage train/test stratifié (80/20)
- `Pipeline` + `ColumnTransformer` : imputation, standardisation, one-hot
- Régression logistique, d'abord sans puis avec `class_weight="balanced"`

## Résultats
| Modèle | Départs prédits | Rappel | Précision | AUC |
|---|---|---|---|---|
| Sans pondération | 0 / 18 | 0 % | – | – |
| `class_weight="balanced"` | 68 | 72 % | 19 % | 0,74 |

## Ce que j'en retiens
Le premier modèle affiche 91 % d'exactitude… en ne prédisant **aucun** départ. Sur des classes déséquilibrées, l'exactitude est trompeuse : il faut regarder le rappel, la précision et l'AUC.

> Le fichier `donnees_churn.csv` est fourni dans ce dossier ; la première cellule du notebook permet aussi de le régénérer.
