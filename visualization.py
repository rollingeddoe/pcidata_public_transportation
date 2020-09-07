import pandas as pd
import numpy as np
np.set_printoptions(suppress=True)
import os
import re
import datetime as dt
from matplotlib import pyplot  as plt
import seaborn as sns
sns.set_style("darkgrid",{'font.sans-serif':['simhei','Arial'],'grid.linestyle': '--'})

from aggregation import *
# The purpose of this .py file is to call the function directly with data_bus
# with the minimal amount of variables setting to get the visualization results



# plot to show the trend for a timeframe (such as month)
# barplot is for the income amount, and lineplot is for count of transactions
# mean field is for showing the plot with a specific mean as the horizontal axis, so that the positive and
# negative trend is obvious
# names is for y-fields and plot title
# xtick is name for x-axis
# reverse is for the range of barplot and pointplot, reverse=False: range for pointplot is larger than barplot

def trend_plot(data, names, means= None,xtick=np.arange(0, 24, 1), reverse = False):
    plt.rcParams.update({"font.size": 10,'axes.unicode_minus':False})
    fig, ax = plt.subplots(figsize=(20, 11))
    ax2 = ax.twinx()
    name1, name2, title = names
    if means:
        mean1, mean2 = means
        data[name1] = data['收入'] - mean1
        data[name2] = data['笔数'] - mean2

    sns.barplot(data=data, x=data.index, y=data[name1], ax=ax)
    sns.pointplot(data=data, x=data.index, y=data[name2], ax=ax2)

    if reverse:
        ax2.set_ylim(ax.get_ylim())
    else:
        ax.set_ylim(ax2.get_ylim())  # set second y axis to have the same limits as the first y axis


    ax.set_title(title)
    plt.xticks(xtick)
    ax2.grid("off")

    plt.show()

# lineplot for showing one set of data with automated range and mean

def lineplot(data, xlabel, ylabel, names=[], xtick=np.arange(0, 24, 1)):
    name, title = names
    plt.rcParams.update({"font.size": 20})
    plt.figure(figsize=(20, 9))
    sns.lineplot(data=data, x=data[xlabel], y=data[ylabel], label=name)
    plt.title(title, fontsize=20)  # for title
    plt.xlabel(xlabel, fontsize=15)  # label for x-axis
    plt.ylabel(ylabel, fontsize=15)  # label for y-axis
    ax2.grid("off")
    plt.xticks(xtick)
    plt.show()

# lineplot for comparing two sets of data

def lineplot_compare(data1, data2, xlabel, ylabel, names=[], xtick=np.arange(0, 24, 1)):
    name1, name2, title = names
    plt.rcParams.update({"font.size": 20})
    fig, ax = plt.subplots(figsize=(20, 9))
    ax2 = ax.twinx()
    sns.lineplot(data=data1, x=data1[xlabel], y=data1[ylabel], label=name1)
    sns.lineplot(data=data2, x=data2[xlabel], y=data2[ylabel], label=name2)
    ax.set_ylim(ax2.get_ylim()) # set second y axis to have the same limits as the first y axis
    # ax2.set_yticks(tick2)
    plt.title(str(name1 + '/' + name2 + title), fontsize=20)  # for title
    plt.xlabel(xlabel, fontsize=15)  # label for x-axis
    plt.ylabel(ylabel, fontsize=15)  # label for y-axis
    ax2.grid("off")
    plt.xticks(xtick)
    plt.show()

def anomaly_plot(data,name,if_sum=True,xtick = np.arange(0,24,1)):
    plt.figure(figsize=(20,9))
    if if_sum:
        y_data = data.收入
    else:
        y_data = data.笔数
    sns.pointplot(data = data, x=data.index, y=y_data, hue = data.日期)
    plt.xticks(xtick)
    plt.yticks(np.arange(min(y_data),max(y_data),(max(y_data)-min(y_data))//5))
    plt.title(name)
    plt.show()



# heatmap for aggregated income amount
# to generate heatmap we must turn data into pivot table using pivot_data()
def heatmap_weekhour(data, name, count = False):
    aggre = pivot_data(data, count)
    plt.figure(figsize=(4,4),dpi=200)
    ax = sns.heatmap(aggre,
                     #vmin=min(aggre.values), vmax=max(aggre.values),
                     annot=True,
                     annot_kws={'size':3, 'color':'blue'},
                     fmt='g',
                     linewidths=.5,
                     cmap="summer_r",
                     xticklabels=aggre.columns, yticklabels=aggre.index)
    ax.set(title = name)
    plt.show()

if __name__ == '__main__':
    print('Visualization plotting functions')



