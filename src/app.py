"""
Flask app setup.
"""
from os import getenv
from flask import Flask
from db import db
import jinjaUtils
from routes import registerRoutes

app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")

# Register routes
registerRoutes(app)

# Register db
databaseUrl = getenv("DATABASE_URL")
if databaseUrl:
    databaseUrl = databaseUrl.replace('postgres://', 'postgresql://')

app.config["SQLALCHEMY_DATABASE_URI"] = databaseUrl
db.init_app(app)

# Register Jinja utils


@app.context_processor
def addJinjaUtils():
    """
    Add utility functions from jinjaUtils to the Jinja context.
    """
    return jinjaUtils.utilityProcessor()


if __name__ == "__main__":
    app.run()
