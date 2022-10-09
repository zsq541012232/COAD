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


def plot_result_for_all_method(labels, M, R):
    index = np.arange(len(labels))
    width = 0.25

    fig, ax = plt.subplots(dpi=300,figsize=(10,4))

    rect1 = ax.bar(index - width / 2, M, width=width, label='M')
    rect2 = ax.bar(index + width / 2, R, width=width, label='R')

    ax.set_title('Preliminary Detection')
    ax.set_xticks(ticks=index)
    ax.set_xticklabels(labels)
    ax.set_ylabel('Values')

    ax.set_xlim(-0.5, 11)
    # auto_label(rect1)
    # auto_label(rect2)
    auto_text(rect1,ax)
    auto_text(rect2,ax)

    ax.legend(loc='upper right')
    fig.tight_layout()
    plt.show()


if __name__ == '__main__':
    labels = ['AutoEncoder', 'COPOD', 'DeepSVDD', 'GMM', 'IForest', 'KDE', 'KNN', 'LOF', 'OCSVM', 'PCA', 'VAE']
    M = [0.71, 0.63, 0.63, 0.72, 0.61, 0.66, 0.66, 0.67, 0.63, 0.71, 0.70]
    R = [0.05, 0.08, 0.11, 0.14, 0.18, 0.17, 0.12, 0.11, 0.03, 0.05, 0.05]

    plot_result_for_all_method(labels,M,R)



