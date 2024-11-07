import random
class ServerConf:
    host = 'localhost'
    #host = '192.168.0.3'
    port = 5432
    user = 'postgres'
    password = 'very_strong_password'
    dbname = 'TRPO_project' #НЕ ЗАБУДЬ СОЗДАТЬ ОДНОИМЕННУЮ БД, иначе будет выдавать дибильные ошибки из разряда "utf-8"



#БАЗА для создания Table{имя}
#table_name - имя таблицы
#table_columns - имена столбцов (массивом)
#table_definition - определение типов столбцов (в скл формате)
class TableATM:
    table_name = 'atms'
    table_columns = ['osmid', 'x_lon', 'y_lat', 'operator', 'in_mkad']
    table_definition = """  osmid BIGSERIAL PRIMARY KEY, 
                            x_lon float8, 
                            y_lat float8, 
                            operator text, 
                            in_mkad boolean
                            """


class TableNearest:
    table_name = 'nearest_nodes'
    table_columns = ['osmid', 'atm_osmid', 'x_lon', 'y_lat', 'distance_to_atm', 'in_mkad']
    table_definition = """  osmid BIGSERIAL, 
                            atm_osmid BIGSERIAL PRIMARY KEY,
                            x_lon float8, 
                            y_lat float8, 
                            distance_to_atm serial,
                            in_mkad boolean,
                            FOREIGN KEY (atm_osmid) REFERENCES atms(osmid)"""


class TableRoutes:
    table_name = 'routes'
    table_columns = ['direction', 'src', 'dst', 'nodes', 'time', 'distance']
    table_definition = """  direction TEXT PRIMARY KEY, 
                            src BIGSERIAL,
                            dst BIGSERIAL, 
                            nodes BIGINT[],
                            time SERIAL,
                            distance serial"""
                            #с bigint это шутка какая то

class TableRoutes2:
    table_name = 'routes_2.0'
    table_columns = ['key_column ', 'src', 'dst', 'nodes', 'time', 'distance']
    table_definition = """  key_column SERIAL PRIMARY KEY, 
                            src BIGSERIAL,
                            dst BIGSERIAL, 
                            nodes BIGINT[],
                            time SERIAL,
                            distance SERIAL,
                            FOREIGN KEY (src) REFERENCES nearest_nodes(osmid),
                            FOREIGN KEY (dst) REFERENCES nearest_nodes(osmid)"""
                            #с bigint это шутка какая то

class TableAvailableATMs:
    table_name = 'allowed_atms'
    table_columns = ['osmid']
    table_definition = """  osmid BIGSERIAL PRIMARY KEY, 
                            FOREIGN KEY (osmid) REFERENCES atms(osmid)"""

class TableRoutesTest:
    table_name = 'routes_test'
    table_columns = ['direction', 'src', 'dst', 'nodes', 'time', 'distance']
    table_definition = """  direction TEXT PRIMARY KEY, 
                            src BIGSERIAL,
                            dst BIGSERIAL, 
                            nodes BIGINT[],
                            time SERIAL,
                            distance serial"""

class TestTable:
    #table_name = f'test_table{random.randint(0,100000)}'
    table_name = 'test_table73565'
    #table_columns = '(osmid BIGSERIAL PRIMARY KEY, x_lon float8, y_lat float8, operator text, in_MKAD boolean);'
    table_columns = ['direction', 'src', 'dst', 'nodes', 'time', 'distance']
    table_definition = """  direction TEXT PRIMARY KEY, 
                            src BIGSERIAL,
                            dst BIGSERIAL, 
                            nodes BIGINT[],
                            time SERIAL,
                            distance serial"""

class TestTable2:
    #table_name = f'test_table{random.randint(0,100000)}'
    table_name = 'test_table73565'
    #table_columns = '(osmid BIGSERIAL PRIMARY KEY, x_lon float8, y_lat float8, operator text, in_MKAD boolean);'
    table_columns = ['osmid', 'x_lon', 'y_lat', 'operator', 'in_mkad']
    table_definition = """  osmid BIGSERIAL PRIMARY KEY, 
                                x_lon float8, 
                                y_lat float8, 
                                operator text, 
                                in_mkad boolean
                                """