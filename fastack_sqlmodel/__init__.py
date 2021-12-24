from fastack import Fastack
from sqlalchemy.engine import Engine
from sqlalchemy.orm.session import close_all_sessions
from sqlmodel import SQLModel, create_engine

from fastack_sqlmodel.session import Session


class DatabaseState:
    def __init__(self, engine: Engine):
        self.engine = engine

    def open(self, engine: Engine = None, **kwds) -> Session:
        engine = engine or self.engine
        session = Session(self.engine, **kwds)
        return session


def setup(app: Fastack):
    def on_startup():
        uri = getattr(app.state.settings, "SQLALCHEMY_DATABASE_URI", None)
        if not uri:
            raise RuntimeError("SQLALCHEMY_DATABASE_URI is not set")

        options = getattr(app.state.settings, "SQLALCHEMY_OPTIONS", {})
        engine = create_engine(uri, **options)
        app.state.db = DatabaseState(engine)
        SQLModel.metadata.create_all(engine)

    def on_shutdown():
        close_all_sessions()

    app.add_event_handler("startup", on_startup)
    app.add_event_handler("shutdown", on_shutdown)
