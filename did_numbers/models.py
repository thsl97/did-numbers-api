import re

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import validates
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
            'monthlyPrice': self.monthly_price / 100,
            'setupPrice': self.setup_price / 100,
            'currency': self.currency
        }

    @validates('value')
    def validate_value(self, key, address):
        """Checks that phone number matches pattern"""
        # +00 00 00000-0000
        phone_pattern = re.compile(
            r'^\+(\d{2}) (\d{2}) (\d{5})-(\d{4})$'
        )
        assert phone_pattern.match(address) is True, ('Value does not match '
                                                      'correct pattern')
        return address

    @validates('monthly_price', 'setup_price')
    def validate_prices(self, key, address):
        assert address > 0, 'Prices must be positive numbers'
        return address
