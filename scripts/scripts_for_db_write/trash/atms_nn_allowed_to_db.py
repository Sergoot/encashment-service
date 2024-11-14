"""
скрипт по выгрузке допустимых АТМов
как формируется
берутся все АТМы которые в МКАДе, а также те АТМы ближайшие обочины которые тоже в МКАДе
затем из них берется первая тысяча
"""

import pandas as pd
from scripts.Utils.PSQLutils.main import PSQL
from scripts.Utils.PSQLutils.config import ServerConf,TableAllowedATMs,TableATM,TableNearest,TableAllowedNNs

atm_sql = PSQL(ServerConf, TableATM)
nn_sql = PSQL(ServerConf, TableNearest)
atm_allowed_sql = PSQL(ServerConf, TableAllowedATMs)
nn_allowed_sql = PSQL(ServerConf, TableAllowedNNs)

atms = atm_sql.fetch_rows()
nn = nn_sql.fetch_rows()
atms = pd.DataFrame(atms, columns=['atm_osmid' , 'atm_lon', 'atm_lat' , 'operator', 'atm_in_mkad'])
nn = pd.DataFrame(nn, columns=['nn_osmid', 'atm_osmid' , 'nn_lon', 'nn_lat' , 'distance', 'nn_in_mkad'])

Merged_ATM_NN = pd.merge(atms, nn, on='atm_osmid')

Merged_ATM_NN = Merged_ATM_NN.sort_values(by='distance')
Merged_ATM_NN = Merged_ATM_NN[(Merged_ATM_NN['atm_in_mkad'] == True) & (Merged_ATM_NN['nn_in_mkad'] == True)]
Merged_ATM_NN = Merged_ATM_NN.head(1000)

print(len(Merged_ATM_NN))

count = 0

for index,row in Merged_ATM_NN.iterrows():
    #print(index)
    atm_allowed_sql.insert_row(
        osmid = row['atm_osmid'],
        on_conflict_ignore = True
    )
    nn_allowed_sql.insert_row(
        osmid = row['nn_osmid'],
        on_conflict_ignore=True
    )
    count += 1

print(count)

atm_sql.close()
nn_sql.close()
atm_allowed_sql.close()

