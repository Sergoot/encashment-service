"""
скрипт по выгрузке АМТов и ближайших нод(nearest node - NN) в БД
"""
from time import time
import pandas as pd
from scripts.Utils.PSQLutils import PSQL
from scripts.Utils.MapUtils.OSMUtils import OSMatms
from scripts.Utils.PSQLutils.config import ServerConf, TableATM, TableNearest

ATMS_sql = PSQL(ServerConf, TableATM)
atms_in_db = ATMS_sql.fetch_rows()
atms_in_db = pd.DataFrame(atms_in_db, columns=TableATM.table_columns)
atms_in_db = atms_in_db['osmid']

osm = OSMatms()

atms_all = osm.get_city()
atms_all = pd.DataFrame(atms_all)
atms_all = atms_all.fillna('Неизвестно')
atms_to_calculate = atms_all[~atms_all['osmid'].isin(atms_in_db)]

print('РАБОТЫ С АТМАМИ')
print('всего:', len(atms_all))
print('в БД:', len(atms_in_db))
print('к вычислению:', len(atms_to_calculate))


for index, row in atms_to_calculate.iterrows():
    ATMS_sql.insert_row(
        osmid=row['osmid'],
        x_lon=row['lon'],
        y_lat=row['lat'],
        operator=row['operator'],
        in_mkad= row['in_mkad'],
        )
ATMS_sql.close()


NNS_sql = PSQL(ServerConf, TableNearest)
nns_in_db = NNS_sql.fetch_rows()
nns_in_db = pd.DataFrame(nns_in_db, columns=TableNearest.table_columns)
nns_in_db = nns_in_db['atm_osmid']
nns_to_calculate =  atms_all[~atms_all['osmid'].isin(nns_in_db)]


print('РАБОТЫ С ОБОЧИНАМИ')
print('всего АТМов:', len(atms_all))
print('в БД:', len(nns_in_db))
print('к вычислению:', len(nns_to_calculate))

start_init = time()
print('Инициализация графа')
osm.init_place_graph()
print('Инициализация завершена, длилась:', time() - start_init)

for index, row in nns_to_calculate.iterrows():
    nn = osm.nearest_node(row['lon'], row['lat'])
    NNS_sql.insert_row(
        osmid=nn['osmid'],
        atm_osmid=row['osmid'],
        x_lon=nn['lon'],
        y_lat=nn['lat'],
        distance_to_atm=nn['distance_to_atm'],
        in_mkad=nn['in_mkad']
    )

    print(index, '/', len(nns_to_calculate))

NNS_sql.close()




