from models import Base, engine

# create the database
Base.metadata.create_all(engine)
