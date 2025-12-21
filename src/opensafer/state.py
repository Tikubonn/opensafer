
from enum import Enum, unique, auto

@unique
class State (Enum):
  
  PENDING = auto()
  MOVED = auto()
  CLEANEDUP = auto()
