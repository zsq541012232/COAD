from functions.detection.anomaly_detection_tools import read_matrix
from functions.utils.filetools import read_ground_truth_file
from functions.utils.plottools import plot_dataset_affected_metric_number_by_ground_truth, \
    plot_dataset_affected_metrics_number_sorted_colored
from script.detection.run import get_instance
import numpy as np
import script.plans.plan as plobj

train_df_lists_by_metric = []
value_upper_lists = []
value_lower_lists = []


def get_test_list(test_df, metric_id):
    return_list = [test_df[i][metric_id] for i in range(len(test_df))]

    return return_list


def get_train_list(train_df, metric_id):
    return_list = [train_df[i][metric_id] for i in range(len(train_df))]

    return return_list


def is_current_metric_affected(ground_truth_time, test_metric_list, elapse_time_):
    abnormal_value_number = 0
    list_mean = np.mean(test_metric_list)
    list_dev = np.std(test_metric_list)
    value_upper = list_mean + 3 * list_dev
    value_lower = list_mean - 3 * list_dev
    for index in range(ground_truth_time, ground_truth_time + elapse_time_ + 1):
        if test_metric_list[index] > value_upper or test_metric_list[index] < value_lower:
            abnormal_value_number += 1

    if abnormal_value_number == 0:  # This metric value is not affected
        return -1
    return 1


def get_current_ground_truth_affected_metric_number(ground_truth_time, test_df, elapse_time_):
    metric_len = len(test_df[0])
    affected_metric_number = 0
    for metric_id in range(metric_len):
        test_metric_list = get_test_list(test_df, metric_id)
        current_metric_affected_flag = is_current_metric_affected(ground_truth_time=ground_truth_time,
                                                                  test_metric_list=test_metric_list,
                                                                  elapse_time_=elapse_time_)
        if current_metric_affected_flag == 1:
            affected_metric_number += 1

    return affected_metric_number


def get_affected_metric_number_list_by_ground_truth(sorted_ground_truth_time, test_df, elapse_time_):
    return_list = []
    for index, ground_truth_time in enumerate(sorted_ground_truth_time):
        current_affected_metric_number = get_current_ground_truth_affected_metric_number(
            ground_truth_time=ground_truth_time,
            test_df=test_df,
            elapse_time_=elapse_time_)
        return_list.append(current_affected_metric_number)

    return return_list


def analyze_dataset():
    instance = get_instance()
    test_time_base = instance[1]
    ground_truth_path = '../../' + instance[0] + '/ground_truth.csv'
    train_df_path = '../../' + instance[0] + '/train_df.csv'
    test_df_path = '../../' + instance[0] + '/test_df.csv'

    train_matrix, test_matrix = read_matrix(train_matrix_path=train_df_path,
                                            test_matrix_path=test_df_path)
    anomaly_time_point_ground_truth, l, c, f = read_ground_truth_file(test_time_base, ground_truth_path)
    sorted_ground_truth = list(sorted(anomaly_time_point_ground_truth))

    elapse_time = 5
    abnormal_metric_number_in_five_minutes = get_affected_metric_number_list_by_ground_truth(
        sorted_ground_truth_time=sorted_ground_truth,
        test_df=test_matrix,
        elapse_time_=elapse_time)

    plot_dataset_affected_metric_number_by_ground_truth(list=abnormal_metric_number_in_five_minutes,
                                                        data_instance=instance)


def put_out_all_data_instance_analyze_result():
    for instance in plobj.instances:
        test_time_base = instance[1]
        ground_truth_path = '../../' + instance[0] + '/ground_truth.csv'
        train_df_path = '../../' + instance[0] + '/train_df.csv'
        test_df_path = '../../' + instance[0] + '/test_df.csv'

        train_matrix, test_matrix = read_matrix(train_matrix_path=train_df_path,
                                                test_matrix_path=test_df_path)
        anomaly_time_point_ground_truth, l, c, f = read_ground_truth_file(test_time_base, ground_truth_path)
        sorted_ground_truth = list(sorted(anomaly_time_point_ground_truth))

        elapse_time = 5
        abnormal_metric_number_in_five_minutes = get_affected_metric_number_list_by_ground_truth(
            sorted_ground_truth_time=sorted_ground_truth,
            test_df=test_matrix,
            elapse_time_=elapse_time)
        print(instance[2] + ': ' + str(abnormal_metric_number_in_five_minutes))


