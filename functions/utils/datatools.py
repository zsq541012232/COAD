import copy


def get_dict_key(dic, value):
    keys = list(dic.keys())
    values = list(dic.values())
    if value not in values:
        return None
    idx = values.index(value)
    key = keys[idx]
    return key


def get_vector_by_index(index_dict: dict, matrix: list, index: int):
    if index > len(index_dict) or index < 0:
        return None
    h = len(matrix)
    instance_kpi_tuple = index_dict[index]
    ts_list = [[matrix[i][index]] for i in range(h)]
    return instance_kpi_tuple, ts_list


def get_vector_by_tuple(index_dict: dict, matrix: list, instance_kpi_tuple: tuple):
    if instance_kpi_tuple not in index_dict.values():
        return None
    h = len(matrix)
    key = get_dict_key(index_dict, instance_kpi_tuple)
    ts_list = [[matrix[i][key]] for i in range(h)]
    return key, ts_list


def join_two_vector_and_their_index(ts_list_1, index_dict_1, ts_list_2, index_dict_2):
    different_key_in_2 = []
    for key, value in index_dict_2.items():
        if value not in index_dict_1.values():
            different_key_in_2.append(key)
    new_dict = copy.deepcopy(index_dict_1)
    new_list = []

    original_len = len(index_dict_1)
    append_len = len(different_key_in_2)
    for i in range(append_len):
        new_dict[original_len + i] = index_dict_2[different_key_in_2[i]]
    for i in range(len(ts_list_1)):
        row = []
        for j in range(original_len + append_len):
            if j < original_len:
                row.append(ts_list_1[i][j])
            else:
                row.append(ts_list_2[i][different_key_in_2[j - original_len]])
        new_list.append(row)
    return new_dict, new_list


def max_min_normalization(matrix: list):
    h = len(matrix)
    w = len(matrix[0])
    new_matrix = [[0 for i in range(w)] for j in range(h)]
    for i in range(w):
        max_v = float('-inf')
        min_v = float('inf')
        for j in range(h):
            if max_v < matrix[j][i]:
                max_v = matrix[j][i]
            if min_v > matrix[j][i]:
                min_v = matrix[j][i]
        if max_v != min_v:
            for j in range(h):
                new_matrix[j][i] = (matrix[j][i] - min_v) / (max_v - min_v)
    return new_matrix


def one_dif_on_matrix(matrix: list):
    h = len(matrix)
    w = len(matrix[0])
    new_matrix = []
    for i in range(h):
        if i == 0:
            row = [0.0 for j in range(w)]
            new_matrix.append(row)
        else:
            row = [(matrix[i][j] - matrix[i - 1][j]) for j in range(w)]
            new_matrix.append(row)
    return new_matrix


def search_insert(nums, target):
    s1 = 0
    s2 = len(nums)
    if s2 == 0:
        return 0
    elif target <= nums[0]:
        return 0
    elif target > nums[-1]:
        return s2
    elif target == nums[-1]:
        return s2 - 1
    else:
        while True:
            index = (s1 + s2) // 2
            if nums[index] < target <= nums[index + 1]:
                return index + 1
            elif nums[index] >= target > nums[index - 1]:
                return index
            elif target > nums[index]:
                s1 = index + 1
            elif target < nums[index]:
                s2 = index - 1


def normalization_and_onedif(matrix: list):
    new_matrix = max_min_normalization(matrix)
    return one_dif_on_matrix(new_matrix)


def get_observation_matrix(matrix, current_time, col_chormosome):
    observation_matrix = []
    for i in range(current_time + 1):
        row = []
        for j in range(len(col_chormosome)):
            row.append(matrix[i][col_chormosome[j]])
        observation_matrix.append(row)
    return observation_matrix


def get_median(data):
    data = sorted(data)
    size = len(data)
    if size % 2 == 0:
        median = (data[size // 2] + data[size // 2 - 1]) / 2
        data[0] = median
    if size % 2 == 1:
        median = data[(size - 1) // 2]
        data[0] = median
    return data[0]


def list_reverse(nums):
    return list(map(list, zip(*nums)))


def find_col(matrix, col_num):
    matrix_w = len(matrix[0])
    if col_num >= matrix_w:
        return None
    matrix_h = len(matrix)
    col_list = []
    for i in range(matrix_h):
        col_list.append(matrix[i][col_num])
    return col_list


def align_matrix(tuple_dict_1, matrix_1, tuple_dict_2, matrix_2):
    if len(tuple_dict_1) != len(tuple_dict_2):
        return None
    new_matrix_2_T = []
    for index, value in tuple_dict_1.items():
        if tuple_dict_2[index] == value:
            new_row = find_col(matrix_1, index)
            new_matrix_2_T.append(new_row)
        else:
            index_find = get_dict_key(tuple_dict_2, value)
            new_row = find_col(matrix_2, index_find)
            new_matrix_2_T.append(new_row)
    new_matrix_2 = list_reverse(new_matrix_2_T)
    return new_matrix_2


def from_test_find_train_chromosome(train_dict, test_dict, test_chromosome):
    test_values = []
    for chromo in test_chromosome:
        test_values.append(test_dict[chromo])
    train_chormosome = []
    for value in test_values:
        key_find = get_dict_key(train_dict, value)
        train_chormosome.append(key_find)
    return train_chormosome


def get_tuple_names_from_chromosome(col_name_list, chromosome):
    tuple_name_list = []
    for index, number in enumerate(chromosome):
        tuple_name_list.append(col_name_list[number])
    return tuple_name_list


# normalize the anomaly score
def data_normalize(score_list):
    returned_list = []
    max_score = max(score_list)
    min_score = min(score_list)
    score_span = max_score - min_score
    for index, value in enumerate(score_list):
        value_normalized = (value - min_score) / score_span
        returned_list.append(value_normalized)
    return returned_list
