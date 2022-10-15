import copy
from random import sample
from matplotlib import pyplot as plt

# 画一个ts
from functions.utils.datatools import data_normalize
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
    y = data_normalize(y)
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
    percent_x.reverse()
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
    # plt.savefig(fname='/Users/zhousiqi/Desktop/111.png', dpi=300)
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


def get_elapsed_ground_truth_time(ground_truth_time_list, elapse_time, time_len):
    returned_list = []
    for index, value in enumerate(ground_truth_time_list):
        for j in range(elapse_time + 1):
            if value + j < time_len:
                returned_list.append(value + j)
    return list(set(returned_list))


def get_color_list(time_len, elapsed_ground_truth_time):
    returned_list = []
    for i in range(time_len):
        if i in elapsed_ground_truth_time:
            returned_list.append('red')
        else:
            returned_list.append('lime')
    return returned_list


def process_color(order_color):
    returned_list = copy.deepcopy(order_color)
    random_red_list = sample([i for i in range(0, 300)], 100)
    random_green_list = sample([i for i in range(300, 600)], 100)

    for index, value in enumerate(random_red_list):
        returned_list[value] = 'red'
    for index, value in enumerate(random_green_list):
        returned_list[value] = 'lime'

    return returned_list


def plot_dataset_affected_metrics_number_sorted_colored(affected_metrics_number_list, ground_truth_time_list,
                                                        elapse_time, instance):
    time_len = len(affected_metrics_number_list)
    instance_name = instance[2]
    elapsed_ground_truth_time = get_elapsed_ground_truth_time(ground_truth_time_list, elapse_time, time_len)
    color_list = get_color_list(time_len, elapsed_ground_truth_time)
    x = [i for i in range(time_len)]
    y = [affected_metrics_number_list[i] for i in range(time_len)]
    original_y = copy.deepcopy(y)
    y.sort(reverse=True)

    order_color = [t[1] for i in y for t in list(zip(original_y, color_list)) if i == t[0]]
    order_color = process_color(order_color)

    fig, ax = plt.subplots()  # 创建图实例
    plt.rcParams['figure.figsize'] = (15, 4)
    plt.rcParams['savefig.dpi'] = 300
    plt.rcParams['figure.dpi'] = 300
    plt.ylim([min(y), 300])
    ax.bar(x, y, color=order_color, width=1)
    # 画出 y=1 这条水平线
    plt.hlines(y=20, xmin=-50, xmax=1440, ls='--', color='black')
    plt.text(500, 28, 'solution length=20', ha='left', va='center')

    plt.ylabel('Abnormal Time Series Number (3-sigma)')
    plt.xlabel('TimeStamps')
    plt.show()
