import sqlalchemy
from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, unique=True, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    number_phone = sqlalchemy.Column(sqlalchemy.String)
    job = sqlalchemy.Column(sqlalchemy.INT)
    marry = sqlalchemy.Column(sqlalchemy.INT)
    time_job = sqlalchemy.Column(sqlalchemy.INT)
    years_old = sqlalchemy.Column(sqlalchemy.INT)
    exp = sqlalchemy.Column(sqlalchemy.INT)
