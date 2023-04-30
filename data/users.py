import sqlalchemy
from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, unique=True, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    number_phone = sqlalchemy.Column(sqlalchemy.String)
    job = sqlalchemy.Column(sqlalchemy.Integer)
    marry = sqlalchemy.Column(sqlalchemy.Integer)
    time_job = sqlalchemy.Column(sqlalchemy.Integer)
    years_old = sqlalchemy.Column(sqlalchemy.Integer)
    exp = sqlalchemy.Column(sqlalchemy.Integer)
