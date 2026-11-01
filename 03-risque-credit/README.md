# 03 · Risque de crédit (défaut de paiement)

**Question métier** : quelles demandes de prêt à la consommation présentent un risque de défaut élevé ?

## Données
8 000 demandes de prêt **générées dans le notebook** (âge, revenu, montant, durée, situation professionnelle, logement, incidents passés, crédits en cours, ancienneté bancaire), **8 % de défauts**.

## Démarche
- Nettoyage, pipeline de prétraitement, régression logistique pondérée
- **Importance des variables par permutation** (sur l'AUC)
- Analyse descriptive : taux de défaut par durée, par quintile de revenu et de montant, tableaux croisés et cartes de chaleur

## Résultats
| | Valeur |
|---|---|
| Rappel | 65 % (83 défauts détectés sur 128) |
| Précision | 17 % |
| AUC | 0,76 |

Variables les plus importantes : **durée, montant et revenu**, soit les ingrédients du taux d'endettement. Le taux de défaut passe de 19,5 % sur 12 mois à 3,7 % sur 84 mois dans ces données simulées.

## Ce que j'en retiens
L'importance par permutation et les tableaux croisés permettent d'expliquer le modèle à un métier. Piste : construire directement un taux d'endettement (mensualité / revenu).
