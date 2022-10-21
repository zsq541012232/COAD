import os
import pandas as pd


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
    return time_value_dict

def get_ts_from_a_file(instance_kpi_tuple: tuple, path: str):
    time_value_dict = dict()
    instance_name = instance_kpi_tuple[0]
    kpi_name = instance_kpi_tuple[1]
    f = pd.read_csv(path)
    for index, value in f.iterrows():
        if value[1] == instance_name and value[2] == kpi_name:
            time_value_dict[value[0]] = value[3]
    return time_value_dict






