import random
import numpy as np

from experiment.utils.datatools import get_observation_matrix, from_test_find_train_chromosome
from experiment.utils.detection_tools import choose_model


"""
Basic roulette wheel selection: O(N)
"""
def basic(fitness):
    '''
    Input: a list of N fitness values (list or tuple)
    Output: selected index
    '''
    sumFits = sum(fitness)
    # generate a random number
    rndPoint = random.uniform(0, sumFits)
    # calculate the index: O(N)
    accumulator = 0.0
    for ind, val in enumerate(fitness):
        accumulator += val
        if accumulator >= rndPoint:
            return ind

# 输入列信息，需要初始化的种群的规模,以及要编码的染色体的长度
# 输出包含染色体的列表，大小为size
def pop_initialization(tuple_dict, pop_size, chromosome_len):
    chromosome_list = []
    for i in range(pop_size):
        new_chromosome = random.sample(tuple_dict.keys(), chromosome_len)
        chromosome_list.append(new_chromosome)
    return chromosome_list


# 输入列信息，可能进行变异的染色体，每个gene位置变异的概率
def mutation(tuple_dict, chromosome, pro):
    new_chromosome = []
    gene_candidate = list(set(tuple_dict.keys()) - set(chromosome))
    for i in range(len(chromosome)):
        if random.random() < pro:
            new_gene = random.choice(gene_candidate)
            new_chromosome.append(new_gene)
            gene_candidate.remove(new_gene)
        else:
            new_chromosome.append(chromosome[i])
    return new_chromosome


# 输入是列信息，种群，以及每个个体变异概率
# 交叉：对每个个体，它将与剩余的个体中选取一个，将它们的列标作为集合，随机选取染色体长度的列标作为新个体
# 变异，在每个交叉之后的个体，都会经过变异函数
# 返回原始种群的数量，以及原始种群加上新个体的并集
def crossover_and_mutation(tuple_dict, pop, pro):
    spring_chromosome = []
    len_pop = len(pop)
    left_index = [i for i in range(len_pop)]
    for i in range(len_pop):
        left_index.remove(i)
        another_chromosome = pop[random.choice(left_index)]
        mix_list = list(set(pop[i]+another_chromosome))
        new_chromosome = random.sample(mix_list,len(another_chromosome))
        new_chromosome = mutation(tuple_dict,new_chromosome,pro)
        spring_chromosome.append(new_chromosome)
        left_index.append(i)
    total_raw = spring_chromosome+pop
    new_total_spring_chromosome = [i for n, i in enumerate(total_raw) if i not in total_raw[:n]]
    return len_pop, new_total_spring_chromosome

# 输入染色体,染色体是test_dict中的染色体，因此需要根据dict信息找到train的对应染色体
# 需要当前时间信息，训练矩阵(可以改版为训练好的模型)，待测矩阵(完整的,需要从中抽取出暂时观测到的数据),测试异常值所用的模型
# 输出该染色体在当前时刻的异常值
def fitness_function(train_dict,train_matrix, test_dict,test_matrix, test_chromosome, current_time, model):
    train_chromosome = from_test_find_train_chromosome(train_dict,test_dict,test_chromosome)
    new_train_matrix = get_observation_matrix(train_matrix,len(train_matrix)-1,train_chromosome)
    observation_matrix = get_observation_matrix(test_matrix,current_time,test_chromosome)
    x_train = np.array(new_train_matrix)
    x_test = np.array(observation_matrix)
    clf = choose_model(model)
    clf.fit(x_train)
    predicted = clf.decision_function(x_test)
    anomaly_score = predicted[current_time]
    return anomaly_score


# 输入是交配变异之后的pop，原始pop的大小，fitness需要的信息
# 选择方式暂时采取一种
# 输出是新pop，大小为原始pop大小
def selection(pop,original_size,train_dict,train_matrix, test_dict,test_matrix, current_time, model):
    output_pop = []
    fitness_list = []
    for i in range(len(pop)):
        new_fitness = fitness_function(train_dict,train_matrix,
                                       test_dict,test_matrix,
                                       pop[i],
                                       current_time,
                                       model)
        fitness_list.append(new_fitness)
    for i in range(original_size):
        selected_index = basic(fitness_list)
        output_pop.append(pop[selected_index])
    return output_pop


# def store_the_final_pop_tuple_string(tuple_string_dict, chromosomes):

