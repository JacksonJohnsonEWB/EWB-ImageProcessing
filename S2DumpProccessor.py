import numpy as np
from matplotlib import pyplot as plt
import pandas as pd

def S2Proccess(DataFrame,filtervalue):
    DataFrame = DataFrame[['system:index','roiGreenPercent','roiCloudPercent']].copy()
    DataFrameFilter = DataFrame['roiCloudPercent']<=filtervalue
    DataFrameFiltered = DataFrame[DataFrameFilter]
    DataFrameFiltered['system:index'] = DataFrameFiltered['system:index'].str.slice(stop=8)
    DataFrameFiltered['system:index'] = pd.to_datetime(DataFrameFiltered['system:index'],infer_datetime_format=True)
    DataFrameFiltered['DayofYear'] = DataFrameFiltered['system:index'].dt.dayofyear
    return DataFrameFiltered

Raw2020 = pd.read_csv('2020-MetaData-Dump-October4.csv',sep=',')
Raw2019 = pd.read_csv('2019-MetaData-Dump.csv',sep=',')
Raw2018 = pd.read_csv('2018-MetaData-Dump.csv',sep=',')
Raw2017 = pd.read_csv('2017-MetaData-Dump.csv',sep=',')
Raw2016 = pd.read_csv('2016-MetaData-Dump.csv',sep=',')

Data2020 = S2Proccess(Raw2020,50)
Data2019 = S2Proccess(Raw2019,50)
Data2018 = S2Proccess(Raw2018,50)
Data2017 = S2Proccess(Raw2017,50)
Data2016 = S2Proccess(Raw2016,50)

#print(Data2020)
#print(Data2019)
#print(Data2018)
#print(Data2017)

fig, ax = plt.subplots(1,1)
ax.plot(Data2020['DayofYear'],Data2020['roiGreenPercent'],label = '2020')
ax.plot(Data2019['DayofYear'],Data2019['roiGreenPercent'],label = '2019')
ax.plot(Data2018['DayofYear'],Data2018['roiGreenPercent'],label = '2018')
ax.plot(Data2017['DayofYear'],Data2017['roiGreenPercent'],label = '2017')
ax.plot(Data2016['DayofYear'],Data2016['roiGreenPercent'],label = '2016')
ax.legend()
fig.suptitle('Vegetation Coverage vs Day of the Year')
ax.set_xlabel('Day of the Year')
ax.set_ylabel('Vegetation coverage (%)')
plt.show()
