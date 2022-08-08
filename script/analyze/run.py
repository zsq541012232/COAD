from functions.utils.filetools import read_ground_truth_file, read_list
from functions.utils.plottools import plot_threshold_pre_recall, plot_prc_curve, plot_roc_curve
from script.detection.run import get_instance


def plot_pre_recall_by_threshold(score_path, instance_):
    test_time_base = instance_[1]
    ground_truth_path = '../../' + instance_[0] + '/ground_truth.csv'

    anomaly_time_point_ground_truth, l, c, f = read_ground_truth_file(test_time_base, ground_truth_path)
    anomaly_scores_at_time = read_list(score_path)
    plot_threshold_pre_recall(anomaly_time_point_ground_truth, anomaly_scores_at_time)
    # plot_roc_curve(anomaly_time_point_ground_truth, anomaly_scores_at_time, curve_label)
    # auc = calculate_auc(anomaly_time_point_ground_truth, anomaly_scores_at_time)
    # print(auc)


def plot_prc(score_path, instance_):
    test_time_base = instance_[1]
    ground_truth_path = '../../' + instance_[0] + '/ground_truth.csv'

    anomaly_time_point_ground_truth, l, c, f = read_ground_truth_file(test_time_base, ground_truth_path)
    anomaly_scores_at_time = read_list(score_path)
    plot_prc_curve(anomaly_time_point_ground_truth, anomaly_scores_at_time)


def get_score_path():
    path = input('Score path?')
    return path

def roc(score_path, instance_):
    test_time_base = instance_[1]
    ground_truth_path = '../../' + instance_[0] + '/ground_truth.csv'

    anomaly_time_point_ground_truth, l, c, f = read_ground_truth_file(test_time_base, ground_truth_path)
    anomaly_scores_at_time = read_list(score_path)
    plot_roc_curve(anomaly_time_point_ground_truth, anomaly_scores_at_time, 'roc')


if __name__ == '__main__':
    result_score_path = get_score_path()
    instance = get_instance()

    plot_pre_recall_by_threshold(result_score_path, instance)

    plot_prc(result_score_path, instance)

    roc(result_score_path, instance)
