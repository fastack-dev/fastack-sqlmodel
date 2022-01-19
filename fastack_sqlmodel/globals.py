from fastack.globals import state, LocalProxy

from fastack_sqlmodel import DatabaseState

def _get_db():
    db = getattr(state, "db", None)
    if not isinstance(db, DatabaseState):
        raise RuntimeError("Database not initialized")
    return db

db: DatabaseState = LocalProxy(_get_db)
