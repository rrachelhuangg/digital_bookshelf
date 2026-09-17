"""Book data access.

Reads from a bundled JSON file. Vercel functions have a read-only filesystem,
so swap this module for a real database client (Postgres, Turso, Supabase, ...)
when you want to add or edit books at runtime.
"""

import hashlib
import json
from functools import lru_cache
from pathlib import Path

DATA_FILE = Path(__file__).parent / "data" / "books.json"
COVER_DIR = Path(__file__).parent / "static" / "covers"

FAVORITES = "favorites"

# Cloth colors for the spines, each paired with a foil tone for the lettering.
BINDINGS = [
    {"cloth": "#6d2f31", "foil": "#e9cfa1"},  # oxblood
    {"cloth": "#2c4436", "foil": "#dcd2ab"},  # forest
    {"cloth": "#26364f", "foil": "#d9c79c"},  # navy
    {"cloth": "#8a6a2f", "foil": "#f6ead1"},  # mustard
    {"cloth": "#2b4a4c", "foil": "#e3d4b0"},  # teal
    {"cloth": "#4a2f47", "foil": "#e6cdb6"},  # plum
    {"cloth": "#8a4a2c", "foil": "#f3dfc2"},  # ochre
    {"cloth": "#3b3f44", "foil": "#d8d3c6"},  # slate
]


def binding(slug):
    """Stable per-book spine geometry and color, derived from the slug.

    Hashing the slug (rather than using the loop index) keeps a book's
    appearance fixed as the shelf is reordered or added to.
    """
    h = int(hashlib.sha1(slug.encode()).hexdigest(), 16)
    return {
        **BINDINGS[h % len(BINDINGS)],
        "height": 152 + (h >> 8) % 56,
        "width": 30 + (h >> 16) % 17,
    }


@lru_cache(maxsize=1)
def _load(_mtime):
    with DATA_FILE.open(encoding="utf-8") as f:
        books = json.load(f)
    return sorted(books, key=lambda b: (b["author"].split()[-1], b["title"]))


def all_books():
    """Parsed books.json, cached on the file's mtime.

    Keying the cache on mtime means editing books.json shows up on the next
    request locally, while a deployed function (where the file never changes)
    still parses it only once.
    """
    return _load(DATA_FILE.stat().st_mtime_ns)


def _on_shelf(shelf):
    """Which books belong on a given shelf.

    "favorite" is a flag rather than a status, so a favorite keeps its real
    reading status but is promoted onto the favorites shelf — it appears
    once, in pride of place, instead of twice.
    """
    if shelf == FAVORITES:
        return [b for b in all_books() if b.get("favorite")]
    return [b for b in all_books() if b["status"] == shelf and not b.get("favorite")]


def cover_file(book):
    """The book's cover filename, but only if that image is really there.

    A missing or misspelled filename degrades to a drawn spine instead of a
    broken image, so entries can be added to books.json before the artwork is.
    """
    name = book.get("cover")
    if name and (COVER_DIR / name).is_file():
        return name
    return None


def _view(book):
    """A book decorated with everything the templates need to draw it."""
    return dict(book, binding=binding(book["slug"]), cover=cover_file(book))


def shelved(shelf):
    """Books for one shelf, ready to render."""
    return [_view(b) for b in _on_shelf(shelf)]
