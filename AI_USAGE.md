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

Tool: Gemini
Prompt: "I am building a 'Guess the Country' full-stack app. I've decided on FastAPI (async), SQLite, and Vanilla JS. Help me plan the workflow (SADP), refine the requirements based on the task PDF, and design the initial database schema and backend structure."
AI Generated: A structured roadmap (SADP), a suggestion for an asynchronous approach to improve scalability, and a normalized SQLite schema design.
Manual Modifications: I reviewed the suggested stack to ensure it met the "Minimal UI" requirements. I decided to use aiosqlite instead of standard sqlite3 to maintain a fully non-blocking flow.

2. Project Setup & Git Configuration
Tool: Claude Code
Prompt: "Create a comprehensive .gitignore file for this project. Since I am using Python, FastAPI, SQLite, and VS Code, please ensure it ignores the venv/ folder, __pycache__, .vscode/, and the SQLite database file."
AI Generated: A standard .gitignore file tailored for the specific tech stack.
Manual Modifications: Verified that the database file extension (*.db) was correctly included to prevent local data from being committed to the repository.