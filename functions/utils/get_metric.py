import os
import pandas as pd


# 这个函数可以将指定的（instance，kpi）的时间序列，从指定的path中读取成ts_dict
# ts_dict中的index是时间，value是值
def get_h_metric(instance_kpi_tuple: tuple, path: str):
    time_value_dict = dict()
    instance_name = instance_kpi_tuple[0]
    kpi_name = instance_kpi_tuple[1]
    for root, dirs, files in os.walk(path):
        for name in files:
            if name.find(kpi_name) != -1:
                f = pd.read_csv(os.path.join(root, name))
                for index, value in f.iterrows():
                    if value[1] == instance_name:
                        time_value_dict[value[0]] = value[3]
    return time_value_dict  # 如果是空表示没有找到

# 更加精细地查找，防止在文件中文件名不包含kpi_name的情况
def get_ts_from_a_file(instance_kpi_tuple: tuple, path: str):
    time_value_dict = dict()
    instance_name = instance_kpi_tuple[0]
    kpi_name = instance_kpi_tuple[1]
    f = pd.read_csv(path)
    for index, value in f.iterrows():
        if value[1] == instance_name and value[2] == kpi_name:
            time_value_dict[value[0]] = value[3]
    return time_value_dict  # 如果是空表示没有找到






