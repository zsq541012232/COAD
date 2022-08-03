from experiment.utils.datatools import search_insert
import numpy as np

min_elapse = 10


# criterion_list是ground_truth里面的时间点，detect_result是检测出的异常时间点
# 这个评价函数会以ground_truth中的时间点为依据进行评分
# 对于每个真实发生故障的时间点，往后time_elapse的时间内认为是故障都算正确
# 如果有多个检测结果在这个允许的时间段内，则取他们的平均值
# 剩下的错误检测结果将会额外剔除，作为误报率返回百分比
# 对于检测的结果，返回平均检测时延
def judge_time_point(criterion_list, detect_result, time_elapse):
    # 首先对criterion进行排序
    criterion_list = sorted(criterion_list)
    detect_result = sorted(detect_result)
    result_elapse = []  # 存放检测正确的结果的时延，如果不是正确检测，就不放
    false_num = 0
    right_set = set()
    # 对于每一个在检测结果中的值进行检查，如果符合要求，就计算检测时延并且把时延放入result_elapse中,并标记相对应的异常被检测到了
    # 如果不满足要求，就让误报个数加一
    # 如果正确，还要记录这个异常被检测到了，并且最后返回检测到到异常占总异常百分比
    for index, value in enumerate(detect_result):
        if value in criterion_list:
            result_elapse.append(0)
            right_set.add(value)
        else:
            searched_index = search_insert(criterion_list, value)
            if searched_index == 0:
                false_num += 1
            elif value - criterion_list[searched_index - 1] > time_elapse:
                false_num += 1
            else:
                result_elapse.append(value - criterion_list[searched_index - 1])
                right_set.add(criterion_list[searched_index - 1])
    if len(result_elapse) == 0:
        return None, None, None
    else:
        avg_elapse = sum(result_elapse) / len(result_elapse)
        recall = len(right_set) / len(criterion_list)
        precision = 1 - false_num / len(detect_result)
        return avg_elapse, precision, recall


# 输入是每个时间点的异常值
# 根据异常值判断每个时间是否为异常点
# 输出是认为是异常点的时间下标
def judge_detect_result_using_3sigma(decision_scores):
    detect_result = []
    score_mean = np.mean(decision_scores)
    score_dev = np.std(decision_scores)
    score_upper = score_mean + 3 * score_dev
    score_lower = score_mean - 3 * score_dev
    for index, score in enumerate(decision_scores):
        if not score_lower <= score <= score_upper:
            detect_result.append(index)
    return detect_result


def get_n_time(anomaly_time_point_ground_truth, time_len):
    whole_time_point = [i for i in range(0, time_len)]
    return_list = list(set(whole_time_point).difference(set(anomaly_time_point_ground_truth)))
    return return_list


# 根据min_elapse min内的positive来计算
def find_p_by_threshold(anomaly_scores_at_time, current_threshold):
    return_list = []
    for index, value in enumerate(anomaly_scores_at_time):
        if value >= current_threshold:
            return_list.append(index)
    return return_list


def get_p_time_intervals(anomaly_time_point_ground_truth):
    return_list = []
    for index, value in enumerate(anomaly_time_point_ground_truth):
        interval = []
        for j in range(min_elapse + 1):
            interval.append(value + j)
        return_list.append(interval)
    return return_list


def get_detected_intervals(p_time_intervals, p_time_detected):
    return_list = []
    for index_d, value_d in enumerate(p_time_detected):
        flag = 0
        for index_g, value_i in enumerate(p_time_intervals):
            if value_d in value_i:
                return_list.append(value_i)
                flag = 1
        if flag == 0:
            interval = [(value_d-j) for j in range(min_elapse+1)]
            return_list.append(interval)
    return return_list


def get_interval_time(intervals):
    return_set = set()
    for index, value_i in enumerate(intervals):
        return_set = return_set.union(set(value_i))
    return list(return_set)


def get_current_fpr_and_tpr(anomaly_time_point_ground_truth, anomaly_scores_at_time, current_threshold):
    p_time_intervals = get_p_time_intervals(anomaly_time_point_ground_truth)  # true positive , true anomaly
    p_time_detected = find_p_by_threshold(anomaly_scores_at_time,
                                          current_threshold)  # detected positive, detected anomaly
    p_time_detected_intervals = get_detected_intervals(p_time_intervals, p_time_detected)
    dp_time = get_interval_time(p_time_detected_intervals)
    p_time = get_interval_time(p_time_intervals)
    n_time = get_n_time(p_time, len(anomaly_scores_at_time))  # ture negative, ture normal time

    tp = list(set(p_time).intersection(set(dp_time)))
    fp = list(set(n_time).intersection(set(dp_time)))

    tpr = len(tp) / len(p_time)
    fpr = len(fp) / len(n_time)

    return fpr, tpr


def get_fpr_and_tpr(anomaly_time_point_ground_truth, anomaly_scores_at_time):
    fprs = []
    tprs = []
    score_sorted = sorted(anomaly_scores_at_time)
    for current_threshold in score_sorted:
        current_fpr, current_tpr = get_current_fpr_and_tpr(anomaly_time_point_ground_truth, anomaly_scores_at_time,
                                                           current_threshold)
        fprs.append(current_fpr)
        tprs.append(current_tpr)
    return sorted(fprs), sorted(tprs)


def calculate_auc(anomaly_time_point_ground_truth, anomaly_scores_at_time):
    fprs, tprs = get_fpr_and_tpr(anomaly_time_point_ground_truth, anomaly_scores_at_time)
    auc = 0
    pre_fpr = 0
    pre_tpr = 0
    for index, fpr_value in enumerate(fprs):
        if index == 0:
            pass
        else:
            x_step = fprs[index] - pre_fpr
            area_current = ((tprs[index] + pre_tpr) * x_step) / 2
            auc += area_current

            pre_fpr = fprs[index]
            pre_tpr = tprs[index]
    return auc


def get_current_pre_and_recall(anomaly_time_point_ground_truth, anomaly_scores_at_time, threshold):
    recall_list = []
    pre_list = []
    p_time_detected = find_p_by_threshold(anomaly_scores_at_time,threshold)
    for index, detected_time in enumerate(p_time_detected):
        for index_dot, interval_start in enumerate(anomaly_time_point_ground_truth):
            if interval_start<=detected_time<=interval_start+min_elapse:
                recall_list.append(index_dot)
                pre_list.append(index)
    pre_list = list(set(pre_list))
    recall_list = list(set(recall_list))

    pre = len(pre_list)/len(p_time_detected)
    recall = len(recall_list)/len(anomaly_time_point_ground_truth)

    return pre, recall


def get_pre_recall_f1(anomaly_time_point_ground_truth, anomaly_scores_at_time, percent_x):
    pre_y = []
    recall_y = []
    f1_y = []
    max_score = max(anomaly_scores_at_time)
    min_score = min(anomaly_scores_at_time)
    span_score = max_score - min_score
    for index, current_percent in enumerate(percent_x):
        threshold = max_score - current_percent * span_score
        pre, recall = get_current_pre_and_recall(anomaly_time_point_ground_truth,
                                                 anomaly_scores_at_time,
                                                 threshold)
        if pre + recall == 0:
            f1 = 0
        else:
            f1 = 2*pre*recall/(pre+recall)
        pre_y.append(pre)
        recall_y.append(recall)
        f1_y.append(f1)

    return pre_y, recall_y, f1_y


