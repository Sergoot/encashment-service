"""
скрипт для импорта базы данных роутов из csv в postgres
мне было лень разбираться как это делается адекватнее поэтому просто написал питон скрипт
"""

from scripts.Utils.PSQLutils.main import PSQL
from scripts.Utils.PSQLutils.config import ServerConf, TableRoutes2, TableRoutes, TableAllowedNNs
import pandas as pd

sql = PSQL(ServerConf, TableRoutes2)

csv = pd.read_csv('~/Документы/routes.csv', names=['destination'] + TableRoutes2.table_columns)


conflict_nn = set()
nn_sql = PSQL(ServerConf, TableAllowedNNs)
nn = nn_sql.fetch_rows()
nn_sql.close()
nn = pd.DataFrame(nn, columns = ['osmid'])
nn = set(nn['osmid'])

csv_src = set(csv['src'])
conflict_nn |= (nn - csv_src)
conflict_nn |= (csv_src - nn)
print(conflict_nn)

error_src = set()
error_dst = set()
error_count = 0
count = 0
for index, row in csv.iterrows():
    if row['src'] in conflict_nn or row['dst'] in conflict_nn:
        continue
    sql.insert_row(
        #direction=f'{row['src']}->{row['dst']}',
        src=row['src'],
        dst=row['dst'],
        nodes=row['nodes'],
        time=row['time'],
        distance=row['distance'],
        on_conflict_ignore=True
    )


    print(f'{index}/{len(csv)}')

print()
print(error_src)
print(error_dst)
print(error_count)