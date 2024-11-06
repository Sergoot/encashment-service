"""
скрипт по выгрузке данныз их БД в CSV таблицу
таблицы АТМов и НН объединятся
"""

from scripts.Utils.PSQLutils.main import PSQL
from scripts.Utils.PSQLutils.config import TableATM,TableNearest, ServerConf
import pandas as pd


atms_sql = PSQL(ServerConf, TableATM)
nn_sql = PSQL(ServerConf, TableNearest)

atms = atms_sql.fetch_rows()
nn = nn_sql.fetch_rows()
atms = pd.DataFrame(atms, columns=['atm_osmid' , 'atm_lon', 'atm_lat' , 'operator', 'atm_in_mkad'])
nn = pd.DataFrame(nn, columns=['nn_osmid', 'atm_osmid' , 'nn_lon', 'nn_lat' , 'distance', 'nn_in_mkad'])

merged = pd.merge(atms, nn, on='atm_osmid')
merged.to_csv('output_csv/merged_atms+nn.csv')