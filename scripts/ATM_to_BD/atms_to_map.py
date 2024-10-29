import pandas as pd
from scripts.Utils.PSQLutils import PSQL
from scripts.Utils.MapUtils.FoliumUtils import ToFoliumMap
sql = PSQL()
lol = sql.get_atms_from_db(in_MKAD = True)
ATM_df = pd.DataFrame(lol, columns=['osmid', 'lon', 'lat', 'operator', 'in_MKAD'])


output_file = "output_htmls/atms_on_map.html"
To_map = ToFoliumMap()
To_map.generate_map(ATM_df)
To_map.save_map(output_file)