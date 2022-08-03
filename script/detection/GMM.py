import os
from functions.utils.detection_tools import conduct_pyod_detection
from functions.utils.filetools import save_list
from functions.utils.plottools import show_result

if __name__ == '__main__':
    # config
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
    test_time_base = '2022-03-20 00:00:00'
    ground_truth_path = '/data_for_run/ground_truth/groundtruth-k8s-1-2022-03-20.csv'
    train_matrix_path = '/data_for_run/data_aiops_2022/2022-03-19-cloudbed1.csv'
    test_matrix_path = '/data_for_run/data_aiops_2022/2022-03-20-cloudbed1.csv'
    model_name = 'GMM'
    file_path_root = '/experiment/experiment_run/run_home/results/GMM/'
    file_name = 'GMM__2022_03_20_cloudbed1_scores.pkl'

    # run
    anomaly_scores_list = conduct_pyod_detection(train_matrix_path, test_matrix_path,model_name)

    # show result
    show_result(test_time_base, ground_truth_path, anomaly_scores_list, model_name)

    # save the combinations list and anomaly scores list
    path = file_path_root + file_name
    save_list(anomaly_scores_list, path)