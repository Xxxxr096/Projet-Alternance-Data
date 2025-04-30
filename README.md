# Rapport détaillé : Analyse de variation des prix par conditionnement

## 1. Objectif du projet

Ce projet a pour but d'analyser les variations de prix dans les produits achetés par des restaurateurs, en utilisant des données issues de leurs factures. L'objectif final est d'aider les restaurateurs à identifier les produits dont les prix varient de manière significative, soit en raison d'un changement de conditionnement, soit en raison de différences entre fournisseurs, afin d'optimiser leurs dépenses.

Les questions clés que nous cherchons à répondre sont :

- Est-ce que le changement de conditionnement explique les variations de prix ?
- Y a-t-il des différences de prix significatives pour un même produit et un même conditionnement ?
- Peut-on regrouper automatiquement les produits selon leur profil (poids/prix) grâce à un algorithme de clustering ?

---

## 2. Découverte et nettoyage des données

### 2.1 Structure du jeu de données

Nous disposons du fichier `extrait_produits.csv`, contenant les colonnes suivantes :

- `designation` : nom brut du produit
- `interpretation_product` : nom standardisé du produit (nettoyé)
- `conditioning` : format du produit (ex: 1kg, 500g)
- `price` : prix unitaire HT

### 2.2 Valeurs manquantes

Les colonnes `interpretation_product`, `conditioning` et `price` sont essentielles pour nos analyses. Les lignes contenant des valeurs manquantes dans l'une de ces colonnes sont supprimées.

### 2.3 Détection des valeurs aberrantes

En analysant les quantiles :

- 90 % des produits ont un prix ≤ 20.88 €
- 95 % ≤ 39.36 €
- 99 % ≤ 154.80 €

Nous avons détecté :

- Des prix **négatifs** : erreurs de saisie
- Des prix **très élevés** (> 1000 €) : unités incorrectes ou prix cumulés

Nous fixons donc un seuil de nettoyage à **150 €**, ce qui permet de conserver 99 % des données pertinentes.

---

## 3. Analyse des variations de prix

### 3.1 Produits avec plusieurs conditionnements

Nous regroupons les données par `interpretation_product` et comptons le nombre de formats distincts (`conditioning`) associés. Les produits avec plus d'un format sont sélectionnés pour analyse.

### 3.2 Variation de prix par conditionnement

Pour chaque (produit, format), nous calculons :

- Le **prix moyen**
- L'**écart-type** (std)
- Le **nombre d'observations**

### 3.3 Variation de prix à conditionnement équivalent

Nous analysons les cas où un même produit a été acheté plusieurs fois dans le même format. Pour chaque groupe, nous calculons :

- Min / Max / Moyenne / écart-type du prix
- Une **variation en pourcentage** : \(\frac{max - min}{min} \times 100\)

Les produits avec une variation > 20 % sont signalés comme potentiellement liés à des fournisseurs différents ou des pratiques tarifaires variables.

---

## 4. Clustering des produits (approche bonus)

### 4.1 Objectif

Regrouper automatiquement les produits selon leurs caractéristiques de **prix** et **conditionnement** afin d'identifier des profils typiques de produits.

### 4.2 Préparation des données

- Le conditionnement est converti en **grammes** ("1kg" → 1000, "500g" → 500).
- Seules les lignes avec des poids exploitables sont conservées.

### 4.3 Normalisation

Les variables `price` et `weight_in_g` sont normalisées avec `StandardScaler` pour que chaque dimension ait une échelle comparable.

### 4.4 Application de KMeans

Nous utilisons **KMeans** avec `n_clusters=3` (choisi empiriquement). Chaque produit est assigné à un cluster.

### 4.5 Évaluation du clustering

- **Silhouette Score** obtenu : **0.5477**
  - Interprétation : le clustering est **plutôt bon**, avec des groupes bien séparés
- **Centres de clusters** analysés pour identifier les profils

## 5. Conclusion

Pour conclure ce projet, on peut dire que les étapes d'exploration, de nettoyage et d'analyse ont permis de mieux comprendre la structure des prix dans le fichier. On a vu que certaines variations de prix sont dues au format du produit (poids), ce qui est logique. Mais dans d'autres cas, à conditionnement identique, le prix varie beaucoup : cela peut venir des fournisseurs ou d'autres paramètres qu'on ne voit pas ici.

Le clustering a été un bon moyen de compléter cette étude. Il nous a permis de regrouper les produits selon leur profil prix/poids, et les résultats sont plutôt satisfaisants, avec un score silhouette de 0.5477. Cela montre que les produits sont bien répartis dans les groupes formés.

Ce type d’analyse pourrait être utile dans un contexte réel pour surveiller les prix, négocier avec des fournisseurs, ou encore faire des recommandations d’achat plus cohérentes. Le script développé est réutilisable sur d'autres fichiers similaires.

---

## 6. Livrables produits

- `projet.ipynb` : notebook Jupyter avec l'analyse pas à pas
- `analyse_prix.py` : script réutilisable pour traitement automatique
- `resultats_clusters.csv` : produits segmentés par cluster
- `clusters.png` : visualisation des groupes formés
- `README.md` : interprétation et justification détaillée

## 7. Sources utiles

Voici quelques sources qui ont été consultées :

- Scikit-learn (clustering, preprocessing, évaluation) : https://scikit-learn.org/stable/
- Analyse exploratoire en Python : https://realpython.com/pandas-python-explore-dataset/
- KMeans et silhouette score expliqués : https://towardsdatascience.com/k-means-clustering-explained-4528df86a120
- Visualisation de données avec seaborn : https://seaborn.pydata.org/tutorial.html
