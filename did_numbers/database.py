from sqlalchemy.engine import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


SQL_ALCHEMY_DATABASE_URL = 'sqlite://'


engine = create_engine(SQL_ALCHEMY_DATABASE_URL)


db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False,
                                         bind=engine))


Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    from did_numbers.models import DIDNumber  # noqa: F401
    Base.metadata.create_all(bind=engine)
