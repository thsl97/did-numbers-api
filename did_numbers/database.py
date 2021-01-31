import click

from sqlalchemy.engine import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from flask.cli import with_appcontext


SQL_ALCHEMY_DATABASE_URL = 'postgresql://psqluser:abcd1234@db:5432/didnumbers'


engine = create_engine(SQL_ALCHEMY_DATABASE_URL)


db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False,
                                         bind=engine))


Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    """Initializes the database"""
    from did_numbers.models import DIDNumber  # noqa: F401
    Base.metadata.create_all(bind=engine)


@click.command('create-db')
@with_appcontext
def create_db_command():
    """Adds a cli command for database initialization"""
    init_db()
    click.echo('Database initialized')


def init_app(app):
    """Adds the create_db_command to flask cli"""
    app.cli.add_command(create_db_command)
