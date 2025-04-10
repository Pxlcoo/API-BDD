# Projet Gestion des Produits

Ce projet se compose d'une API REST développée avec **FastAPI** qui permet de gérer une base de données de produits, et d'une application cliente en ligne de commande (CLI) qui interagit avec cette API grâce à la bibliothèque **requests**.

L'API permet de créer, lire, mettre à jour et supprimer des produits dans une base de données MySQL en utilisant **SQLAlchemy** comme ORM. Le côté client propose un menu interactif pour tester facilement les fonctionnalités de l'API.

---

## Technologies utilisées

- **Python 3.7+**
- **FastAPI** pour la gestion de l’API REST
- **SQLAlchemy** pour l'interaction avec la base de données
- **MySQL** (avec `mysql-connector-python`) comme SGBD
- **Pydantic** pour la validation des données et la création de schémas
- **Requests** pour effectuer des appels HTTP depuis le client CLI
- **Logging** pour la journalisation des actions et erreurs

---

## Structure du projet

Le projet se compose de deux parties principales :

1. **API FastAPI :**
   - **Configuration et connexion à la base de données :**  
     Le code configure une connexion vers une base MySQL. L’URL de connexion se définit via la variable d’environnement `DATABASE_URL` (par défaut : `mysql+mysqlconnector://root:@localhost:3306/pizzeriadb`).
   - **Modèle SQLAlchemy (`Produit`) :**  
     Il définit la table `produit` avec des colonnes telles que `id`, `nom`, `description`, `prix`, `categorie` et `disponibilite`.
   - **Schémas Pydantic :**  
     `ProduitCreate` sert à la validation des données d’entrée (avec notamment une vérification pour s’assurer que le prix est positif) et `ProduitOut` ajoute l'ID pour les réponses.
   - **Endpoints REST :**  
     - `GET /api/produit` : Récupérer la liste de tous les produits  
     - `POST /api/produit` : Ajouter un nouveau produit  
     - `DELETE /api/produit/{produit_id}` : Supprimer un produit par son ID  
     - `PUT /api/produit/{produit_id}` : Mettre à jour un produit existant par son ID  
     
2. **Client CLI :**
   - Un script Python qui utilise la bibliothèque `requests` pour appeler les endpoints de l'API.
   - Il propose un menu interactif permettant de :
     - Voir la liste des produits
     - Ajouter un produit (en renseignant nom, description, catégorie, prix et disponibilité)
     - Supprimer un produit via son ID
     - Mettre à jour les informations d’un produit via son ID

---

## Installation et Configuration

1. **Prérequis :**

   - Installer Python (version 3.7 ou supérieure).
   - Avoir un serveur MySQL opérationnel.

2. **Installation des dépendances :**

   Exécutez la commande suivante pour installer toutes les bibliothèques nécessaires :

   ```bash
   pip install fastapi uvicorn sqlalchemy mysql-connector-python pydantic requests
