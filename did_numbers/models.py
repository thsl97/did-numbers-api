from sqlalchemy import Column, Integer, String
from did_numbers.database import Base


class DIDNumber(Base):
    __tablename__ = 'didnumbers'

    id = Column(Integer, primary_key=True)

    value = Column(String(), nullable=False)
    monthly_price = Column(Integer, nullable=False)
    setup_price = Column(Integer, nullable=False)
    currency = Column(String(), nullable=False)

    @property
    def serialized(self):
        """Returns object data in serialized format"""
        return {
            'id': self.id,
            'value': self.value,
            'monthlyPrice': self.monthly_price,
            'setupPrice': self.setup_price,
            'currency': self.currency
        }
