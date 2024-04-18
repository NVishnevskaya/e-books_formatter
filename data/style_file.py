import sqlalchemy
from flask_login import UserMixin
from .db_session import SqlAlchemyBase


class StyleFile(SqlAlchemyBase, UserMixin):
    __tablename__ = 'styles'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    font_size = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    font_color = sqlalchemy.Column(sqlalchemy.String, default='black')
    font_family = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    """"
    file_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("files.id"))
    files = orm.relationship('Files')
    """

