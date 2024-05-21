from flask_login import UserMixin
from utils import *

class Paciente(UserMixin):
    def __init__(self, user_id):
        self.id = user_id

    @staticmethod
    def get(user_id):
        conn, cursor = get_db_connection()
        cursor.execute("SELECT * FROM paciente WHERE user_id = %s", (user_id,))
        user_data = cursor.fetchone()
        cursor.close()
        conn.close()
        if user_data:
            return Paciente(user_id=user_id)
        return None

    def is_active(self):
        return True
