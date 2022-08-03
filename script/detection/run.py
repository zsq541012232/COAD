import os
from functions.detection.anomaly_detection_tools import anomaly_detection
from functions.utils.detection_tools import conduct_pyod_detection
from functions.utils.filetools import save_list
from functions.utils.plottools import show_result
import script.plans.plan as plobj


def get_type():
    flag = True
    return_type = ''
    while flag:
        answer = input('Use COAD? y/n?')
        if answer == 'y' or answer == 'Y':
            return_type = 'COAD'
        elif answer == 'n' or answer == 'N':
            return_type = 'BASIC'
        else:
            continue
        flag = False
    return return_type


def get_model():
    flag = True
    return_model = ''
    while flag:
        print('The models are:', str(plobj.model_names))
        answer = input('Use which model?')
        if answer not in plobj.model_names:
            continue
        else:
            return_model = answer
            flag = False
    return return_model


def get_optimizer():
    flag = True
    return_optimizer = ''
    while flag:
        print('The models are:', str(plobj.optimizers))
        answer = input('Use which optimizer?')
        if answer not in plobj.optimizers:
            continue
        else:
            return_optimizer = answer
            flag = False
    return return_optimizer


def get_instance(index):
    return plobj.instance_paths[index]


def conduct_basic_detection(test_time_base, ground_truth_path, train_df_path, test_df_path,
                            model_name):
    # config
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
    file_path_root = 'result'
    file_head = str(model_name) + '_' + str(test_time_base[:10]) + '_'
    file_name_scores = file_head + 'scores.pkl'

    # run
    anomaly_scores_list = conduct_pyod_detection(train_df_path, test_df_path, model_name)

    # show result
    show_result(test_time_base, ground_truth_path, anomaly_scores_list, model_name)

    # save the combinations list and anomaly scores list
    path = file_path_root + file_name_scores
    save_list(anomaly_scores_list, path)


def conduct_coad_detection(test_time_base, ground_truth_path, train_df_path, test_df_path,
                           optimizer, model_name):
    # config
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
    file_head = str(optimizer) + '_' + str(model_name) + '_' + str(test_time_base[:10]) + '_'
    file_name_combination = file_head + 'combination.pkl'
    file_name_scores = file_head + 'scores.pkl'
    file_path_root = 'result/'

    # run
    solutions_list, anomaly_scores_list = anomaly_detection(model_name=model_name,
                                                            train_matrix_path=train_df_path,
                                                            test_matrix_path=test_df_path,
                                                            optimizer=optimizer)

    # show result
    show_result(test_time_base, ground_truth_path, anomaly_scores_list, model_name)

    # save the combinations list and anomaly scores list
    path_combination = file_path_root + file_name_combination
    path_scores = file_path_root + file_name_scores

    save_list(solutions_list, path_combination)
    save_list(anomaly_scores_list, path_scores)


if __name__ == '__main__':
    detection_type = get_type()
    detection_model = get_model()
    instance_information = get_instance(0)

    test_time_base = instance_information[1]
    ground_truth_path = instance_information[0] + '/ground_truth.csv'
    train_df_path = instance_information[0] + '/train_df.csv'
    test_df_path = instance_information[0] + '/test_df.csv'

    if detection_type == 'COAD':
        optimizer = get_optimizer()
        conduct_coad_detection(test_time_base=test_time_base,
                               ground_truth_path=ground_truth_path,
                               train_df_path=train_df_path,
                               test_df_path=test_df_path,
                               optimizer=optimizer,
                               model_name=detection_model)
    else:
        conduct_basic_detection(test_time_base=test_time_base,
                                ground_truth_path=ground_truth_path,
                                train_df_path=train_df_path,
                                test_df_path=test_df_path,
                                model_name=detection_model)
