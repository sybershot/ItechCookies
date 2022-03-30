from pymysql import connect, cursors

from itechframework.configuration.constants import MYSQL_SERVER_HOST, MYSQL_PORT, DB_NAME


class SQLMaster:

    def __init__(self, login, password):
        self.login = login
        self.password = password
        self.connection = self.connect_db()

    def connect_db(self):
        return connect(host=MYSQL_SERVER_HOST,
                       port=MYSQL_PORT,
                       user=self.login,
                       password=self.password,
                       database=DB_NAME,
                       charset='utf8mb4',
                       cursorclass=cursors.DictCursor)

    def fetch_all(self, table_name):
        query = "SELECT * FROM " + table_name
        cursor = self.connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        from_table = {table_name: result}
        return from_table

    def get_table_list(self):
        cursor = self.connection.cursor()
        cursor.execute("Show tables;")
        result = cursor.fetchall()
        db_tables = 'Tables_in_' + DB_NAME
        result = [v[db_tables] for v in result]
        return result
