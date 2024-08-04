from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData

meta = MetaData()
Base = declarative_base(metadata=meta)

def to_dict(self):
    def get_value(self, column: str):
        value = getattr(self, column.name, None)
        if isinstance(value, decimal.Decimal):
            value = float(value)
        if isinstance(value, datetime):
            value = value.strftime('%Y-%m-%d %H:%M:%S')
        return value
    return {c.name: get_value(self, c) for c in self.__table__.columns}


Base.to_dict = to_dict