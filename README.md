# Projets de data science : banque, assurance et plus

Des cas d'usage métier traités de bout en bout en Python, du nettoyage des données jusqu'à la décision (choix du seuil selon les coûts, simulation de scénarios, recommandation argumentée). Les projets sont classés par secteur et deviennent progressivement plus complexes.

> **Données entièrement fictives.** Elles sont générées dans les notebooks, par des scripts ou proviennent d'exports simulés. Aucune donnée client réelle n'est utilisée.

## Banque

| # | Projet | Question métier | Données | AUC |
|---|---|---|---|---|
| 01 | [Churn – premier modèle](01-churn-premier-modele) | Quels clients risquent de partir ? | 1 000 clients, 9 % de départs | 0,74 |
| 02 | [Détection de fraude](02-detection-fraude) | Quelles transactions vérifier ? | 20 000 transactions, 2 % de fraudes | 0,78 |
| 03 | [Risque de crédit](03-risque-credit) | Quelles demandes de prêt sont à risque ? | 8 000 prêts, 8 % de défauts | 0,76 |
| 04 | [Insatisfaction client](04-insatisfaction-client) | Qui contacter en priorité ? | 6 000 clients, 15 % d'insatisfaits | 0,77 |
| 05 | [Activation appli mobile](05-activation-appli-mobile) | Quels leviers de campagne activer ? | 5 018 clients, 38 % d'activations | 0,77 |
| 06 | [Attrition + interactions](06-attrition-interactions) | L'historique de relation améliore-t-il la détection ? | 4 000 clients + 210 000 interactions | 0,65 → 0,74 |
| 07 | [Comparaison de modèles – crédit](07-comparaison-modeles-credit) | Un modèle plus complexe vaut-il la perte d'explicabilité ? | 12 000 demandes de prêt, 11 % de défauts | 0,76 → 0,81 |

**Prochains projets** : assurance (coût des sinistres, régression), segmentation de clientèle, séries temporelles, traitement de texte.

## Démarche (projets de classification)
1. Poser le problème : classification binaire, au service de quelle décision ?
2. Auditer et nettoyer : doublons, valeurs manquantes, valeurs impossibles, formats français
3. Découper en train/test stratifié
4. Prétraiter dans un `ColumnTransformer` (imputation, standardisation, one-hot) au sein d'un `Pipeline`
5. Modéliser : régression logistique avec pondération des classes déséquilibrées
6. Évaluer : matrice de confusion, rappel, précision, AUC, plutôt que la seule exactitude
7. Interpréter : odds ratios, importance par permutation, tableaux croisés
8. Décider : seuil choisi selon les coûts métier, simulations « et si ? »

À partir du projet 07 : validation croisée, forêt aléatoire et gradient boosting, réglages par `GridSearchCV`, seuil choisi sans regarder le jeu de test.

## Outils
Python · pandas · NumPy · scikit-learn · matplotlib · JupyterLab

## Lancer les notebooks
```bash
pip install -r requirements.txt
jupyter lab
```
Chaque dossier contient les fichiers CSV utilisés. Les projets 01 à 04 peuvent aussi régénérer leurs données (première cellule du notebook), le projet 07 avec `generer_donnees.py`.

## Auteur
**Loïc Thiery** – Data Analyst (Power BI, Microsoft Fabric, Python) · [GitHub](https://github.com/loic1thiery)
