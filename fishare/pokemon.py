from dataclasses import Field

from sqlmodel import SQLModel, create_engine, Session, select


class Pokemon(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    pokedex_number: int
    name: str
    type1: str
    type2: str


db_uri = 'sqlite:///pokedex.sqlite'

engine = create_engine(db_uri)
with Session(engine) as session:
    statement = select(Pokemon).limit(10)
    pokemons = session.exec(statement).all()

    print(pokemons)
