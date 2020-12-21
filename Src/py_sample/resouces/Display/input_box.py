# バルクイン用
import csv
from datetime import *
import os
import sys
from pathlib import Path

root = os.path.dirname(__file__)
sys.path.append(root + "/CSV")

future_list=['a','b']
a_name = 'area_'+ datetime.now().strftime('%Y%m%d%H%M%S') + '.csv'
s_name = 'spot_'+ datetime.now().strftime("%Y%m%d%H%M%S") + '.csv'
a_path = Path(root + '/CSV/create_areas/' + a_name)
s_path = Path(root + '/CSV/create_spots/' + s_name)
#a_path = Path('.CSV/create_areas/' + a_name)
#s_path = Path('.CSV/create_spots/' + s_name)
print(a_path)
print(s_path)
a_file = open(a_path, 'w')
s_file = open(s_path, 'w')
a_writer = csv.writer(a_file)
s_writer = csv.writer(s_file)
a_writer.writerow(future_list)
s_writer.writerow(future_list)

print('end')