from functions.utils.filetools import read_ground_truth_file, read_list
from functions.utils.judgement import get_pre_recall_f1
from functions.utils.plottools import plot_threshold_pre_recall, plot_prc_curve, plot_roc_curve
from script.detection.run import get_instance, get_type, get_model, get_optimizer


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


if __name__ == '__main__':
    result_score_path = get_score_path()
    instance = get_instance()
    method_name = get_method_name()

    plot_pre_recall_by_threshold(result_score_path, instance, method_name)

    plot_prc(result_score_path, instance, method_name)

    plot_roc(result_score_path, instance, method_name)

    putout_f1_by_threshold_percent(result_score_path, instance)
