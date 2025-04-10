from fastapi import FastAPI
from api import router

app = FastAPI()

# Inclusion des routes
app.include_router(router)