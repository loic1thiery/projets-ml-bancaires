# 07 · Comparaison de modèles pour le risque de crédit

**Question métier** : une forêt aléatoire ou un gradient boosting détecterait-il mieux les défauts de paiement que la régression logistique en place ? Et le gain justifie-t-il de perdre en explicabilité, alors qu'une banque doit pouvoir justifier un refus de crédit ?

## Données
`demandes_credit.csv` : **12 070 demandes de prêt à la consommation fictives** (2023-2025), avec profil de l'emprunteur, caractéristiques du prêt, incidents et découverts, et **10,6 % de défauts**. Elles sont générées par `generer_donnees.py`, avec des pièges volontaires : doublons, âges et revenus impossibles, durées nulles, libellés incohérents (`CDI`, `cdi`, `C.D.I.`…) et une colonne qui provoque une fuite de données.

## Démarche
1. **Nettoyage** : valeurs impossibles remplacées par `NaN` et imputées dans le pipeline. Les valeurs manquantes informatives (ancienneté des retraités) sont distinguées des erreurs de saisie.
2. **Fuite de données** : `Nb_Relances_Recouvrement` est connue seulement après l'impayé. Elle fait passer l'AUC à 0,98 et est donc exclue.
3. **Variables métier** : mensualité (formule d'annuité), taux d'endettement et dépassement du plafond de 35 %. Le taux de défaut passe de **4 % à 25 %** au-delà de ce plafond.
4. **Validation croisée stratifiée à 5 plis sur le train**, avec les mêmes plis pour tous les modèles. Le jeu de test n'est ouvert qu'une fois, à la fin.
5. **Modèles** : régression logistique, forêt aléatoire, `HistGradientBoostingClassifier` réglé par `GridSearchCV`.
6. **Seuil choisi selon les coûts sans regarder le test**, avec `cross_val_predict` (hypothèses : 4 000 € par défaut accordé, 600 € par bon client refusé).
7. **Interprétation** : importance par permutation pour les deux modèles, coefficients et odds ratios de la logistique, comparaison pli par pli.

## Résultats
| Modèle | AUC validation croisée | AUC test | Coût test |
|---|---|---|---|
| Logistique | 0,756 ± 0,013 | – | – |
| Logistique + `Depasse_35` | 0,791 ± 0,006 | 0,796 | 599 200 € |
| Logistique + `Depasse_35` + `Age_Extreme` | 0,800 ± 0,008 | non évalué¹ | – |
| Forêt aléatoire | 0,795 ± 0,007 | 0,804 | 637 600 € |
| **Boosting réglé** | **0,807 ± 0,007** | **0,819** | **596 200 €** |

¹ Variable ajoutée après l'ouverture du test, donc évaluée uniquement par validation croisée.

- **Les variables métier comptent autant que le choix du modèle.** `Depasse_35` fait gagner 3,5 points d'AUC à la logistique et presque rien à la forêt, qui trouve ce seuil toute seule.
- **Le boosting est le meilleur, mais de peu.** Il fait gagner environ 52 000 € sur 9 600 dossiers en validation croisée, soit environ 5 € par dossier. Sur le test, l'écart avec la logistique n'est plus que de 3 000 € : c'est moins que le coût d'un seul défaut.
- **À volume de refus égal**, les deux modèles se valent quand on refuse 31 % des demandes. Le boosting fait mieux quand on en refuse 21 % : il trie mieux la « zone grise ».
- **Ce qui pèse dans les décisions** : dépassement des 35 %, incidents de paiement, âge (risque en U, plus élevé avant 25 ans et après 72 ans) et épargne. La logistique ne peut pas lire seule ces effets non linéaires.

## Recommandation
**Logistique enrichie de variables métier.** Elle obtient un AUC de 0,800 contre 0,807 pour le boosting, elle est explicable dossier par dossier et plus simple à maintenir. Le gain du boosting est modeste (environ 5 € par dossier en validation croisée) et incertain : sur le test, l'écart est plus petit que le coût d'un seul défaut.

Je basculerais vers le boosting si la banque veut accepter davantage de demandes, car c'est dans la « zone grise » qu'il fait la différence. Il faudrait alors comparer ce gain au coût de mise en production et d'explication (SHAP).

## Ce que j'en retiens
Un modèle complexe ne bat un modèle simple que sur ce qu'on ne lui a pas décrit. Décrire les données à une logistique (seuils, formes en U) demande du temps et une compréhension métier, alors que le boosting les trouve seul. Choisir la logistique, c'est échanger un peu de performance contre de la transparence.

**Limites** : données fictives, coûts simplifiés, test de seulement 254 défauts.

**Pistes** : calibration des probabilités, explications individuelles (SHAP), validation sur une période ultérieure (`Date_Demande`).
