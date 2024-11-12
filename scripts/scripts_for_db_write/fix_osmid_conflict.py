from scripts.Utils.PSQLutils.main import PSQL
from scripts.Utils.PSQLutils.config import ServerConf,TableAllowedNNs, TableRoutes2
import pandas as pd

csv = pd.read_csv('~/Документы/routes.csv', names=TableRoutes2.table_columns)

nn_sql = PSQL(ServerConf, TableAllowedNNs)
nn = nn_sql.fetch_rows()
nn = pd.DataFrame(nn, columns = ['osmid'])
nn = nn['osmid']
nn = set(nn)
print(len(nn))

csv_src = set(csv['src'])
csv_dst = set(csv['dst'])

print(csv_src - nn)
print(nn - csv_src)
#4936258703

print(len(set(csv_dst)) * (len(set(csv_src))-1))
