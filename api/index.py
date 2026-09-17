"""Vercel serverless entrypoint.

Vercel's Python runtime looks for a module-level WSGI callable named `app`,
and vercel.json rewrites every request to this function.
"""

from app import create_app

app = create_app()
