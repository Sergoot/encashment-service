"""
класс отвечающий ра работу с постгрей
"""

import psycopg2
from psycopg2 import sql
from scripts.Utils.PSQLutils.config import TestTable
from typing import List, Tuple, Any, Dict, Optional

"""
class PSQL:
    def __init__(self, DB_dc, Table_dc):
        self.user = DB_dc.user #dc - data class
        self.password = DB_dc.password
        self.host = DB_dc.host
        self.dbname = DB_dc.dbname
        self.table_name = Table_dc.table_name
        self.table_columns = Table_dc.table_columns
        self.conn = psycopg2.connect(user=self.user,
                                    password=self.password,
                                    host=self.host,
                                    dbname=self.dbname,
                                    )
        query = f"CREATE TABLE IF NOT EXISTS {self.table_name} {self.table_columns}"
        self._execute_sql(query)

    def _execute_sql(self, sql_query:str, values = None, output:bool=False):
        with self.conn.cursor() as cur:
            cur.execute(sql_query, values)
            if output:
                return cur.fetchall()
            else:
                self.conn.commit()

    def write_row(self, conflict_column=None, **kwargs):
        names = map(str, kwargs.keys())
        values = map(str, kwargs.values())
        #formatted_values = tuple(self._format_value(value) for value in values)
        query = f
                INSERT INTO {self.table_name} ({','.join(names)}) 
                VALUES ({','.join(values)})
                

        query = sql.SQL("INSERT INTO {table} ({fields}) VALUES ({placeholders})").format(
            table=sql.Identifier(self.table_name),
            fields=sql.SQL(', ').join(map(sql.Identifier, names)),
            placeholders=sql.SQL(', ').join(sql.Placeholder() * len(kwargs))
        )
        print(query)

        #if conflict_column is not None:
            #query = f' ON CONFLICT ({conflict_column}) DO NOTHING;'
        self._execute_sql(query, values)

    #Я ЗНАЮ ЧТО ЭТО ОЧКО БЕЗОПАСНОСТИ
    #к этому скрипту пользователь не допущен
    #я художник я так вижу
    def get_atms_from_db(self, in_mkad:bool = None):
        query = f"SELECT * FROM {TableATM.table_name}"

        if in_mkad is not None:
            query += f' WHERE in_MKAD = {in_mkad}'
        return self._execute_sql(query, output=True)

    def close(self):
        self.conn.close()

 #'(osmid BIGSERIAL PRIMARY KEY, x_lon float8, y_lat float8, operator text, in_MKAD boolean);'
"""

class PSQL:
    def __init__(self, DB_dc, Table_dc, auto_connect:bool=True,auto_create_table:bool=True):
        self.user = DB_dc.user  # dc - data class
        self.password = DB_dc.password
        self.host = DB_dc.host
        self.dbname = DB_dc.dbname
        self.table_name = Table_dc.table_name
        self.table_columns = Table_dc.table_columns
        self.table_definition = Table_dc.table_definition
        self.connection = None
        self.debug = False
        self.last_query = None
        if auto_connect:
            self.connect()
        if auto_create_table:
            self.create_table()

    def connect(self):
        if not self.connection:
            self.connection = psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
            )
            if self.debug:
                print('сервер подключен')
        else:
            if self.debug:
                print('сервер УЖЕ был подключен')


    def create_table(self):
        query = sql.SQL("CREATE TABLE IF NOT EXISTS {table} ({definition})").format(
                table=sql.Identifier(self.table_name),
                definition=sql.SQL(self.table_definition)
            )
        self.__execute_query(query)

        if self.debug:
            print('таблица создалась')

    def close(self):
        if self.connection:
            self.connection.close()

    def __execute_query(self, query, values=None, output=False):
        self.last_query = query
        if self.debug:
            print(query.as_string(self.connection))
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, values)
                self.connection.commit()
                if output:
                    return cursor.fetchall()
        except Exception as e:
            if self.connection:
                self.connection.rollback()
                self.close()
                if debug:
                    print('таблица откатана')
            raise e

    #я ебал тут фильтрацию реализовывать
    #пока что только по in_mkad, но далее
    #скорее всего придется еще и по удаленности делать
    #типо больше меньше указанного расстояния
    #и я хз как уже такое реализовывать
    def fetch_all_rows(self, filter_sql:str=None) -> List[Tuple[Any, ...]]:
        query = sql.SQL("SELECT * FROM {table}").format(table=sql.Identifier(self.table_name))
        if filter_sql is not None:

            query += sql.SQL(' WHERE ' + filter_sql)
        #values = tuple(filter.values()) if filter else None
        return self.__execute_query(query, output=True)

    def insert_row(self, on_conflict_ignore:bool = False,
                   **values) -> None:
        values = list(values.values())
        query = sql.SQL("INSERT INTO {table} ({fields}) VALUES ({placeholders})").format(
            table=sql.Identifier(self.table_name),
            fields=sql.SQL(', ').join(map(sql.Identifier, self.table_columns)),
            placeholders=sql.SQL(', ').join(sql.Placeholder() * len(values))
        )

        if on_conflict_ignore:
            query += sql.SQL(" ON CONFLICT DO NOTHING")

        self.__execute_query(query, values)
    def _drop_table(self):
        query = sql.SQL("DROP TABLE {table}").format(
                table=sql.Identifier(self.table_name)
        )
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            self.connection.commit()
        print(f'таблица {self.table_name} дропнута')




def test_PSQL():
    from config import ServerConf, TableATM
    psql = PSQL(ServerConf, TestTable)
    try:
        psql.debug = True
        psql.connect()
        psql.insert_row(osmid=1235 ,x_lon=3,y_lat=4,operator='ahah',in_MKAD=True, on_conflict_ignore=True)
        psql.insert_row(osmid=123 ,x_lon=3,y_lat=4,operator='ahah',in_MKAD=True, on_conflict_ignore=True)

        print(psql.fetch_all_rows('osmid=123'))
        print(psql.fetch_all_rows('osmid=1235'))
        print(psql.fetch_all_rows())
        psql._drop_table()
    except Exception as e:
        psql._drop_table()
        raise e


if __name__ == '__main__':
    test_PSQL()
