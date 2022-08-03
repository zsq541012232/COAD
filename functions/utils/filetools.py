import pickle
import time
import pandas as pd
from experiment.utils.datatools import get_dict_key,join_two_vector_and_their_index
import os


# 读取指定kpi文件，并输入其日期信息
# 返回高为1450的矩阵，每一列代表一个ts，dict信息代表每一列的ts名，下标从0开始
def read_file(path, base_time_string):
    tuple_list = []
    f = pd.read_csv(path)
    for index, value in f.iterrows():
        instance_name = value[1]
        kpi_name = value[2]
        if (instance_name, kpi_name) not in tuple_list:
            tuple_list.append((instance_name, kpi_name))
    tuple_dict = {}
    for index, item in enumerate(tuple_list):
        tuple_dict[index] = item
    init_matrix = [[0 for i in range(len(tuple_list))] for j in range(1450)]
    base_time_stamp = int(time.mktime(time.strptime(base_time_string, "%Y-%m-%d %H:%M:%S")))
    f = pd.read_csv(path)
    for index, value in f.iterrows():
        instance_name = value[1]
        kpi_name = value[2]
        time_row = int((value[0] - base_time_stamp) / 60)
        key = get_dict_key(tuple_dict, (instance_name, kpi_name))
        init_matrix[time_row][key] = value[3]
    return tuple_dict, init_matrix


# 输入日期信息和groundtruth所在文件路径
# 返回4个list信息
def read_ground_truth_file(base_time_string, path):
    f = pd.read_csv(path)
    time_index = []
    levels = []
    cmdb_ids = []
    failure_types = []
    for index, value in f.iterrows():
        base_time_stamp = int(time.mktime(time.strptime(base_time_string, "%Y-%m-%d %H:%M:%S")))
        time_index.append(int((value[0] - base_time_stamp) / 60))
        levels.append(value[1])
        cmdb_ids.append(value[2])
        failure_types.append(value[3])
    return time_index, levels, cmdb_ids, failure_types


# 这个函数将会读取file_paths中的所有以kpi开头的文件，并且将他们粘合成一个matrix，并返回其列信息和matrix
def get_all_kpi_files_into_a_matrix(file_paths:list,base_time:str):
    print('开始合并文件为matrix：')
    ituple_dict_init, matrix_init = read_file(file_paths[0],base_time)
    dict_new, matrix_new = ituple_dict_init, matrix_init
    i = 1
    for index,item in enumerate(file_paths):
        if index != 0:
            print('合并文件为matrix，进度{}'.format(i/len(file_paths)))
            tuple_dict, matrix = read_file(item,base_time)
            dict_new, matrix_new = join_two_vector_and_their_index(matrix,tuple_dict,matrix_new,dict_new)
            i += 1
    return dict_new,matrix_new


def get_file_path_list_from_roots(root_lists):
    return_list = []
    for root_path in root_lists:
        for root, dirs, files in os.walk(root_path):
            for file_name in files:
                if file_name.startswith('kpi_'):
                    file_path = os.path.join(root, file_name)
                    return_list.append(file_path)
    return return_list


def save_list(list_to_save,path):
    open_file = open(path, "wb")
    pickle.dump(list_to_save, open_file)
    open_file.close()

def read_list(path):
    open_file = open(path, "rb")
    loaded_list = pickle.load(open_file)
    open_file.close()
    return loaded_list



