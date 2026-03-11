AI Usage Documentation

This document describes how AI tools were used during the development of the "Guess the Country" application.

AI Tools Used

Gemini (Google): Used as a Senior Fullstack Mentor for project planning, architectural decisions, learning backend concepts (Async, FastAPI), and refining requirements.

Claude Code (Anthropic): Used as the primary development tool within VS Code for generating boilerplate code, managing Git configurations, and implementing the database and API logic.

AI Configuration

File: .claude.md (or equivalent)

Purpose: Guided the AI to follow a specific stack: Python (FastAPI), SQLite (aiosqlite), and Vanilla JS. It ensured the AI prioritized clean, asynchronous code and "Engineering Thinking."

Development Log

1. Planning & Architecture
**Tool:** Gemini
**Prompt:** "I am building a 'Guess the Country' full-stack app. I've decided on FastAPI (async), SQLite, and Vanilla JS. Help me plan the workflow (SADP), refine the requirements based on the task PDF, and design the initial database schema and backend structure."
**AI Generated:** A structured roadmap (SADP), a suggestion for an asynchronous approach to improve scalability, and a normalized SQLite schema design.
**Manual Modifications:** I reviewed the suggested stack to ensure it met the "Minimal UI" requirements. I decided to use aiosqlite instead of standard sqlite3 to maintain a fully non-blocking flow.

2. Project Setup & Git Configuration
**Tool:** Claude Code
**Prompt:** "Create a comprehensive .gitignore file for this project. Since I am using Python, FastAPI, SQLite, and VS Code, please ensure it ignores the venv/ folder, __pycache__, .vscode/, and the SQLite database file."
**AI Generated:** A standard .gitignore file tailored for the specific tech stack.
**Manual Modifications:** Verified that the database file extension (*.db) was correctly included to prevent local data from being committed to the repository.

3.
**Tool:** Claude Code
**Prompt:** "I need to implement the backend and database for my 'Guess the Country' app. 1. Database (database.py): Use SQLAlchemy with aiosqlite. Create a Country model with an id (Integer, Primary Key), name (String), and three clue strings. 2. Seeding: Add an init_db function that populates the DB with 7 countries. 3. Backend (main.py): Create a FastAPI app with a startup event and a GET endpoint /api/country/random that returns id and clues list."
**AI Generation:** Claude generated the database.py file with the SQLAlchemy models and seeding logic, and the main.py file with the FastAPI application and the asynchronous endpoint.
**Manual Modifications:** I manually updated the SEED_DATA list to include a more diverse set of countries, including Israel. I also rewrote the clues to ensure they are factually interesting and provided at varying difficulty levels. I added comments in `database.py` and `main.py` to improve code maintainability. I reviewed and corrected the grammar and punctuation of the AI-generated clues

4.
**Tool:** Gemini
**Prompt:** "I need to move to Creating the Validation Endpoint. Guide me through the architectural design: POST vs GET, Request Body for a stateless server, and response structure based on the task requirements."
**AI Generation:** Provided a detailed architectural rationale for using POST over GET. Explaining that the client must provide the country_id back to the server(statelessness). It also helped define a clear response contract to ensure the output matches the required format according to the instructions in the PDF.
**Manual Modifications:** I instructed the AI to trimming whitespaces from the inoput and change it to lower case letters. While the AI suggested the basic architecture, I identified these as critical edge cases.

5.
**Tool:** Claude Code
**Prompt:** "I need to implement a validation endpoint in main.py for my 'Guess the Country' app.
1. Pydantic Model: Create a GuessRequest class with country_id (int) and guess (str).
2. Endpoint: Create a POST endpoint at /api/guess.
3. Logic: Fetch the country from the SQLite database using the provided country_id. If the country is not found, raise an HTTPException with status code 404.
Compare the user's guess with the name in the database. Ensure the comparison is case-insensitive and ignores leading/trailing whitespace.Response: Return a JSON object following these requirements: if correct, return 'Correct!'; if wrong, return 'Wrong. The correct answer is [Country Name].'.Please use the existing get_db dependency and ensure the database operation is awaited for asynchronous efficiency."
**AI Generation:** Added get_country_by_id in database.py — uses session.get() (primary key lookup, no manual query needed).
GuessRequest model in main.py — validates country_id: int and guess: str
POST /api/guess — fetches the country by id, compares .strip().lower() vs the stored name, and returns the appropriate message
**Manual Modifications:** I adjusted the response strings to match the project instructions (it was with 'The result is'). I added comprehensive comments to the generated code.