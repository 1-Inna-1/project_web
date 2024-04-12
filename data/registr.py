from flask_login import UserMixin
from .db_session import SqlAlchemyBase
class Users(SqlAlchemyBase, UserMixin):
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.__user['id'])
