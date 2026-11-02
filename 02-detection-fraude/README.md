# 02 · Détection de fraude

**Question métier** : quelles transactions bloquer ou faire vérifier avant validation ?

## Données
20 000 transactions **générées dans le notebook** (montant, heure, type, étranger, distance, nombre de transactions sur 24 h, ancienneté du compte, nouveau bénéficiaire, âge), **2 % de fraudes**.

## Démarche
- Nettoyage (doublons, valeurs manquantes)
- Création d'une variable `nuit` (transactions entre 0 h et 5 h)
- Pipeline de prétraitement + régression logistique avec `class_weight="balanced"`

## Résultats (jeu de test, 4 000 transactions)
| | Valeur |
|---|---|
| Fraudes détectées | 51 sur 79 (rappel 65 %) |
| Alertes émises | 1 078 (précision 5 %) |
| AUC | 0,78 |

## Ce que j'en retiens
Quand l'événement est très rare, détecter deux tiers des fraudes coûte cher en fausses alertes : environ un client honnête sur quatre serait bloqué. Le seuil doit se choisir avec le coût d'une fraude manquée et le coût d'une vérification. Pistes : modèles non linéaires (forêt aléatoire, gradient boosting) et variables comportementales plus fines.

> Le fichier `transactions_fraude.csv` est fourni dans ce dossier ; la première cellule du notebook permet aussi de le régénérer.
