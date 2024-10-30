import pandas as pd
from scripts.Utils.PSQLutils import PSQL
from scripts.Utils.MapUtils.FoliumUtils import ToFoliumMap

from scripts.Utils.PSQLutils.config import ServerConf, TableATM

sql = PSQL(ServerConf, TableATM)
sql.connect()
lol = sql.fetch_all_rows("in_mkad=TRUE")
sql.close()
ATM_df = pd.DataFrame(lol, columns=['osmid', 'lon', 'lat', 'operator', 'in_MKAD'])
print(sql.last_query)
print(ATM_df)

output_file = "output_htmls/atms_on_map.html"
To_map = ToFoliumMap()
To_map.generate_map(ATM_df)
To_map.save_map(output_file)