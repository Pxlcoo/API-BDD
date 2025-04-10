from fastapi import FastAPI, APIRouter, HTTPException
from pydantic import BaseModel, validator
from typing import List
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
import os
import logging

# Logging configuration
logging.basicConfig(level=logging.INFO)

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "mysql+mysqlconnector://root:@localhost:3306/pizzeriadb")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# SQLAlchemy model
class Produit(Base):
    __tablename__ = "produit"
    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(255))
    description = Column(String(255))  # Example additional column
    prix = Column(Float)
    categorie = Column(String(255))  # Example additional column
    disponibilite = Column(String(50))  # Example additional column

# Create the table if it doesn't exist
Base.metadata.create_all(bind=engine)

# Pydantic schemas
class ProduitCreate(BaseModel):
    nom: str
    prix: float
    description: str = ""
    categorie: str = ""
    disponibilite: str = "Disponible"

    @validator('prix')
    def check_prix_positive(cls, value):
        if value <= 0:
            raise ValueError("Le prix doit être positif.")
        return value

class ProduitOut(ProduitCreate):
    id: int

# Router setup
router = APIRouter()

@router.get("/produit", response_model=List[ProduitOut])
def lire_produits():
    with SessionLocal() as session:
        try:
            produits = session.query(Produit).all()
            logging.info("Produits récupérés avec succès.")
            return produits
        except SQLAlchemyError as e:
            logging.error(f"Erreur SQL: {str(e)}")
            raise HTTPException(status_code=500, detail="Erreur lors de la récupération des produits")

@router.post("/produit", response_model=ProduitOut)
def ajouter_produit(produit: ProduitCreate):
    with SessionLocal() as session:
        try:
            db_produit = Produit(**produit.dict())
            session.add(db_produit)
            session.commit()
            session.refresh(db_produit)
            logging.info("Produit ajouté avec succès.")
            return db_produit
        except SQLAlchemyError as e:
            logging.error(f"Erreur SQL: {str(e)}")
            raise HTTPException(status_code=500, detail="Erreur lors de l'ajout du produit")

@router.delete("/produit/{produit_id}")
def supprimer_produit(produit_id: int):
    with SessionLocal() as session:
        try:
            produit = session.query(Produit).filter(Produit.id == produit_id).first()
            if not produit:
                raise HTTPException(status_code=404, detail="Produit non trouvé")
            session.delete(produit)
            session.commit()
            logging.info(f"Produit supprimé: ID {produit_id}")
            return {"message": "Produit supprimé"}
        except SQLAlchemyError as e:
            logging.error(f"Erreur SQL: {str(e)}")
            raise HTTPException(status_code=500, detail="Erreur lors de la suppression du produit")

@router.put("/produit/{produit_id}", response_model=ProduitOut)
def maj_produit(produit_id: int, produit_data: ProduitCreate):
    with SessionLocal() as session:
        try:
            produit = session.query(Produit).filter(Produit.id == produit_id).first()
            if not produit:
                raise HTTPException(status_code=404, detail="Produit non trouvé")
            for key, value in produit_data.dict().items():
                setattr(produit, key, value)
            session.commit()
            session.refresh(produit)
            logging.info(f"Produit mis à jour: ID {produit_id}")
            return produit
        except SQLAlchemyError as e:
            logging.error(f"Erreur SQL: {str(e)}")
            raise HTTPException(status_code=500, detail="Erreur lors de la mise à jour du produit")

# FastAPI application setup
app = FastAPI()
app.include_router(router, prefix="/api")
