from numpy.random.mtrand import operator

from scripts.Utils.PSQLutils.main import PSQL
from scripts.Utils.PSQLutils.config import TableATM,TableNearest, ServerConf, TableATMAllowedNew
import pandas as pd


atms_sql = PSQL(ServerConf, TableATM)
nn_sql = PSQL(ServerConf, TableNearest)

atms_nn_sql = PSQL(ServerConf, TableATMAllowedNew)

atms = atms_sql.fetch_rows()
nn = nn_sql.fetch_rows()
atms = pd.DataFrame(atms, columns=['atm_osmid' , 'atm_lon', 'atm_lat' , 'operator', 'atm_in_mkad'])
nn = pd.DataFrame(nn, columns=['nn_osmid', 'atm_osmid' , 'nn_lon', 'nn_lat' , 'distance', 'nn_in_mkad'])

Merged_ATM_NN = pd.merge(atms, nn, on='atm_osmid')

Merged_ATM_NN = Merged_ATM_NN.sort_values(by='distance')
Merged_ATM_NN = Merged_ATM_NN[(Merged_ATM_NN['atm_in_mkad'] == True) & (Merged_ATM_NN['nn_in_mkad'] == True)]
Merged_ATM_NN = Merged_ATM_NN.head(1000)


for index, row in Merged_ATM_NN.iterrows():
    atms_nn_sql.insert_row(
        atm_osmid = row['atm_osmid'],
        atm_x_lon = row['atm_lon'],
        atm_y_lat = row['atm_lat'],
        operator = row['operator'],
        atm_in_mkad = row['atm_in_mkad'],
        nn_osmid = row['nn_osmid'],
        nn_x_lon = row['nn_lon'],
        nn_x_lat = row['nn_lat'],
        nn_in_mkad = row['nn_in_mkad'],
        atm_nn_distance = row['distance']


    )

atms_nn_sql.close()