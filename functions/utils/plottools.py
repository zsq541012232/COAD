from matplotlib import pyplot as plt

# 画一个ts
from functions.utils.filetools import read_ground_truth_file
from functions.utils.judgement import get_fpr_and_tpr, get_pre_recall_f1


def plot_function_a_single_ts(ts_dict):
    ts_dict_tuple_list = sorted(ts_dict.items(), key=lambda x: x[0])
    x = []
    y = []
    for index, value in ts_dict_tuple_list:
        x.append(index)
        y.append(value)
    plt.plot(x, y)
    plt.show()


# 画一个list
def plot_list_with_index(list):
    x = [i for i in range(len(list))]
    plt.plot(x, list)
    plt.show()


def plot_dataset_affected_metric_number_by_ground_truth(list, data_instance):
    instance_name = data_instance[2]
    x = [i for i in range(len(list))]
    plt.rcParams['savefig.dpi'] = 300
    plt.rcParams['figure.dpi'] = 300
    plt.plot(x, list)
    plt.xlabel('Ground Truth ID')
    plt.ylabel('Affected Metric Number (3-sigma)')
    plt.title(instance_name)
    plt.show()


def plot_anomaly_line_with_ground_truth(list, ground_truth_time_list, model_name):
    x = [i for i in range(1440)]
    y = list[:1440]
    plt.rcParams['figure.figsize'] = (15, 4)
    plt.rcParams['savefig.dpi'] = 300
    plt.rcParams['figure.dpi'] = 300
    plt.plot(x, y, label=model_name + '_detected_result', linewidth=0.7,
             alpha=0.5,
             ls='-.',
             color='blue', marker='*')
    plt.vlines(ground_truth_time_list, ymin=min(y), ymax=max(y), label='ground_truth', colors='green')
    plt.xlabel('Timestamp')
    plt.ylabel('Anomaly Score')
    plt.legend()
    plt.show()


def show_result(test_time_base, ground_truth_path, anomaly_scores_list, model_name):
    time_index, l, c, f = read_ground_truth_file(test_time_base,
                                                 ground_truth_path)  # get the ground_truth anomaly time point
    plot_anomaly_line_with_ground_truth(anomaly_scores_list, time_index, model_name)


def plot_roc_curve(anomaly_time_point_ground_truth, anomaly_scores_at_time, method_name):
    FPR, TPR = get_fpr_and_tpr(anomaly_time_point_ground_truth, anomaly_scores_at_time)
    plt.plot(FPR, TPR, label='roc', linewidth=0.7,
             alpha=0.5,
             ls='-.',
             color='blue', marker='*')
    plt.title(method_name)
    plt.xlabel('FPR')
    plt.ylabel('TPR')
    plt.legend()
    plt.show()


def plot_threshold_pre_recall(anomaly_time_point_ground_truth, anomaly_scores_at_time, method_name):
    percent_x = [i / 100 for i in range(100 + 1)]
    pre_y, recall_y, f1_y = get_pre_recall_f1(anomaly_time_point_ground_truth,
                                              anomaly_scores_at_time,
                                              percent_x)
    fig, ax = plt.subplots()  # 创建图实例
    ax.plot(percent_x, pre_y, label='precision', linewidth=0.7,
            alpha=0.5,
            ls='-.',
            color='blue', marker='*')
    ax.plot(percent_x, recall_y, label='recall', linewidth=0.7,
            alpha=0.5,
            ls='-.',
            color='red', marker='*')
    ax.plot(percent_x, f1_y, label='f1-score', linewidth=0.7,
            alpha=0.5,
            ls='-.',
            color='green', marker='*')
    plt.xlabel('Threshold Percentage')
    plt.title(method_name)
    ax.legend()
    # plt.savefig(fname='/Users/zsq/Desktop/111.png', dpi=300)
    plt.show()



def plot_prc_curve(anomaly_time_point_ground_truth, anomaly_scores_at_time, method_name):
    percent_x = [i / 100 for i in range(100 + 1)]
    pre_y, recall_y, f1_y = get_pre_recall_f1(anomaly_time_point_ground_truth,
                                              anomaly_scores_at_time,
                                              percent_x)
    fig, ax = plt.subplots()  # 创建图实例
    ax.plot(recall_y, pre_y, label='prc', linewidth=0.7,
            alpha=0.5,
            ls='-.',
            color='red', marker='*')
    plt.title(method_name)
    plt.xlabel('Recall')
    plt.ylabel('Precision')
    ax.legend()
    plt.show()
