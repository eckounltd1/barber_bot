import sqlite3



class Database:
    def __init__(self,db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()


    def add_user(self, user_id):
        with self.connection:
            self.cursor.execute("INSERT INTO 'users' ('user_id') VALUE (?)", (user_id, ))

    def user_exists(self,user_id):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM 'users' WHERE 'user_id' = ?", (user_id,)).fetchall()
            return bool(len(result))

    def set_name(self, user_id, name):
        with self.connection:
            return self.cursor.execute("UPDATE 'users' SET 'name' = ? WHERE 'user_id' = ?", (name, user_id))

    def choice_service(self, user_id, service):
        with self.connection:
            return self.cursor.execute("UPDATE 'users' SET 'service' = ? WHERE 'user_id' = ?", (service, user_id))