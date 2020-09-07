import pandas as pd
import numpy as np
np.set_printoptions(suppress=True)
import os
import re
import datetime as dt
from matplotlib import pyplot  as plt
import seaborn as sns
sns.set_style("darkgrid",{'font.sans-serif':['simhei','Arial'],'grid.linestyle': '--'})


# The purpose of this .py file is to call the function directly with data_bus

def get_chinese(code):
    pattern="[\u4e00-\u9fa5]+"
    regex = re.compile(pattern)
    result = regex.findall(code.decode())
    if result:
        return result
    else:
        return [None]


def all_travel(new_user, old_user):
    new = get_aggregated(new_user, by='date')
    old = get_aggregated(old_user, by='date')
    d = {'新用户笔数': new['笔数'], '老用户笔数': old['笔数'], '新用户收入': new['收入'], '老用户收入': old['收入'], '日期': old['日期']}
    df = pd.DataFrame(data=d)
    df.set_index('日期',inplace = True)
    return df

# aggregate data into sum and count fields by date or hour
def get_aggregated(data, by = 'date'):
    if by == 'date':
        agg = data.groupby([data.发生时间.dt.date]).agg({'收入金额（+元）': ['sum','count']},)
        agg.columns = ['收入', '笔数']
        agg.index.set_names(['日期'], inplace=True)
        agg.reset_index(inplace=True)
    elif by == 'hour':
        agg = data.groupby(data.发生时间.dt.hour).agg(收入=pd.NamedAgg('收入金额（+元）', aggfunc='sum'),
                                                  笔数=pd.NamedAgg('收入金额（+元）', aggfunc='count'))
    elif by == 'date_hour':
        agg = data.groupby([data.发生时间.dt.date, data.发生时间.dt.hour]).agg(收入=pd.NamedAgg('收入金额（+元）', aggfunc='sum'),
                                                                       笔数=pd.NamedAgg('收入金额（+元）', aggfunc='count'))
        agg.index.set_names(['日期', '小时'], inplace=True)
        agg.reset_index(inplace=True)
    elif by == 'date_hour_weekday':
        agg = data.groupby([data.发生时间.dt.weekday, data.发生时间.dt.date, data.发生时间.dt.hour]).agg(收入=pd.NamedAgg('收入金额（+元）', aggfunc='sum'),
                                                                       笔数=pd.NamedAgg('收入金额（+元）', aggfunc='count'))
        agg.index.set_names(['星期日', '日期', '小时'], inplace=True)
        agg.reset_index(inplace=True)

    return agg

# get all data that matches a specific weekday/month/date/hour
def get_chunk(data, value, field='weekday'):
    if field == 'weekday':
        result = data[data.发生时间.dt.weekday == value]
    elif field == 'month':
        result = data[data.发生时间.dt.month == value]
    elif field == 'date':
        result = data[data.发生时间.dt.date == value]
    elif field == 'hour':
        result = data[data.发生时间.dt.hour == value]

    return result



# generate pivot table for heatmap
def pivot_data(data,count=False):
    if count:
        field = '笔数'
        agg = data.groupby([data.发生时间.dt.weekday, data.发生时间.dt.date, data.发生时间.dt.hour]).agg(
            笔数=pd.NamedAgg('收入金额（+元）', aggfunc='count'))
    else:
        field = '收入'
        agg = data.groupby([data.发生时间.dt.weekday, data.发生时间.dt.date, data.发生时间.dt.hour]).agg(
            收入=pd.NamedAgg('收入金额（+元）', aggfunc='sum'))
    agg.index.set_names(['星期日', '日期', '小时'], inplace=True)
    agg.reset_index(inplace=True)
    agg = agg.groupby(['星期日', '小时']).agg(平均值 = pd.NamedAgg(field, aggfunc = 'mean'))
    agg = agg.reset_index()
    weekdays = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期天"]
    agg.星期日.replace(agg.星期日.unique(),weekdays,inplace = True)
    agg = agg.pivot(index='小时', columns='星期日', values='平均值')
    agg = agg[weekdays]
    return agg



if __name__ == '__main__':
    print('Aggregation file')