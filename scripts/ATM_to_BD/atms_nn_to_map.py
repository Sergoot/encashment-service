"""
простой скрипт по генерации html карты с банкоматами и ближайшими к ним "обочинами"
"""
from scripts.Utils.PSQLutils.main import PSQL
from scripts.Utils.PSQLutils.config import TableATM,TableNearest, ServerConf
import pandas as pd
from scripts.Utils.MapUtils.FoliumUtils import ToFoliumMap

atms_sql = PSQL(ServerConf, TableATM)
nn_sql = PSQL(ServerConf, TableNearest)

atms = atms_sql.fetch_all_rows()
nn = nn_sql.fetch_all_rows()
atms = pd.DataFrame(atms, columns=['atm_osmid' , 'atm_lon', 'atm_lat' , 'operator', 'atm_in_mkad'])
nn = pd.DataFrame(nn, columns=['nn_osmid', 'atm_osmid' , 'nn_lon', 'nn_lat' , 'distance', 'nn_in_mkad'])

Merged_ATM_NN = pd.merge(atms, nn, on='atm_osmid')


output_file = "output_htmls/atms+nn_map.html"
To_map = ToFoliumMap()
To_map.generate_atm_nn_map(Merged_ATM_NN,
                           atm_lat_key='atm_lat',
                           atm_lon_key='atm_lon',
                           nn_lat_key='nn_lat',
                           nn_lon_key='nn_lon')
To_map.save_map(output_file)

