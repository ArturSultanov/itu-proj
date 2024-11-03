# backend/src/database/__init__.py

from .database import Base  # Import the base class for models
from .models import PlayerOrm, GameOrm  # Import the models to register them with Base
