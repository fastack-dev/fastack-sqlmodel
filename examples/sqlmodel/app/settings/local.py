DEBUG = True
PLUGINS = [
    "fastack_sqlmodel",
]
COMMANDS = ["app.commands.book.cli"]

DB_USER = "fastack_user"
DB_PASSWORD = "fastack_pass"
DB_HOST = "localhost"
DB_PORT = 5888
DB_NAME = "fastack_db"
SQLALCHEMY_DATABASE_URI = (
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)
SQLALCHEMY_OPTIONS = {}
