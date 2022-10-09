import matplotlib.pyplot as plt
import numpy as np


def auto_label(rects,ax):
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height), # put the detail data
                    xy=(rect.get_x() + rect.get_width() / 2, height), # get the center location.
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')


def auto_text(rects,ax):
    for rect in rects:
        ax.text(rect.get_x(), rect.get_height(), rect.get_height(), ha='left', va='bottom')


def plot_result_for_a_method(method_name, labels, M, R):
    index = np.arange(len(labels))
    width = 0.2

    fig, ax = plt.subplots()

    rect1 = ax.bar(index - width / 2, M, width=width, label='M')
    rect2 = ax.bar(index + width / 2, R, width=width, label='R')

    ax.set_title('XX_'+str(method_name))
    ax.set_xticks(ticks=index)
    ax.set_xticklabels(labels)
    ax.set_ylabel('Values')

    ax.set_xlim(-0.5, 6)
    # auto_label(rect1)
    # auto_label(rect2)
    auto_text(rect1,ax)
    auto_text(rect2,ax)

    ax.legend()
    fig.tight_layout()
    plt.show()


if __name__ == '__main__':
    labels = ['AEO', 'BBO', 'GA', 'HS', 'PSO', 'BASIC']
    M_LOF = [0.72, 0.62, 0.72, 0.54, 0.64, 0.67]
    R_LOF = [0.29, 0.19, 0.24, 0.15, 0.32, 0.11]
    M_KNN = [0.73, 0.72, 0.70, 0.75, 0.73, 0.66]
    R_KNN = [0.23, 0.29, 0.29, 0.23, 0.26, 0.12]
    M_GMM = [0.76, 0.72, 0.75, 0.72, 0.76, 0.72]
    R_GMM = [0.32, 0.28, 0.28, 0.40, 0.46, 0.14]

    plot_result_for_a_method('LOF',labels,M_LOF,R_LOF)
    plot_result_for_a_method('KNN',labels,M_KNN,R_KNN)
    plot_result_for_a_method('GMM',labels,M_GMM,R_GMM)



