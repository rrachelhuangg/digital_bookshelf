"""Book data access.

Reads from a bundled JSON file. Vercel functions have a read-only filesystem,
so swap this module for a real database client (Postgres, Turso, Supabase, ...)
when you want to add or edit books at runtime.
"""

import json
from functools import lru_cache
from pathlib import Path

DATA_FILE = Path(__file__).parent / "data" / "books.json"


@lru_cache(maxsize=1)
def all_books():
    with DATA_FILE.open(encoding="utf-8") as f:
        books = json.load(f)
    return sorted(books, key=lambda b: (b["author"].split()[-1], b["title"]))


def get_book(slug):
    return next((b for b in all_books() if b["slug"] == slug), None)


def by_status(status):
    return [b for b in all_books() if b["status"] == status]
