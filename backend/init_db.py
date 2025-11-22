from backend.db import Base, engine
from backend.models import PlanSection, Metadata

def init_db():
    Base.metadata.create_all(bind=engine)
