import sqlalchemy
import sqlmodel
from sqlalchemy.ext.automap import automap_base
from sqlmodel import Field, SQLModel, Session, select


class Pokemon(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    pokedex_number: int
    name: str
    type1: str
    type2: str


db_uri = 'sqlite:///pokedex.sqlite'


def pokedex_with_sqlmodel():
    engine = sqlmodel.create_engine(db_uri)
    with Session(engine) as session:
        statement = select(Pokemon).limit(10)
        pokemons = session.exec(statement).all()

        print(pokemons)


def pokedex_with_sqlalchemy():
    Base = automap_base()
    engine = sqlalchemy.create_engine('sqlite:///database.db')
    Base.prepare(autoload_with=engine)

    FileDetails = Base.classes.filedetails

    with sqlalchemy.orm.Session(engine) as session:
        files = session.query(FileDetails).all()
        for file in files:
            print(file.filename)


pokedex_with_sqlalchemy()
