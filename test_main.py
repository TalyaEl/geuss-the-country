import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from database import Base, Country
from main import app, get_db

# In-Memory database setup for isolated testing
# This ensures tests run fast and do not affect the production SQLite file
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

# Mock Data
TEST_COUNTRIES = [
    Country(id=1, name="Japan",
            clue1="Bowing is a standard greeting.",
            clue2="It features the world's busiest pedestrian crossing.",
            clue3="Cherry blossoms are a celebrated symbol of its culture."),
    Country(id=2, name="Brazil",
            clue1="This country contains the majority of the Amazon Rainforest.",
            clue2="It has won the FIFA World Cup a record five times.",
            clue3="It has more than 400 public airports."),
]

@pytest_asyncio.fixture(scope="session", autouse=True)
async def override_db():
    """Setup the in-memory database and apply dependency injection for the test session."""
    test_engine = create_async_engine(TEST_DATABASE_URL)
    TestSessionLocal = async_sessionmaker(test_engine, expire_on_commit=False)

    # Create tables and seed mock data
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with TestSessionLocal() as session:
        session.add_all(TEST_COUNTRIES)
        await session.commit()

    # The FastAPI Way: Dependency Injection override
    # This securely swaps the production database dependency with our test session
    async def override_get_db():
        async with TestSessionLocal() as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db

    yield

    # Cleanup after tests finish
    app.dependency_overrides.clear()
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await test_engine.dispose()

@pytest_asyncio.fixture
async def client():
    """Create an asynchronous HTTPX client to perform requests against the test application."""
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac

# ---------------------------------------------------------------------------
# Tests: GET /api/country/random
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_random_country_returns_200_and_three_clues(client):
    response = await client.get("/api/country/random")

    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert "clues" in data
    assert len(data["clues"]) == 3

# ---------------------------------------------------------------------------
# Tests: POST /api/guess — Correct Guesses
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_guess_correct_japan_lowercase(client):
    response = await client.post("/api/guess", json={"country_id": 1, "guess": "japan"})

    assert response.status_code == 200
    assert response.json()["message"] == "Correct!"

@pytest.mark.asyncio
async def test_guess_correct_brazil_with_spaces_and_caps(client):
    # Verify the system correctly handles whitespace and case sensitivity edge cases
    response = await client.post("/api/guess", json={"country_id": 2, "guess": "  BRAZIL  "})

    assert response.status_code == 200
    assert response.json()["message"] == "Correct!"

# ---------------------------------------------------------------------------
# Tests: POST /api/guess — Incorrect Guesses
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_guess_wrong_returns_correct_answer(client):
    response = await client.post("/api/guess", json={"country_id": 1, "guess": "USA"})

    assert response.status_code == 200
    data = response.json()
    assert "Wrong" in data["message"]
    assert "Japan" in data["message"]

# ---------------------------------------------------------------------------
# Tests: POST /api/guess — 404 Error for unknown ID
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_guess_unknown_id_returns_404(client):
    response = await client.post("/api/guess", json={"country_id": 9999, "guess": "Anywhere"})

    assert response.status_code == 404