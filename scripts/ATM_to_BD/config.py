class DB:
    host = 'localhost'
    port = 5432
    user = 'postgres'
    password = 'very_strong_password'
    dbname = 'TRPO_project' #НЕ ЗАБУДЬ СОЗДАТЬ ОДНОИМЕННУЮ БД, иначе будет выдавать дибильные ошибки из разряда "utf-8"


class TableATM:
    table_name = 'ATMs'



"""
id      bigserial
x_lon   float8
y_lat   float8






"""