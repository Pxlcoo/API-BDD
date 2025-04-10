from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

router = APIRouter()

# Config base de données
DATABASE_URL = "mysql+mysqlconnector://root:@localhost:3306/pizzeriaDB"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# Modèle SQLAlchemy
class Produit(Base):
    __tablename__ = "produits"
    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(255))
    prix = Column(Float)

# Crée la table au démarrage (si elle n’existe pas)
Base.metadata.create_all(bind=engine)

# Schémas Pydantic
class ProduitCreate(BaseModel):
    nom: str
    prix: float

class ProduitOut(ProduitCreate):
    id: int

# Endpoints

@router.get("/produits", response_model=List[ProduitOut])
def lire_produits():
    session = SessionLocal()
    produits = session.query(Produit).all()
    session.close()
    return produits

@router.post("/produits", response_model=ProduitOut)
def ajouter_produit(produit: ProduitCreate):
    session = SessionLocal()
    db_produit = Produit(nom=produit.nom, prix=produit.prix)
    session.add(db_produit)
    session.commit()
    session.refresh(db_produit)
    session.close()
    return db_produit

@router.delete("/produits/{produit_id}")
def supprimer_produit(produit_id: int):
    session = SessionLocal()
    produit = session.query(Produit).get(produit_id)
    if not produit:
        session.close()
        raise HTTPException(status_code=404, detail="Produit non trouvé")
    session.delete(produit)
    session.commit()
    session.close()
    return {"message": "Produit supprimé"}

@router.put("/produits/{produit_id}", response_model=ProduitOut)
def maj_produit(produit_id: int, produit_data: ProduitCreate):
    session = SessionLocal()
    produit = session.query(Produit).get(produit_id)
    if not produit:
        session.close()
        raise HTTPException(status_code=404, detail="Produit non trouvé")
    produit.nom = produit_data.nom
    produit.prix = produit_data.prix
    session.commit()
    session.refresh(produit)
    session.close()
    return produit