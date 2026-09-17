from flask import Blueprint, jsonify, render_template

from . import books

bp = Blueprint("main", __name__)

# Top shelf first. "favorites" is a flag on a book, the rest are statuses.
SHELVES = ["reading", books.FAVORITES, "finished", "want-to-read"]


@bp.route("/")
def index():
    shelves = [(name, books.shelved(name)) for name in SHELVES]
    return render_template("index.html", shelves=shelves, total=len(books.all_books()))


@bp.route("/api/books")
def api_books():
    return jsonify(books.all_books())


@bp.route("/healthz")
def healthz():
    return {"status": "ok"}


@bp.app_errorhandler(404)
def not_found(_error):
    return render_template("404.html"), 404
