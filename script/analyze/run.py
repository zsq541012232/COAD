from functions.utils.filetools import read_ground_truth_file, read_list
from functions.utils.judgement import get_pre_recall_f1, get_current_pre_and_recall
from functions.utils.plottools import plot_threshold_pre_recall, plot_prc_curve, plot_roc_curve, show_result
from script.detection.run import get_instance, get_type, get_model, get_optimizer
import random


def plot_pre_recall_by_threshold(score_path, instance_, method_name):
    test_time_base = instance_[1]
    ground_truth_path = '../../' + instance_[0] + '/ground_truth.csv'
    instance_name = instance_[2]

    anomaly_time_point_ground_truth, l, c, f = read_ground_truth_file(test_time_base, ground_truth_path)
    anomaly_scores_at_time = read_list(score_path)
    plot_threshold_pre_recall(anomaly_time_point_ground_truth, anomaly_scores_at_time, method_name)


def plot_prc(score_path, instance_, method_name):
    test_time_base = instance_[1]
    ground_truth_path = '../../' + instance_[0] + '/ground_truth.csv'

    anomaly_time_point_ground_truth, l, c, f = read_ground_truth_file(test_time_base, ground_truth_path)
    anomaly_scores_at_time = read_list(score_path)
    plot_prc_curve(anomaly_time_point_ground_truth, anomaly_scores_at_time, method_name)


def get_score_path():
    path = input('Score path?')
    return path


def plot_roc(score_path, instance_, method_name):
    test_time_base = instance_[1]
    ground_truth_path = '../../' + instance_[0] + '/ground_truth.csv'

    anomaly_time_point_ground_truth, l, c, f = read_ground_truth_file(test_time_base, ground_truth_path)
    anomaly_scores_at_time = read_list(score_path)
    plot_roc_curve(anomaly_time_point_ground_truth, anomaly_scores_at_time, method_name)


def putout_f1_by_threshold_percent(score_path, instance_):
    test_time_base = instance_[1]
    ground_truth_path = '../../' + instance_[0] + '/ground_truth.csv'

    anomaly_time_point_ground_truth, l, c, f = read_ground_truth_file(test_time_base, ground_truth_path)
    anomaly_scores_at_time = read_list(score_path)

    percent_step = 10
    print('The percent step is ' + str(percent_step) + '%.')
    percent_x = [i / 100 for i in range(0, 100 + 1, percent_step)]
    pre, recall, f1 = get_pre_recall_f1(anomaly_time_point_ground_truth=anomaly_time_point_ground_truth,
                                        anomaly_scores_at_time=anomaly_scores_at_time,
                                        percent_x=percent_x)
    f1_len = len(f1) - 1
    for index, value in enumerate(f1):
        percent_current = index / f1_len
        print(str(percent_current) + ': ' + str(value))


def get_method_name():
    return_method_name = ''
    detection_type = get_type()
    detection_model = get_model()

    if detection_type == 'COAD':
        optimizer = get_optimizer()
        return_method_name += optimizer + '_' + str(detection_model)
    else:
        return_method_name += 'BASIC' + '_' + str(detection_model)

    return return_method_name


def get_f1(anomaly_time_point_ground_truth, anomaly_scores_at_time, percent):
    max_score = max(anomaly_scores_at_time)
    min_score = min(anomaly_scores_at_time)
    span_score = max_score - min_score
    threshold = max_score - percent * span_score
    pre, recall = get_current_pre_and_recall(anomaly_time_point_ground_truth,
                                             anomaly_scores_at_time,
                                             threshold)
    if pre + recall == 0:
        f1 = 0
    else:
        f1 = 2 * pre * recall / (pre + recall)

    return f1


def putout_f1_by_random_choose_threshold(score_path, instance_):
    f1_list = []
    random_choose_time = 10000

    test_time_base = instance_[1]
    ground_truth_path = '../../' + instance_[0] + '/ground_truth.csv'

    anomaly_time_point_ground_truth, l, c, f = read_ground_truth_file(test_time_base, ground_truth_path)
    anomaly_scores_at_time = read_list(score_path)

    for i in range(random_choose_time):
        random_percent = random.random()
        f1 = get_f1(anomaly_time_point_ground_truth=anomaly_time_point_ground_truth,
                    anomaly_scores_at_time=anomaly_scores_at_time,
                    percent=random_percent)
        f1_list.append(f1)

    return sum(f1_list) / len(f1_list)


def putout_max_f1_among_all_threshold(score_path, instance_):
    f1_list = []

    test_time_base = instance_[1]
    ground_truth_path = '../../' + instance_[0] + '/ground_truth.csv'

    anomaly_time_point_ground_truth, l, c, f = read_ground_truth_file(test_time_base, ground_truth_path)
    anomaly_scores_at_time = read_list(score_path)

    for percent_int in range(0, 101):
        current_percentage = percent_int / 100
        f1 = get_f1(anomaly_time_point_ground_truth=anomaly_time_point_ground_truth,
                    anomaly_scores_at_time=anomaly_scores_at_time,
                    percent=current_percentage)
        f1_list.append(f1)

    return max(f1_list)


if __name__ == '__main__':
    result_score_path = get_score_path()
    instance = get_instance()
    method_name = get_method_name()
    test_time_base = instance[1]
    ground_truth_path = '../../' + instance[0] + '/ground_truth.csv'
    anomaly_scores_list = read_list(result_score_path)
    model_name = method_name

    plot_pre_recall_by_threshold(result_score_path, instance, method_name)
    #
    # plot_prc(result_score_path, instance, method_name)
    #
    # plot_roc(result_score_path, instance, method_name)
    #
    # putout_f1_by_threshold_percent(result_score_path, instance)
    #
    show_result(test_time_base, ground_truth_path, anomaly_scores_list, model_name)

    avg_f1 = putout_f1_by_random_choose_threshold(result_score_path, instance)
    print('avg_f1: ' + str(avg_f1))

    max_f1 = putout_max_f1_among_all_threshold(result_score_path, instance)
    print('max_f1: ' + str(max_f1))
