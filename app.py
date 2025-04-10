import requests

API_URL = "http://127.0.0.1:8000"  # Base URL for the API

def afficher_menu():
    print("\n==== MENU PRODUITS ====")
    print("1. Voir tous les produits")
    print("2. Ajouter un produit")
    print("3. Supprimer un produit")
    print("4. Mettre à jour un produit")
    print("5. Quitter")

def voir_produits():
    try:
        r = requests.get(f"{API_URL}/api/produit")
        r.raise_for_status()
        produits = r.json()
        if isinstance(produits, list):
            print("\n--- Liste des produits ---")
            for p in produits:
                print(f"{p['id']}: {p['nom']} - {p['prix']} € (Description: {p.get('description', '')}, Catégorie: {p.get('categorie', '')})")
        else:
            print("La réponse n'est pas une liste de produits.")
    except requests.exceptions.RequestException as e:
        print(f"❌ Erreur de connexion à l'API : {e}")

def ajouter_produit():
    try:
        nom = input("Nom du produit : ")
        description = input("Description : ")
        categorie = input("Catégorie : ")
        prix = float(input("Prix : "))
        disponibilite = input("Disponibilité (Disponible/Indisponible) : ") or "Disponible"

        if prix <= 0:
            print("❌ Le prix doit être un nombre positif.")
            return

        r = requests.post(f"{API_URL}/api/produit", json={
            "nom": nom, "description": description, "categorie": categorie, "prix": prix, "disponibilite": disponibilite
        })
        r.raise_for_status()
        print("✅ Produit ajouté :", r.json())
    except requests.exceptions.RequestException as e:
        print(f"❌ Erreur lors de l'ajout du produit : {e}")

def supprimer_produit():
    try:
        produit_id = int(input("ID du produit à supprimer : "))
        r = requests.delete(f"{API_URL}/api/produit/{produit_id}")
        r.raise_for_status()
        print("🗑️ Produit supprimé")
    except requests.exceptions.RequestException as e:
        print(f"❌ Erreur lors de la suppression du produit : {e}")

def mettre_a_jour():
    try:
        produit_id = int(input("ID du produit à modifier : "))
        nom = input("Nouveau nom : ")
        description = input("Nouvelle description : ")
        categorie = input("Nouvelle catégorie : ")
        prix = float(input("Nouveau prix : "))
        disponibilite = input("Nouvelle disponibilité (Disponible/Indisponible) : ")

        if prix <= 0:
            print("❌ Le prix doit être un nombre positif.")
            return

        r = requests.put(f"{API_URL}/api/produit/{produit_id}", json={
            "nom": nom, "description": description, "categorie": categorie, "prix": prix, "disponibilite": disponibilite
        })
        r.raise_for_status()
        print("✅ Produit mis à jour :", r.json())
    except requests.exceptions.RequestException as e:
        print(f"❌ Erreur lors de la mise à jour du produit : {e}")

if __name__ == "__main__":
    while True:
        afficher_menu()
        choix = input("Choix : ")
        if choix == "1":
            voir_produits()
        elif choix == "2":
            ajouter_produit()
        elif choix == "3":
            supprimer_produit()
        elif choix == "4":
            mettre_a_jour()
        elif choix == "5":
            print("👋 Au revoir !")
            break
        else:
            print("Choix invalide.")
