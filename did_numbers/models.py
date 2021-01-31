from sqlalchemy import Column, Integer, String
from did_numbers.database import Base


class DIDNumber(Base):
    __tablename__ = 'didnumbers'

    id = Column(Integer, primary_key=True)

    value = Column(String(), nullable=False)
    monthly_price = Column(String(), nullable=False)
    setup_price = Column(Integer, nullable=False)
    monthly_price = Column(Integer, nullable=False)
    currency = Column(String(), nullable=False)
