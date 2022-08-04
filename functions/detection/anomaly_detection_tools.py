import numpy as np
import pandas as pd
from functions.detection.optimizer import get_optimizer
from functions.utils.detection_tools import choose_model


# 全局变量
train_matrix = []
test_matrix = []
detection_model_name = ''
current_time = 0
solution_length = 20


def anomaly_detection(model_name,
                      train_matrix_path,
                      test_matrix_path,
                      optimizer: str):
    # 读入数据
    global train_matrix
    global test_matrix
    global detection_model_name
    global current_time
    train_matrix, test_matrix = read_matrix(train_matrix_path=train_matrix_path,
                                            test_matrix_path=test_matrix_path)
    detection_model_name = model_name

    # 优化问题的定义
    problem_dict = problem_generation()
    # 选择模型
    model = get_optimizer(optimizer,problem_dict)
    # 对每个时间点进行检测
    current_time = 0
    solutions_list, anomaly_scores_list = conduct_detection_in_real_time(optimizer_model=model)
    return solutions_list,anomaly_scores_list


def fitness_function(solution):
    clf = choose_model(detection_model_name)
    train_array, test_vector = get_array_data(solution)
    clf.fit(train_array)
    anomaly_score_list = clf.decision_function(test_vector)
    fx = anomaly_score_list[0]
    return fx


def get_array_data(solution):
    return_train_list = []
    return_test_list = []
    solution_positions = list(set(solution))
    # 获取train
    for train_row in range(len(train_matrix)):
        new_row = [train_matrix[train_row][solution_pos] for solution_pos in solution_positions]
        return_train_list.append(new_row)
    # 获取test
    return_test_list.append([test_matrix[current_time][solution_pos] for solution_pos in solution_positions])
    # 转换成np_array
    return_train_array = np.array(return_train_list)
    return_test_array = np.array(return_test_list)
    return return_train_array, return_test_array


# solution中的值只可能是整数
def amend_position(solution, lowerbound, upperbound):
    pos = np.clip(solution, lowerbound, upperbound)
    return pos.astype(int)


def read_matrix(train_matrix_path: str, test_matrix_path: str):
    train_df = pd.read_csv(train_matrix_path)
    test_df = pd.read_csv(test_matrix_path)
    train_df_1 = train_df.drop(['Unnamed: 0', 'time'], axis=1)
    test_df_1 = test_df.drop(['Unnamed: 0', 'time'], axis=1)
    train_array = np.array(train_df_1)
    test_array = np.array(test_df_1)
    train_list = train_array.tolist()
    test_list = test_array.tolist()
    return train_list, test_list


def conduct_detection_in_real_time(optimizer_model):
    global current_time
    solutions_list = []
    anomaly_scores_list = []
    time_len = len(test_matrix)
    while current_time < time_len:
        print('time_point：' + str(current_time) + ' detecting')
        best_position, best_fitness = optimizer_model.solve()
        solutions_list.append(best_position)
        anomaly_scores_list.append(best_fitness)
        print('time_point: ' + str(current_time) + ' anomaly_score is: ' + str(best_fitness))
        current_time += 1
    return solutions_list, anomaly_scores_list


def problem_generation():
    index_bound = len(test_matrix[0])

    problem_dict = {
        "fit_func": fitness_function,
        "lb": [0, ] * solution_length,
        "ub": [index_bound-0.1, ] * solution_length,
        "minmax": "max",
        "amend_position": amend_position
    }
    return problem_dict



