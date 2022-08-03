import numpy as np
import pandas as pd
from pyod.models.abod import ABOD
from pyod.models.anogan import AnoGAN
from pyod.models.auto_encoder import AutoEncoder
from pyod.models.cblof import CBLOF
from pyod.models.cof import COF
from pyod.models.copod import COPOD
from pyod.models.deep_svdd import DeepSVDD
from pyod.models.ecod import ECOD
from pyod.models.gmm import GMM
from pyod.models.hbos import HBOS
from pyod.models.iforest import IForest
from pyod.models.kde import KDE
from pyod.models.knn import KNN
from pyod.models.lof import LOF
from pyod.models.ocsvm import OCSVM
from pyod.models.pca import PCA
from pyod.models.vae import VAE
from experiment.utils import judgement
from experiment.utils.datatools import get_observation_matrix, from_test_find_train_chromosome
from experiment.utils.filetools import read_ground_truth_file


def choose_model(model_name: str):
    if model_name == 'COPOD':
        return COPOD()
    elif model_name == 'DeepSVDD':
        return DeepSVDD()
    elif model_name == 'AutoEncoder':
        return AutoEncoder()
    elif model_name == 'COF':
        return COF()
    elif model_name == 'AnoGAN':
        return AnoGAN()
    elif model_name == 'CBLOF':
        return CBLOF()
    elif model_name == 'ABOD':
        return ABOD()
    elif model_name == 'ECOD':
        return ECOD()
    elif model_name == 'GMM':
        return GMM()
    elif model_name == 'HBOS':
        return HBOS()
    elif model_name == 'IForest':
        return IForest()
    elif model_name == 'LOF':
        return LOF()
    elif model_name == 'PCA':
        return PCA()
    elif model_name == 'VAE':
        return VAE()
    elif model_name == 'OCSVM':
        return OCSVM()
    elif model_name == 'KNN':
        return KNN()
    elif model_name == 'KDE':
        return KDE()
    else:
        return None


# 输入训练ts矩阵，待测ts矩阵，ground_truth文件的path,测试时间的基准时间字符串，所选择模型的名称
# 输出模型自动判别出的异常的平均测出时延，准确率，以及召回率
def detection_test(train_ts_input,
                   test_ts_input,
                   ground_truth_path: str,
                   base_time_string: str,
                   model_name: str):
    x_test = np.array(test_ts_input)
    model = choose_model(model_name)
    clf = model.fit(train_ts_input)
    predicted = clf.predict(x_test)
    anomaly_time = []
    for i in range(len(predicted)):
        if predicted[i] == 1:
            anomaly_time.append(i)
    time_index, l, c, f = read_ground_truth_file(base_time_string, ground_truth_path)
    avg_elapse, precision, recall = judgement.judge_time_point(time_index, anomaly_time, 10)
    print("检测平均时延为{},准确率为{},召回率为{}".format(avg_elapse, precision, recall))


def print_avg_elapse_precision_recall(anomaly_time, ground_truth_path, base_time_string, time_elapse_threshold):
    time_index, l, c, f = read_ground_truth_file(base_time_string, ground_truth_path)
    avg_elapse, precision, recall = judgement.judge_time_point(time_index, anomaly_time, time_elapse_threshold)
    print("检测平均时延为{},准确率为{},召回率为{}".format(avg_elapse, precision, recall))
    return avg_elapse, precision, recall


def real_time_detect_and_return_anomaly_score(train_dict,
                                              train_matrix,
                                              test_dict,
                                              test_matrix,
                                              current_time,
                                              model_name,
                                              cols: list):
    current_observation = get_observation_matrix(test_matrix, current_time, cols)
    train_chromosome = from_test_find_train_chromosome(train_dict, test_dict, cols)
    train_matrix = get_observation_matrix(train_matrix, len(train_matrix) - 1, train_chromosome)
    x_test = np.array(current_observation)
    clf = choose_model(model_name)
    clf.fit(train_matrix)
    anomaly_scores = clf.decision_function(x_test)
    return anomaly_scores


def conduct_pyod_detection(train_matrix_path, test_matrix_path,model_name):
    print('begin ' + model_name + ' detection')
    train_df = pd.read_csv(train_matrix_path)
    test_df = pd.read_csv(test_matrix_path)
    train_df_1 = train_df.drop(['Unnamed: 0', 'time'], axis=1)
    test_df_1 = test_df.drop(['Unnamed: 0', 'time'], axis=1)
    train_array = np.array(train_df_1)
    test_array = np.array(test_df_1)
    clf = choose_model(model_name)
    clf.fit(train_array)
    anomaly_score_at_time_list = clf.decision_function(test_array)  # anomaly_score for plot
    return anomaly_score_at_time_list
