from flask_login import UserMixin
from .db_session import SqlAlchemyBase
class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.__user['id'])
