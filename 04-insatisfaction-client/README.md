# 04 · Insatisfaction client (digital et communication)

**Question métier** : quels clients contacter en priorité pour prévenir l'insatisfaction ?

## Données
6 000 clients **générés dans le notebook** : segment, canal préféré, conseiller dédié, connexions à l'appli, bugs signalés, temps de réponse du chat, e-mails et notifications reçus, taux d'ouverture, réclamations. **15 % d'insatisfaits**.

## Démarche
- Nettoyage, pipeline de prétraitement, régression logistique pondérée
- **Choix du seuil de décision par le coût** : tableau rappel / précision / coût total pour des seuils de 0,30 à 0,85

## Résultats
| | Valeur |
|---|---|
| Rappel | 70 % (124 insatisfaits détectés sur 176) |
| Précision | 28 % |
| AUC | 0,77 |
| Seuil retenu | 0,45 (hypothèses : 15 € par contact, 120 € par insatisfait manqué) |

## Ce que j'en retiens
Le seuil de 0,5 par défaut n'a rien d'optimal : il se choisit à partir des coûts métier, qui doivent être explicités. Piste : choisir le seuil par validation croisée sur l'entraînement plutôt que sur le test.
