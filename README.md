# Telegram Support Bot

A production-ready Telegram support ticket bot built with **Python 3.11**, **aiogram 3**, and **SQLite**.

This project implements a structured support workflow inside Telegram: users open tickets in a private chat, support staff receives new tickets in a dedicated group, and the assigned agent gets the user's contact details privately.

---

## Overview

The bot is designed for teams that want a simple and secure way to handle support requests directly in Telegram without exposing user contact data in a shared staff chat.

### Current workflow

- A user starts the bot in a private chat
- The user selects a language
- The user sends their issue in a single text message
- The bot creates a ticket and posts it to the admin group
- A staff member claims the ticket
- The bot sends user details privately to the assigned staff member
- The user receives a notification telling them exactly which staff member will contact them
- The assigned staff member closes the ticket from private chat

---

## Features

- Multi-language onboarding on first start
- Supported languages:
  - English
  - Russian
  - Spanish
- Ticket creation from the first user text message
- Duplicate active ticket protection
- Safe ticket posting to an admin group
- No user contact details in the admin group
- Private delivery of user details to the assigned agent
- Ticket claiming with race-condition-safe database update
- Ticket closing restricted to the assigned agent
- SQLite-based persistence layer
- Docker support
- Simple modular project structure
- Basic database test script included

---

## Ticket lifecycle

open → claimed → closed

### Status meanings

- open — waiting for agent
- claimed — assigned to agent
- closed — resolved

---

## Project structure

support_bot_final/

app/
    handlers/
        admin.py
        user.py

    keyboards/
        admin.py
        user.py

    services/
        database.py
        tickets.py

    locales/
        texts.py

    utils/
        time.py

config.py
main.py
requirements.txt
.env.example
Dockerfile
README.md

---

## Technology stack

- Python 3.11
- aiogram 3
- SQLite
- aiosqlite
- python-dotenv
- Docker

---

## Requirements

- Python 3.11
- Telegram bot token (BotFather)
- Telegram group for support agents
- Bot added to that group with permission to send and edit messages

---

## Installation

Clone repository

git clone [https://github.com/xXxMOTxXx/telegram-support-bot](https://github.com/xXxMOTxXx/telegram-support-bot)

cd telegram-support-bot

Create virtual environment

python -m venv .venv

Activate environment

Linux / macOS
source .venv/bin/activate

Windows
.venv\Scripts\activate

Install dependencies

pip install -r requirements.txt

Create environment file

cp .env.example .env

Configure environment variables

BOT_TOKEN=YOUR_TELEGRAM_BOT_TOKEN
ADMIN_GROUP_ID=-100XXXXXXXXXX
DB_PATH=data/support_bot.db
TIMEZONE=Europe/Berlin

Run bot

python main.py

---

## Environment variables

BOT_TOKEN — Telegram bot token

ADMIN_GROUP_ID — Telegram support group ID

DB_PATH — path to SQLite database file

TIMEZONE — timezone used for timestamps

---

## Security model

Admin group receives:

- ticket id
- creation time
- language
- first message

Admin group does NOT receive:

- user telegram id
- username
- full name

User details are sent only to the support agent who claims the ticket.

---

## Database

Two tables are used.

users
- user_id
- username
- full_name
- language
- created_at
- updated_at

tickets
- id
- user_id
- language
- first_message
- status
- assigned_admin_id
- assigned_admin_username
- assigned_admin_name
- group_chat_id
- group_message_id
- created_at
- claimed_at
- closed_at

---

## Tests

Basic database test included:

tests/test_database.py

Run:

python tests/test_database.py

---

## Current limitations

The current version intentionally keeps the system simple.

Not included yet:

- webhook mode
- PostgreSQL support
- Redis
- analytics dashboard
- ticket categories
- rate limiting

These can be added later depending on project needs.

---

## License

Add a license only if you want to allow code reuse.

If you plan to use MIT license, add a LICENSE file to the repository.
