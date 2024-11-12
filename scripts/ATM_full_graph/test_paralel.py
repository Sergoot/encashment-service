from time import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from scripts.Utils.PSQLutils.main import PSQL
from scripts.Utils.PSQLutils.config import TableNearest, ServerConf, TableATM, TableRoutesTest
from scripts.Utils.PSQLutils.config import TableRoutesTest as TableRoutes
import pandas as pd
from scripts.Utils.MapUtils.OSMUtils import OSMatms

atm_sql = PSQL(ServerConf, TableATM)
nn_sql = PSQL(ServerConf, TableNearest)
routes_sql = PSQL(ServerConf, TableRoutesTest)

# Загрузка данных из базы данных
atms = pd.DataFrame(atm_sql.fetch_all_rows(), columns=['atm_osmid' , 'atm_lon', 'atm_lat' , 'operator', 'atm_in_mkad'])
nn = pd.DataFrame(nn_sql.fetch_all_rows(), columns=['nn_osmid', 'atm_osmid' , 'nn_lon', 'nn_lat' , 'distance', 'nn_in_mkad'])

# Объединение и фильтрация данных
Merged_ATM_NN = pd.merge(atms, nn, on='atm_osmid')
Merged_ATM_NN = Merged_ATM_NN.sort_values(by='distance')
Merged_ATM_NN = Merged_ATM_NN[(Merged_ATM_NN['atm_in_mkad'] == True) & (Merged_ATM_NN['nn_in_mkad'] == True)]

# Определение маршрутов, которые нужно рассчитать
nn_all = set(Merged_ATM_NN['nn_osmid'])
routes_in_db = set(pd.DataFrame(routes_sql.fetch_all_rows(), columns=TableRoutesTest.table_columns)['direction'])
routes_all = {f'{src}->{dst}' for src in nn_all for dst in nn_all if src != dst}
routes_to_calculate = routes_all - routes_in_db

# Инициализация графа
ox = OSMatms()
ox.init_place_graph()

# Функция для расчета маршрута
def calculate_route(direction):
    src, dst = map(int, direction.split('->'))
    try:
        nodes = ox.get_shortest_route(src, dst)
        travel_time = ox.get_travel_time(nodes)
        distance = ox.get_total_distance(nodes)
        routes_sql.insert_row(
            direction=direction,
            src=src,
            dst=dst,
            nodes=nodes,
            time=travel_time,
            distance=distance
        )
        return True  # Успешно
    except Exception as e:
        print(f"Ошибка при расчете маршрута {direction}: {e}")
        return False  # Ошибка

# Параллельный запуск вычислений
start_total_time = time()
count_done, count_error = 0, 0
with ProcessPoolExecutor(max_workers=4) as executor:
    futures = {executor.submit(calculate_route, direction): direction for direction in routes_to_calculate}
    for future in as_completed(futures):
        result = future.result()
        if result:
            count_done += 1
        else:
            count_error += 1
        print(f'Рассчитано: {count_done}/{len(routes_to_calculate)}, Ошибок: {count_error}')

print(f'Время выполнения: {time() - start_total_time}')