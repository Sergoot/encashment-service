"""
простой скрипт по отрисовке всех данных точек МКАДа
из которых потом строится граница для АТМок
"""
import pandas as pd
from scripts.Utils.MapUtils.mkad_coords import MKAD_1
from scripts.Utils.MapUtils.FoliumUtils import ToFoliumMap

MKAD_df = pd.DataFrame(MKAD_1, columns=['lon', 'lat'])

output_file = "output_htmls/mkad_dots_on_map.html"

To_map = ToFoliumMap()
To_map.generate_atm_map(MKAD_df)
To_map.save_map(output_file)