import pandas as pd
from numpy.random.mtrand import operator

from scripts.Utils.PSQLutils import PSQL
from scripts.Utils.MapUtils.OSMUtils import OSMatms

from scripts.Utils.PSQLutils.config import ServerConf, TableATM, TableNearest

ATMS_sql = PSQL(ServerConf, TableATM)
Nearest_sql = PSQL(ServerConf, TableNearest)
osm = OSMatms()
osm.init_place_graph()

atms = osm.get_city()
atms = pd.DataFrame(atms)
atms = atms.fillna('Неизвестно')
for index, atm in atms.iterrows():
    ATMS_sql.insert_row(
        osmid=atm['osmid'],
        x_lon=atm['lon'],
        y_lat=atm['lat'],
        operator=atm['operator'],
        in_mkad= atm['in_mkad'],
        on_conflict_ignore=True
        )

    nn = osm.nearest_node(atm['lon'], atm['lat'])
    #print(atm['osmid'])
    Nearest_sql.insert_row(
        osmid = nn['osmid'],
        atm_osmid = atm['osmid'],
        x_lon=nn['lon'],
        y_lat=nn['lat'],
        distance_to_atm=nn['distance_to_atm'],
        in_mkad=nn['in_mkad']

    )
ATMS_sql.close()
Nearest_sql.close()




