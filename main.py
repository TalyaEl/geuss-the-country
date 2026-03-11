from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from database import SessionLocal, init_db, get_random_country, get_country_by_id

@asynccontextmanager
# Lifespan Handles startup logic. 
# Initialize the DB and seed data once when the server starts.
async def lifespan(app: FastAPI):
    await init_db()
    yield

# Initialize FastAPI
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
        id=country.id,
        clues=[country.clue1, country.clue2, country.clue3],
    )


class GuessRequest(BaseModel):
    country_id: int
    guess: str

# POST endpoint to validate the user's guess against the stored country name
# Comparison is case-insensitive and strips leading/trailing whitespace
@app.post("/api/guess")
async def submit_guess(body: GuessRequest):
    async with SessionLocal() as session:
        country = await get_country_by_id(session, body.country_id)

    if country is None:
        raise HTTPException(status_code=404, detail="Country not found.")

    is_correct = body.guess.strip().lower() == country.name.lower()
    if is_correct:
        return {"Correct!"}
    return {f"Wrong. The correct answer is {country.name}."}
