from database import Base, engine
import models

# Creamos las tablas en la base de datos
Base.metadata.create_all(bind=engine)
