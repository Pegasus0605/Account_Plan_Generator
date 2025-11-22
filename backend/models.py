from sqlalchemy import Column, String, Text
from backend.db import Base


class PlanSection(Base):
    __tablename__ = "plan_sections"

    section_name = Column(String, primary_key=True, index=True)
    content = Column(Text, nullable=True)


class Metadata(Base):
    __tablename__ = "metadata"

    key = Column(String, primary_key=True, index=True)
    value = Column(Text, nullable=True)
