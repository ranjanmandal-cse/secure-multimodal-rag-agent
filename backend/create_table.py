from database import engine, Base
from models import Case, Evidence

Base.metadata.create_all(bind=engine)

print("Tables created successfully!")