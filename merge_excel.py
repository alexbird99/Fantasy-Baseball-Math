#
# 1. merge and clean data to a file for Tableau
# 2. Benford's Law testing
#
import os
import pandas as pd
import numpy as np
import benfordslaw
import benfordslaw_demo

# read all xls files and merge
path = os.getcwd() + "\\xls\\"
files = os.listdir(path)
files_xls = [f for f in files if f[-3:] == 'xls']

df = pd.DataFrame()

for f in files_xls:
    data = pd.read_excel(
        path + f,
        names=['鄉別', '宋楚瑜', '韓國瑜', '蔡英文', '有效票數', '無效票數',
               '投票數', '已領未投票數', '發出票數', '用餘票數', '選舉人數', '投票率'],
        thousands=','
    )
    # remove top five rows
    data = data.drop(data.index[0:5], axis=0)

    # add county name column data from file name
    # todo: add county name from file content
    countyName = f[19:22]
    data.insert(0, '縣別', countyName)
    df = df.append(data)


# convert to numeric type
df.iloc[:, 2:] = df.iloc[:, 2:].apply(pd.to_numeric)

# remove first space
df['鄉別'] = df['鄉別'].str[1:]

# check data completion
df['韓國瑜'].sum()  # 5522119
df['蔡英文'].sum()  # 8170231

# add percent column
df['韓國瑜得票率'] = df['韓國瑜'] / df['投票數'] * 100
df['蔡英文得票率'] = df['蔡英文'] / df['投票數'] * 100
df['宋楚瑜得票率'] = df['宋楚瑜'] / df['投票數'] * 100

# output

# df.reset_index(drop=True, inplace=True)
output_path = os.getcwd() + "\\output\\merged_votes.xlsx"
df.to_excel(output_path, index=False)


# Benford's Law
data = df['韓國瑜']
# data = benfordslaw_demo.get_random_data()

benford_table = benfordslaw.calculate(data)
benfordslaw_demo.print_as_table(benford_table)
# benfordslaw_demo.print_as_graph(benford_table)
