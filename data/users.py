import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin
from werkzeug.security import generate_password_hash, check_password_hash


class Article(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    title = sqlalchemy.Column(sqlalchemy.String(100), nullable=False)
    intro = sqlalchemy.Column(sqlalchemy.String(300), nullable=False)
    text = sqlalchemy.Column(sqlalchemy.Text, nullable=False)
    date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    #image_file = sqlalchemy.Column(sqlalchemy.String(20), nullable=False)


    def __repr__(self):
        return '<Article %r>' % self.id