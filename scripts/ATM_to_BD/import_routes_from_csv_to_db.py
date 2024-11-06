"""
скрипт для импорта базы данных роутов из csv в postgres
мне было лень разбираться как это делается адекватнее поэтому просто написал питон скрипт
"""

from scripts.Utils.PSQLutils.main import PSQL
from scripts.Utils.PSQLutils.config import ServerConf, TableRoutes
import pandas as pd

sql = PSQL(ServerConf, TableRoutes)

csv = pd.read_csv('~/Документы/routes.csv', names=TableRoutes.table_columns)
#['direction', 'src', 'dst', 'nodes', 'time', 'distance']
print(csv)

for index, row in csv.iterrows():
    sql.insert_row(
        direction=row['direction'],
        src=row['src'],
        dst=row['dst'],
        nodes=row['nodes'],
        time=row['time'],
        distance=row['distance']
    )
    print(f'{index}/{len(csv)}')