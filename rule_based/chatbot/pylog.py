import sqlite3


class LogQuery:
    def __init__(self, user='Anonymous'):
        self.username = user
        self.connection = sqlite3.connect('db.userlog', check_same_thread=False)
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        statement = "CREATE TABLE IF NOT EXISTS UserLog (" \
                    "id INTEGER PRIMARY KEY," \
                    "username VARCHAR(100),"\
                    "query VARCHAR(1000),"\
                    "t_stamp CURRENT_TIMESTAMP)"
        self.cursor.execute(statement)
        self.connection.commit()

    def insert_data(self, user_query):
        statement = r"INSERT INTO UserLog" \
                     "(username, query, t_stamp)" \
                     "VALUES ('{}','{}',CURRENT_TIMESTAMP)".format(self.username, user_query)
        self.cursor.execute(statement)
        self.connection.commit()

    def fetch_data(self):
        user_log = list()
        statement = "SELECT * FROM UserLog"
        self.cursor.execute(statement)
        headers = [desc[0] for desc in self.cursor.description]
        for row in self.cursor:
            user_log.append(dict(zip(headers, row)))
        return user_log

