from experiment.utils.filetools import read_ground_truth_file, read_list
from experiment.utils.plottools import plot_threshold_pre_recall

if __name__ == '__main__':
    test_time_base = '2022-03-20 00:00:00'
    ground_truth_path = '/Users/zsq/Desktop/Experiment/data_for_run/ground_truth/groundtruth-k8s-1-2022-03-20.csv'
    anomaly_time_point_ground_truth, l, c, f = read_ground_truth_file(test_time_base,
                                                 ground_truth_path)
    curve_label = 'GMM_c1_2022_03_20'
    anomaly_scores_at_time = read_list(
        '/experiment/experiment_run/run_home/results/basic/GMM/GMM__2022_03_20_cloudbed1_scores.pkl')
    # plot_roc_curve(anomaly_time_point_ground_truth, anomaly_scores_at_time, curve_label)
    plot_threshold_pre_recall(anomaly_time_point_ground_truth, anomaly_scores_at_time)
    # auc = calculate_auc(anomaly_time_point_ground_truth, anomaly_scores_at_time)
    # print(auc)