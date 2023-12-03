from psycopg import Cursor, connect

class DBHelper:

    @staticmethod
    def execute(cur: Cursor, path: str):
        cur.execute(open(path, 'rt').read()) # type: ignore

    def __init__(self, host: str, port: int, user: str, password: str, dbname: str, drop: bool = False) -> None:

        self.__connection = connect(f'host={host} port={port} user={user} password={password} dbname={dbname}', autocommit=True)

        with self.__connection.cursor() as cur:

            if drop:
                DBHelper.execute(cur, 'sql/init/drop_tables.sql')
                DBHelper.execute(cur, 'sql/init/drop_types.sql')

            DBHelper.execute(cur, 'sql/init/create_types.sql')
            DBHelper.execute(cur, 'sql/init/create_tables.sql')


    def get_all_users(self) -> list:
        with self.__connection.cursor() as cur:
            DBHelper.execute(cur, 'sql/get_all_users.sql')
            return cur.fetchall()
