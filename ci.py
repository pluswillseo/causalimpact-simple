import pandas as pd
from causalimpact import CausalImpact
from pandas.core.indexing import convert_from_missing_indexer_tuple

data_1 = pd.read_csv('test.csv',
                  #usecols = [0,1],
                  header = 0,
                  encoding = 'utf-8-sig')

# 2020 data
data_2 = pd.read_csv('control - 2020.csv',
                          header = 0,
                          encoding = 'utf-8-sig')

# 2019 data
data_3 = pd.read_csv('control - 2019.csv',
                          header = 0,
                          encoding = 'utf-8-sig')

# 2018 data
data_4 = pd.read_csv('control - 2018.csv',
                          header = 0,
                          encoding = 'utf-8-sig')

# choose 1 inmarket control - try one category up, or similar product
data_5 = pd.read_csv('control - buttplugs.csv',
                          header = 0,
                          encoding = 'utf-8-sig')

# choose 1 cross market control - ideally a market that you know won't change
data_6 = pd.read_csv('control - aus.csv',
                          header = 0,
                          encoding = 'utf-8-sig')

def data_format(startDate, dataset, controlName):
    startDate = pd.to_datetime(startDate)
    dataset['Date formatted'] = pd.to_datetime(dataset['Date formatted'])
    dataset['index'] = dataset['Date formatted'] - startDate
    dataset['index'] = pd.to_numeric(dataset['index'])/86400000000000
    dataset = dataset.rename(columns={"Sessions": controlName})
    if controlName != 'test':
        dataset = dataset.drop(columns = 'Date formatted')
    return dataset

data_1 = data_format('2021-03-01', data_1, 'test')
data_2 = data_format('2020-03-02', data_2, '2020')
data_3 = data_format('2019-03-03', data_3, '2019')
data_4 = data_format('2018-03-04', data_4, '2018')
data_5 = data_format('2021-03-01', data_5, 'inmarket')
data_6 = data_format('2021-03-01', data_6, 'crossmarket')

data_bt = data_1.merge(data_2, how = "outer", on= 'index').merge(data_3, how = "outer", on= 'index').merge(data_4, how = "outer", on= 'index').merge(data_5, how = "outer", on= 'index').merge(data_6, how = "outer", on= 'index')

data_bt.fillna(0, inplace = True)

pre_period = [0,114] #dates before
post_period = [115, 152] #dates after

backTesting = CausalImpact(data_bt.drop(columns=['index','Date formatted']), pre_period, post_period)

print(backTesting.summary())
backTesting.plot()
print(backTesting.summary(output='report'))
print(backTesting.trained_model.summary())
'''
data_ci = data_1.merge(data_3, how = 'outer', on = 'index').merge(data_5, how = 'outer', on = 'index')
data_ci.fillna(0, inplace = True)

pre_period = [0,114] #dates before
post_period = [115, 152] #dates after

ci = CausalImpact(data_ci.drop(columns=['index','Date formatted']), pre_period, post_period)

print(ci.summary())
ci.plot()
'''