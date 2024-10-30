import pandas as pd
from numpy.random.mtrand import operator

from scripts.Utils.PSQLutils import PSQL
from scripts.Utils.MapUtils.OSMUtils import OSMatms

from scripts.Utils.PSQLutils.config import ServerConf, TableATM

sql = PSQL(ServerConf, TableATM)
#nearest_nodes = PSQL(dbname = 'neare
# st_nodes')
os = OSMatms()

atms = os.get_city()
atms = pd.DataFrame(atms)
atms = atms.fillna('Неизвестно')
for index, atm in atms.iterrows():
    sql.insert_row(osmid=atm['osmid'],
                   x_lon=atm['lon'],
                   y_lat=atm['lat'],
                   operator=atm['operator'],
                   in_mkad= atm['in_MKAD'],
                   on_conflict_ignore=True
                   )
sql.close()





