from typing import Optional, Tuple
from model.store import DatabaseName, Store, Username
from model.database import Database
from dataclasses import dataclass


@dataclass
class Context:
  "A temporary storage for the connected clients to store their state during the lifetime of the connection."

  store: Store
  response: str = str()
  username: Username = str()
  database_name: DatabaseName = str()
  database: Optional[Database] = None
  params: Tuple[str, ...] = tuple()
