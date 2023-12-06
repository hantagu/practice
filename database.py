from uuid import UUID
from psycopg import Cursor, connect

class User:

    def __init__(self, id: UUID, login: str, password: str, role: str, name: str, balance: float, scoring_system: str | None) -> None:
        self.id = id
        self.login = login
        self.password = password
        self.role = role
        self.name = name
        self.balance = balance
        self.scoring_system = scoring_system


class Course:

    def __init__(self) -> None:
        pass


class Group:

    def __init__(self, id: UUID, course_id: UUID, curator_id: UUID, title: str) -> None:
        self.id = id
        self.course_id = course_id
        self.curator_id = curator_id
        self.title = title


class DBHelper:

    @staticmethod
    def execute(cur: Cursor, path: str, params: tuple = ()):
        cur.execute(open(path, 'rt').read(), params) # type: ignore

    def __init__(self, host: str, port: int, user: str, password: str, dbname: str, drop: bool = False) -> None:

        self.__connection = connect(f'host={host} port={port} user={user} password={password} dbname={dbname}', autocommit=True)

        with self.__connection.cursor() as cur:

            if drop:
                DBHelper.execute(cur, 'sql/init/drop_tables.sql')
                DBHelper.execute(cur, 'sql/init/drop_types.sql')

            DBHelper.execute(cur, 'sql/init/create_types.sql')
            DBHelper.execute(cur, 'sql/init/create_tables.sql')


    def check_user_exists(self, login: str) -> bool:
        with self.__connection.cursor() as cur:
            DBHelper.execute(cur, 'sql/check_user_exists.sql', (login, ))
            return True if cur.fetchone()[0] else False # type: ignore (select exists всегда что-то вернёт, поэтому можно безопасно взять перый столбец первой строчки)


    def get_user_by_id(self, id: UUID) -> User | None:
        with self.__connection.cursor() as cur:
            DBHelper.execute(cur, 'sql/get_user_by_id.sql', (id, ))
            return User(*r) if (r := cur.fetchone()) else None


    def get_user_by_login(self, login: str) -> User | None:
        with self.__connection.cursor() as cur:
            DBHelper.execute(cur, 'sql/get_user_by_login.sql', (login, ))
            return User(*r) if (r := cur.fetchone()) else None


    def get_all_users(self) -> list[User]:
        with self.__connection.cursor() as cur:
            DBHelper.execute(cur, 'sql/get_all_users.sql')
            r = []
            for row in cur.fetchall():
                r.append(User(*row))
            return r


    def get_all_groups(self) -> list[Group]:
        with self.__connection.cursor() as cur:
            DBHelper.execute(cur, 'sql/get_all_groups.sql')
            r = []
            for row in cur.fetchall():
                r.append(Group(*row))
            return r
