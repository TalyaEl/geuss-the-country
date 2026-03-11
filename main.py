from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from database import SessionLocal, init_db, get_random_country

@asynccontextmanager
# Lifespan Handles startup logic. 
# Initialize the DB and seed data once when the server starts.
async def lifespan(app: FastAPI):
    await init_db()
    yield

# Initialize F
app = FastAPI(lifespan=lifespan)

# Defines the API contract.
# Only returns id and clues to keep the country name hidden from the client.
class CountryResponse(BaseModel):
    id: int
    clues: list[str]

# GET endpoint to fetch a random challenge.
# Uses an async database session to avoid blocking the event loop.
@app.get("/api/country/random", response_model=CountryResponse)
async def random_country():
    async with SessionLocal() as session:
        country = await get_random_country(session)

    if country is None:
        raise HTTPException(status_code=404, detail="No countries found.")

    return CountryResponse(
        id = country.id,
        clues=[country.clue1, country.clue2, country.clue3],)
