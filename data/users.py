import sqlalchemy
from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, unique=True, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    number_phone = sqlalchemy.Column(sqlalchemy.String, unique=True)
    quest_1 = sqlalchemy.Column(sqlalchemy.INT)
    quest_2 = sqlalchemy.Column(sqlalchemy.INT)
    quest_3 = sqlalchemy.Column(sqlalchemy.INT)
    quest_4 = sqlalchemy.Column(sqlalchemy.INT)
    quest_5 = sqlalchemy.Column(sqlalchemy.INT)
