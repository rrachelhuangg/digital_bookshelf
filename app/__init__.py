import os

from flask import Flask


def create_app(config=None):
    """Application factory.

    Templates and static files resolve relative to this package, so both the
    local dev server and the Vercel function find them at the same paths.
    """
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY", "dev-only-not-for-production"),
        SITE_TITLE=os.environ.get("SITE_TITLE", "2026 Digital Bookshelf"),
    )
    if config:
        app.config.from_mapping(config)

    from .routes import bp

    app.register_blueprint(bp)

    return app
