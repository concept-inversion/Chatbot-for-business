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
                    "probable_question varchar(255),"\
                    "attempted_response varchar(255),"\
                    "semantic_similarity float,"\
                    "t_stamp CURRENT_TIMESTAMP)"
        self.cursor.execute(statement)
        self.connection.commit()

    def insert_data(self, user_query, probable_question, attempted_response, semantic_similarity):
        # print("""user_query: {}
        #     probable_question: {}
        #     attempted_response: {}
        #     semantic_similarity{}""".
        #     format(user_query, probable_question, attempted_response, semantic_similarity))

        statement = r"INSERT INTO UserLog" \
                     "(username, query,probable_question, attempted_response, semantic_similarity, t_stamp)" \
                     "VALUES ('{}','{}','{}','{}','{}',CURRENT_TIMESTAMP)".format(self.username, user_query, probable_question,
                                                                   attempted_response, semantic_similarity)
        # print(statement)
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

