import os
import pandas as pd
import json


# 这个函数会统计文件夹下所有相关的cmbd_id以及kpi_name,并将他们组合为元组，之后放入字典内
# key为(instance,kpi),value为编号,编号为这个函数自动生成
# 这个字典作为全局信息，供后面时间序列分析使用
# 同时，这个函数也会生成instance和kpi的自己的编号,也是作为字典的形式
def generate_instance_cmdbid_tuple_dict():
    instance_names = set()
    kpi_names = set()
    instance_names_no = dict()
    kpi_names_no = dict()
    instance_kpi_tuple_no = dict()
    for root, dirs, files in os.walk("../data_raw"):
        for name in files:
            if name.startswith('kpi_'):
                f = pd.read_csv(os.path.join(root, name))
                for index, value in f.iterrows():
                    instance_names.add(value[1])  # value[1]是cmdb_id
                    kpi_names.add(value[2])  # value[2]是kpi_name
    # 进行编号
    for index, item in enumerate(instance_names):
        instance_names_no[index] = item
    for index, item in enumerate(kpi_names):
        kpi_names_no[index] = item
    index_new = 0
    for index_1, item_1 in enumerate(instance_names):
        for index_2, item_2 in enumerate(kpi_names):
            instance_kpi_tuple_no[index_new] = (item_1, item_2)
            index_new += 1
    with open("../data_processed/instance_names_dict.json", 'w') as fout:
        json.dump(instance_names_no, fout)
    with open('../data_processed/kpi_names_dict.json', 'w') as fout:
        json.dump(kpi_names_no, fout)
    with open('../data_processed/instance_kpi_tuple.json', 'w') as fout:
        json.dump(instance_kpi_tuple_no, fout)


def find_instance_index(instance_name):
    with open('../data_processed/instance_names_dict.json', 'r') as fin:
        f = json.load(fin)
    for index, value in f.items():
        if value == instance_name:
            return index


def find_kpi_index(kpi_name):
    with open('../data_processed/kpi_names_dict.json', 'r') as fin:
        f = json.load(fin)
    for index, value in f.items():
        if value == kpi_name:
            return index


def turn_tuple_string_to_tuple_number():
    with open('../data_processed/instance_kpi_tuple.json', 'r') as fin:
        f = json.load(fin)
    new_tuple_dict = {}
    for index, item in f.items():
        index_instance = find_instance_index(item[0])
        index_kpi = find_kpi_index(item[1])
        new_tuple_dict[index] = (index_instance, index_kpi)

    with open('../data_processed/i_k_index.json', 'w') as fout:
        json.dump(new_tuple_dict, fout)
