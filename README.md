# Dashboard BI – Analyse des ventes commerciales

## 📊 Présentation

Projet d'analyse de données visant à explorer les performances commerciales d'un ensemble de données de ventes et à transformer les données en indicateurs, visualisations et insights exploitables.

Le projet combine une démarche d'analyse exploratoire avec un dashboard interactif permettant d'examiner les performances selon plusieurs dimensions commerciales.

## 🎯 Objectifs

- Comprendre la structure et la qualité des données.
- Identifier les principales tendances commerciales.
- Analyser le chiffre d'affaires selon les produits, pays, années et tailles de vente.
- Étudier les relations entre certaines variables numériques.
- Identifier les observations potentiellement atypiques.
- Mettre les résultats à disposition à travers un dashboard interactif.
- Dégager des observations pouvant contribuer à la prise de décision.

## 🗂️ Données

Le jeu de données contient **2 823 observations et 25 variables** relatives aux ventes commerciales.

Les principales informations concernent notamment :

- les commandes ;
- les clients ;
- les produits ;
- les pays ;
- les dates de commande ;
- les quantités commandées ;
- les prix ;
- le chiffre d'affaires ;
- la taille des ventes ;
- le statut des commandes.

## 🔎 Démarche d'analyse

Le projet suit plusieurs étapes :

1. Découverte et compréhension du jeu de données
2. Vérification de la structure et de la qualité des données
3. Analyse des valeurs manquantes
4. Exploration statistique et descriptive
5. Analyse des performances commerciales
6. Analyse temporelle
7. Étude des relations entre variables
8. Détection des valeurs potentiellement atypiques
9. Synthèse des principaux insights
10. Formulation de recommandations

## 📈 Principaux résultats

Quelques résultats issus de l'analyse :

- **Chiffre d'affaires total : 10 032 628,85**
- **307 commandes uniques**
- **92 clients uniques**
- **Classic Cars représente 39,07 % du chiffre d'affaires**
- **Classic Cars et Vintage Cars représentent ensemble 58,04 % du chiffre d'affaires**
- Les **États-Unis** constituent le principal marché avec **3 627 982,83** de chiffre d'affaires.
- Les ventes de taille **Medium représentent 60,68 % du chiffre d'affaires**.
- Le chiffre d'affaires a progressé de **34,32 % entre 2003 et 2004**.
- L'analyse temporelle montre une concentration importante de l'activité sur **octobre et novembre**.
- La variable `PRICEEACH` présente une corrélation de **0,6578 avec `SALES`**.
- **81 observations potentiellement atypiques** ont été identifiées selon la méthode de l'IQR et conservées après analyse.

## 💡 Insights et recommandations

L'analyse met notamment en évidence :

- l'importance des gammes **Classic Cars** et **Vintage Cars** dans le chiffre d'affaires ;
- le poids du marché américain ;
- l'intérêt de surveiller les périodes de forte activité, notamment octobre et novembre ;
- la nécessité d'approfondir l'analyse des ventes de grande taille ;
- l'intérêt d'étudier plus précisément les performances des principaux marchés.

Ces observations peuvent servir de base à une analyse commerciale plus approfondie et à l'identification de nouvelles opportunités.

## 🛠️ Technologies utilisées

- **Python**
- **Pandas**
- **SQL**
- **Matplotlib**
- **Seaborn**
- **Streamlit**
- **Jupyter Notebook**

## 📁 Structure du projet

```text
Dashboard-BI-Analyse-Ventes/
│
├── app.py
├── projet_nettotage_explorations.ipynb
├── sales_data.csv
├── .gitignore
└── README.md

### `app.py`

Application Streamlit permettant d'explorer les performances commerciales de manière interactive à travers des filtres, des KPI, des visualisations et différentes analyses.

### `projet_nettotage_explorations.ipynb`

Notebook présentant la démarche d'exploration, de préparation et d'analyse des données.

### `sales_data.csv`

Jeu de données utilisé pour construire les analyses et le dashboard.

## 🚀 Lancer le dashboard

Installer les dépendances nécessaires :

```bash
pip install pandas matplotlib seaborn streamlit
```

Puis lancer l'application :

```bash
streamlit run app.py
```

Le dashboard s'ouvre ensuite automatiquement dans le navigateur.

## 👤 Auteur

**Modeste Adjéran DJANGBO**

Étudiant en Licence d'Anglais – Option Britannique

Intérêt pour la Data Analysis, la Business Intelligence et la valorisation des données.