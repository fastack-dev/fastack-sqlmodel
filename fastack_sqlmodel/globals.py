from fastack.globals import state
from werkzeug.local import LocalProxy

from fastack_sqlmodel import DatabaseState

db: DatabaseState = LocalProxy(lambda: getattr(state, "db", None))
