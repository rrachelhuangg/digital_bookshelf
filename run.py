"""Local dev server. Vercel does not use this file — see api/index.py."""

from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True, port=5000)