def is_normal(current_value, upper_value, lower_value):
    if lower_value <= current_value <= upper_value:
        return True
    else:
        return False


def get_current_affected_metrics_number(test_df_list):
    global value_upper_lists
    global value_lower_lists
    metrics_len = len(test_df_list)
    returned_number = 0
    for current_metric in range(metrics_len):
        current_value = test_df_list[current_metric]
        upper_value = value_upper_lists[current_metric]
        lower_value = value_lower_lists[current_metric]
        if is_normal(current_value, upper_value, lower_value):
            pass
        else:
            returned_number += 1

    return returned_number


def fill_global_lists_by_metric(train_df):
    global train_df_lists_by_metric
    global value_upper_lists
    global value_lower_lists
    metrics_len = len(train_df[0])
    for i in range(metrics_len):
        current_train_list = get_train_list(train_df, i)
        train_df_lists_by_metric.append(current_train_list)
        list_mean = np.mean(current_train_list)
        list_dev = np.std(current_train_list)
        value_upper = list_mean + 3 * list_dev
        value_lower = list_mean - 3 * list_dev
        value_upper_lists.append(value_upper)
        value_lower_lists.append(value_lower)


def get_affected_metric_number_list_by_time(train_df, test_df):
    time_len = len(test_df)
    returned_list = []
    fill_global_lists_by_metric(train_df)

    for current_time in range(time_len):
        test_df_list = test_df[current_time]
        current_affected_metrics_number = get_current_affected_metrics_number(test_df_list)
        returned_list.append(current_affected_metrics_number)

    return returned_list


def get_current_affected_metrics_number_plus_weight(test_df_list):
    global value_upper_lists
    global value_lower_lists
    metrics_len = len(test_df_list)
    returned_number = 0
    for current_metric in range(metrics_len):
        current_value = test_df_list[current_metric]
        upper_value = value_upper_lists[current_metric]
        lower_value = value_lower_lists[current_metric]
        mean_value = (upper_value + lower_value) / 2
        value_abs = abs(current_value - mean_value)
        returned_number += value_abs


    return returned_number


def get_affected_metric_number_plus_weight_by_time(train_df, test_df):
    time_len = len(test_df)
    returned_list = []
    fill_global_lists_by_metric(train_df)

    for current_time in range(time_len):
        test_df_list = test_df[current_time]
        current_affected_metrics_number = get_current_affected_metrics_number_plus_weight(test_df_list)
        returned_list.append(current_affected_metrics_number)

    # normalize
    returned_list_max = max(returned_list)
    returned_list_normalized = [returned_list[i] / returned_list_max for i in range(len(returned_list))]

    return returned_list_normalized


def analyze_dataset_improve():
    instance = get_instance()
    test_time_base = instance[1]
    ground_truth_path = '../../' + instance[0] + '/ground_truth.csv'
    train_df_path = '../../' + instance[0] + '/train_df.csv'
    test_df_path = '../../' + instance[0] + '/test_df.csv'

    train_matrix, test_matrix = read_matrix(train_matrix_path=train_df_path,
                                            test_matrix_path=test_df_path)
    anomaly_time_point_ground_truth, l, c, f = read_ground_truth_file(test_time_base, ground_truth_path)
    sorted_ground_truth = list(sorted(anomaly_time_point_ground_truth))
    elapse_time = 5

    affected_metrics_number_order_by_time = get_affected_metric_number_list_by_time(
        train_df=train_matrix,
        test_df=test_matrix,
    )

    # affected_metrics_number_order_by_time = get_affected_metric_number_plus_weight_by_time(
    #     train_df=train_matrix,
    #     test_df=test_matrix,
    # )

    plot_dataset_affected_metrics_number_sorted_colored(
        affected_metrics_number_list=affected_metrics_number_order_by_time,
        ground_truth_time_list=sorted_ground_truth,
        elapse_time=elapse_time,
        instance=instance
    )


if __name__ == '__main__':
    analyze_dataset_improve()
