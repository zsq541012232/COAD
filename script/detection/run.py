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


def get_instance():
    flag = True
    index = 0
    while flag:
        index = int(input('Which instance?'))
        if 0 <= index < len(plobj.instances):
            flag = False
    return plobj.instances[index]


def conduct_basic_detection(instance,model_name):
    test_time_base = instance[1]
    ground_truth_path = instance[0] + '/ground_truth.csv'
    train_df_path = instance[0] + '/train_df.csv'
    test_df_path = instance[0] + '/test_df.csv'
    instance_name = instance[2]
    # config
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
    file_path_root = 'result'
    file_head = str(model_name) + '_' + str(instance_name) + '_'
    file_name_scores = file_head + 'scores.pkl'

    # run
    anomaly_scores_list = conduct_pyod_detection(train_df_path, test_df_path, model_name)

    # show result
    show_result(test_time_base, ground_truth_path, anomaly_scores_list, model_name)

    # save the combinations list and anomaly scores list
    path = file_path_root + file_name_scores
    save_list(anomaly_scores_list, path)


def conduct_coad_detection(instance,optimizer, model_name):
    test_time_base = instance[1]
    ground_truth_path = instance[0] + '/ground_truth.csv'
    train_df_path = instance[0] + '/train_df.csv'
    test_df_path = instance[0] + '/test_df.csv'
    instance_name = instance[2]
    # config
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
    file_head = str(optimizer) + '_' + str(model_name) + '_' + str(instance_name) + '_'
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
    instance = get_instance()

    if detection_type == 'COAD':
        optimizer = get_optimizer()
        conduct_coad_detection(instance=instance,
                               optimizer=optimizer,
                               model_name=detection_model)
    else:
        conduct_basic_detection(instance=instance,
                                model_name=detection_model)