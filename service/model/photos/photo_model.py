"""
PhotoModel — user photo model.

## Traceability
Feature: F003 — Photo storage
Scenarios: SC004, SC005, SC006
"""
from sqlalchemy import BigInteger, Column, String

from model.base_model import Base, BaseModel


class PhotoModel(Base, BaseModel):
    __tablename__ = "photos"

    user_id = Column(BigInteger, nullable=False, index=True)
    file_id = Column(String(255), nullable=False)
    file_path = Column(String(1024), nullable=True)
