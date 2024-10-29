import pandas as pd
from scripts.Utils.PSQLutils import PSQL
from scripts.Utils.MapUtils import OSMatms


sql = PSQL()
os = OSMatms()

atms = os.get_city()
atms = pd.DataFrame(atms)
atms = atms.fillna('Неизвестно')
for index, atm in atms.iterrows():
    osmid = atm['osmid']
    lon = atm['lon']
    lat = atm['lat']
    operator = atm['operator']
    in_MKAD = atm['in_MKAD']
    sql.write_atm_to_db(osmid, lon, lat, operator, in_MKAD)
sql.close()




