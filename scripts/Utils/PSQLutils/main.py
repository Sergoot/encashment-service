from .config import DB, TableATM
import psycopg2

class PSQL:
    def __init__(self):
        self.conn = psycopg2.connect(user=DB.user, password=DB.password, host=DB.host, dbname=DB.dbname)
        with self.conn.cursor() as cur:
            sql_request = f"CREATE TABLE IF NOT EXISTS {TableATM.table_name} (osmid BIGSERIAL PRIMARY KEY, x_lon float8, y_lat float8, operator text, in_MKAD boolean);"
            cur.execute(sql_request)
        self.conn.commit()
    def write_atm_to_db(self, osmid, x_lon, y_lat, operator, in_MKAD):
        with self.conn.cursor() as cur:
            sql_request = f"""
                    INSERT INTO {TableATM.table_name} (osmid, x_lon, y_lat, operator, in_MKAD) 
                    VALUES ({osmid}, {x_lon}, {y_lat}, '{operator}', {in_MKAD})
                    ON CONFLICT (osmid) DO NOTHING;
                """
            cur.execute(sql_request)
            self.conn.commit()
    #Я ЗНАЮ ЧТО ЭТО ОЧКО БЕЗОПАСНОСТИ
    #к этому скрипту пользователь не допущен
    #я художник я так вижу
    def get_atms_from_db(self, in_MKAD = None):
        qurery = f"SELECT * FROM {TableATM.table_name}"

        if in_MKAD is not None:
            qurery += f' WHERE in_MKAD = {in_MKAD}'

        with self.conn.cursor() as cur:
            cur.execute(qurery)
            self.conn.commit()
            return cur.fetchall()
    def close(self):
        self.conn.close()

