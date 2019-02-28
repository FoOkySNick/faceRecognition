import pypyodbc


class Connection:
    @staticmethod
    def connect(database, driver="DRIVER={SQL Server}", server="SERVER=localhost",
                user="", password="", port="PORT=1433"):
        conn_str = ';'.join([driver, server, port, database, user, password])
        conn = pypyodbc.connect(conn_str)
        cursor = conn.cursor()
        return conn, cursor


if __name__ == "__main__":
    Connection.connect("WorkAttendance")
else:
    print("Вы используете database_connection как библиотеку")