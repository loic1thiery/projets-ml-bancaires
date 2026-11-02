# 05 · Activation de l'appli mobile après campagne

**Question métier** : quels leviers de campagne (canal, horaire, personnalisation, relances) augmentent l'activation de l'appli dans les 30 jours ?

## Données
Export CSV fictif au format français (`;` et `,` décimale) de 5 018 clients, **38 % d'activations**.

## Démarche
- Import d'un CSV au format français, nettoyage réel : âges impossibles (0, 3, 156, 999…), doublons, valeurs manquantes
- Cible Oui/Non → 1/0, extraction du **jour de la semaine** depuis la date d'envoi
- Pipeline de prétraitement + régression logistique pondérée
- **Simulation « et si ? »** : on modifie un levier pour toute la base et on recalcule les activations attendues

## Résultats
| | Valeur |
|---|---|
| Rappel | 75 % |
| Précision | 58 % |
| AUC | 0,77 |

| Scénario simulé | Gain estimé d'activations |
|---|---|
| Canal = notification | +611 |
| Envoi à 12 h | +339 |
| Message personnalisé | +328 |
| Canal = courrier | −899 |

## Limites
Le modèle mesure des corrélations, pas des causes : un **test A/B** est nécessaire avant de généraliser un canal.

> Le fichier `export_campagne_appli_mobile.csv` est fourni dans ce dossier.
