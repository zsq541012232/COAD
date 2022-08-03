import os
from functions.detection.anomaly_detection_tools import anomaly_detection
from functions.utils.filetools import save_list
from functions.utils.plottools import show_result

if __name__ == '__main__':
    # config
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
    test_time_base = '2022-03-20 00:00:00'
    ground_truth_path = '/Users/zsq/Desktop/Experiment/data_for_run/ground_truth/groundtruth-k8s-1-2022-03-20.csv'
    train_matrix_path = '/Users/zsq/Desktop/Experiment/data_for_run/data_aiops_2022/2022-03-19-cloudbed1.csv'
    test_matrix_path = '/Users/zsq/Desktop/Experiment/data_for_run/data_aiops_2022/2022-03-20-cloudbed1.csv'
    optimizer = 'BBO'
    model_name = 'GMM'
    file_name_1 = 'BBO_GMM_c1__2022_03_20_cloudbed1_combinations.pkl'
    file_name_2 = 'BBO_GMM_c1__2022_03_20_cloudbed1_scores.pkl'
    file_path_root = '/Users/zsq/Desktop/Experiment/experiment/experiment_run/run_home/results/combination_basic/BBO/BBO_GMM'

    # run
    solutions_list, anomaly_scores_list = anomaly_detection(model_name=model_name,
                                                            train_matrix_path=train_matrix_path,
                                                            test_matrix_path=test_matrix_path,
                                                            optimizer=optimizer)

    # show result
    show_result(test_time_base, ground_truth_path, anomaly_scores_list, model_name)

    # save the combinations list and anomaly scores list
    path_1 = file_path_root + file_name_1
    path_2 = file_path_root + file_name_2

    save_list(solutions_list,path_1)
    save_list(anomaly_scores_list,path_2)