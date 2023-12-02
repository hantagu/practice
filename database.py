from psycopg import connect

class DBHelper:

    def __init__(self, host: str, port: int, user: str, password: str, dbname: str) -> None:
        self.__connection = connect(f'host={host} port={port} user={user} password={password} dbname={dbname}', autocommit=True)

        with self.__connection.cursor() as cur:
            cur.execute('DO $$ BEGIN CREATE TYPE "user_role" AS ENUM (\'student\', \'teacher\', \'curator\', \'admin\'); EXCEPTION WHEN duplicate_object THEN NULL; END $$;')
            cur.execute('DO $$ BEGIN CREATE TYPE "scoring_system" AS ENUM (\'abstract\', \'points\'); EXCEPTION WHEN duplicate_object THEN NULL; END $$;')
