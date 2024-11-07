"""
класс отвечающий ра работу с постгрей
"""

import psycopg2
from psycopg2 import sql

from scripts.Utils.PSQLutils.config import TestTable
from typing import List, Tuple, Any, Dict, Optional


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
                if self.debug:
                    print('таблица откатана')
            raise e

    #я ебал тут фильтрацию реализовывать
    #пока что только по in_mkad, но далее
    #скорее всего придется еще и по удаленности делать
    #типо больше меньше указанного расстояния
    #и я хз как уже такое реализовывать
    def fetch_rows(self, filter_sql:str=None, _count:int=None) -> List[Tuple[Any, ...]]:
        query = sql.SQL("SELECT * FROM {table}").format(table=sql.Identifier(self.table_name))
        if filter_sql:

            query += sql.SQL(' WHERE ' + filter_sql)
        if _count:
            query += sql.SQL(' LIMIT {count} ').format(
                count=sql.Literal(_count)
            )
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
    psql = PSQL(ServerConf, TableATM)
    try:
        psql.debug = True
        psql.connect()
        psql.insert_row(osmid=1235 ,x_lon=3,y_lat=4,operator='ahah',in_MKAD=True, on_conflict_ignore=True)
        #psql.insert_row(osmid=123 ,x_lon=3,y_lat=4,operator='ahah',in_MKAD=True, on_conflict_ignore=True)
        #['direction', 'src', 'dst', 'nodes', 'time', 'distance']
        #print(psql.fetch_all_rows('osmid=123'))
        # print(psql.fetch_all_rows('osmid=1235'))
        #psql.insert_row(direction='123->321>',
        #                src='123',dst='321',
        #                nodes=[1,2,3,4,5],
        #                time=228,
        #                distance=1337,
        #                on_conflict_ignore=True)
        #psql.insert_row(direction='1263->321>',
        #                src='123', dst='321',
        #                nodes=[1, 2, 3, 4, 5],
        #                time=228,
        #                distance=1337,
        #                on_conflict_ignore=True)
        #psql.insert_row(direction='1243->321>',
        #                src='123', dst='321',
        #                nodes=[1, 2, 3, 4, 5],
        #                time=228,
        #                distance=1337,
        #                on_conflict_ignore=True)

        #print(psql.fetch_all_rows('osmid=123'))
        print(psql.fetch_rows(_count=1))
        print(psql.fetch_rows())
        psql._drop_table()
    except Exception as e:
        psql._drop_table()
        raise e


if __name__ == '__main__':
    test_PSQL()
