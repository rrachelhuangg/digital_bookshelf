from flask import Blueprint, abort, jsonify, render_template

from . import books

bp = Blueprint("main", __name__)

STATUSES = ["reading", "finished", "want-to-read"]


@bp.route("/")
def index():
    shelves = [(status, books.by_status(status)) for status in STATUSES]
    return render_template("index.html", shelves=shelves, total=len(books.all_books()))


@bp.route("/book/<slug>")
def book_detail(slug):
    book = books.get_book(slug)
    if book is None:
        abort(404)
    return render_template("book.html", book=book)


@bp.route("/api/books")
def api_books():
    return jsonify(books.all_books())


@bp.route("/healthz")
def healthz():
    return {"status": "ok"}


@bp.app_errorhandler(404)
def not_found(_error):
    return render_template("404.html"), 404
