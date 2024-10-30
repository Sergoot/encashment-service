import pandas as pd
from scripts.Utils.PSQLutils import PSQL
from scripts.Utils.MapUtils.FoliumUtils import ToFoliumMap

from scripts.Utils.PSQLutils.config import ServerConf, TableATM

sql = PSQL(ServerConf, TableATM)
lol = sql.fetch_all_rows("in_mkad=TRUE")
sql.close()
ATM_df = pd.DataFrame(lol, columns=TableATM.table_columns)

output_file = "output_htmls/atms_on_map.html"
To_map = ToFoliumMap()
To_map.generate_map(ATM_df,lat_key='x_lon',lon_key='y_lat')
To_map.save_map(output_file)