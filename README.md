# Guess the Country

A stateless full-stack web application where the user is presented with three factual clues and must identify the correct country. The backend serves a random challenge on each request and validates the user's guess server-side, keeping the country name hidden from the client at all times.

---

## Live Demo
The application is deployed and accessible at:
**[https://guess-the-country-h2bt.onrender.com](https://guess-the-country-h2bt.onrender.com)**

---

## Features

- **Random challenge on every game** — a new country with 3 clues is fetched from the database on load and on reset
- **Case-insensitive, whitespace-tolerant validation** — `" JAPAN "`, `"japan"`, and `"Japan"` are all accepted as correct
- **Stateless REST API** — the server holds no session state; the client passes the `country_id` back with every guess
- **Fully asynchronous database queries** — all I/O is non-blocking using `async/await` and `aiosqlite`
- **Dynamic UI** — feedback and clues update without any page reload using the `fetch` API
- **Isolated automated tests** — an in-memory SQLite database ensures tests are fast and never affect production data

---

## Tech Stack

**Backend:** Python, FastAPI (async/await).
**Database:** SQLite · aiosqlite · SQLAlchemy 2.0 async ORM.
**Frontend:** Vanilla HTML, CSS (Flexbox), JavaScript — single `index.html`.
**Testing:** pytest · pytest-asyncio · httpx `AsyncClient`.

### Engineering Decisions

FastAPI was chosen for its first-class `async/await` support, which prevents the event loop from blocking during database queries - a critical property even for a small app, since synchronous SQLite calls would stall every concurrent request. The API is intentionally **stateless**: the server issues a `country_id` with each challenge and the client echoes it back on guess, so no server-side session tracking is needed. SQLAlchemy's async ORM provides a clean, type-safe query layer over `aiosqlite` without raw SQL. For testing, an **in-memory SQLite database** is swapped in via FastAPI's `dependency_overrides` mechanism, giving each test run a clean, predictable state with zero disk I/O.

---

## API Reference
### `GET /api/country/random`
Returns a randomly selected country challenge. The country name is **never** included in the response.
**Response `200 OK`**
```json
{
  "id": 3,
  "clues": [
    "This country is shaped like a boot.",
    "It is home to the Colosseum and the Vatican City.",
    "It gave the world pizza, pasta, and the Renaissance."
  ]
}
```

---

### `POST /api/guess`
Validates the user's guess against the stored country name.
**Request Body**
```json
{
  "country_id": 3,
  "guess": "italy"
}
```
**Response `200 OK` — Correct**
```json
{ "message": "Correct!" }
```
**Response `200 OK` — Wrong**
```json
{ "message": "Wrong. The correct answer is Italy." }
```
**Response `404 Not Found`** — when `country_id` does not exist
```json
{ "detail": "Country not found." }
```

---

## Local Setup & Running

**1. Clone the repository and navigate into the project folder**
```bash
git clone https://github.com/TalyaEl/guess-the-country
cd guess-the-country
```

**2. Create and activate a virtual environment**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Start the development server**
```bash
uvicorn main:app --reload
```

**5. Open the application**

Navigate to **http://127.0.0.1:8000** in your browser. The database is created and seeded automatically on first startup.

---

## Running the Tests

With the virtual environment activated, run:

```bash
pytest test_main.py -v
```

The test suite spins up an isolated in-memory database, seeds it with test data, and tears it down automatically — no `countries.db` file is touched.

**Expected output:**
```
test_main.py::test_random_country_returns_200_and_three_clues PASSED
test_main.py::test_guess_correct_japan_lowercase PASSED
test_main.py::test_guess_correct_brazil_with_spaces_and_caps PASSED
test_main.py::test_guess_wrong_returns_correct_answer PASSED
test_main.py::test_guess_unknown_id_returns_404 PASSED

5 passed in 0.88s
```
---

## AI Usage
AI tools (Gemini and Claude Code) were used during development to assist with architecture planning, generating boilerplate, and debugging. All generated code was reviewed, tested, and manually refined. For a full breakdown of every prompt, what was generated, and what was modified by hand, see **[AI_USAGE.md](AI_USAGE.md)**.
