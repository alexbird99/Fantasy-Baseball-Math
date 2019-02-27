import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def convert_percent(x):
    return float(x.strip('%')) / 100


def find_two_consecutive_season(df, s1, s2, col):
    ls1 = []
    ls2 = []
    df1 = df[df['Season'] == s1]
    df2 = df[df['Season'] == s2]

    if (df1.empty | df2.empty):
        return [], []

    for index, row in df1.iterrows():
        # find rows with same playerid in season2
        same_id_df = df2.loc[df2['playerid'] == row['playerid']]
        if not same_id_df.empty:
            ls1.append(row[col])
            # pick first row of dataframe
            ls2.append(same_id_df[col].iloc[0])

    return ls1, ls2


def draw(df, col):
    s1, s2 = collect_data(df, col)
    plt.scatter(s1, s2)
    plt.title(str(len(s1))+' points')
    plt.xlabel('season ' + col)
    plt.ylabel('season+1 '+col)
    plt.show()


def calculate_correlation(s1, s2):
    return np.corrcoef(s1, s2)[0][1]


def collect_data(df, col):
    seasons = sorted(pd.unique(df['Season']))
    s1 = []
    s2 = []
    for s in seasons:
        ls1, ls2 = find_two_consecutive_season(df, s, s + 1, col)
        s1.extend(ls1)
        s2.extend(ls2)
    return s1, s2


def calculate_all_cols(df, cols):
    result = []
    for col in cols:
        s1, s2 = collect_data(df, col)
        result.append(calculate_correlation(s1, s2))
    # combine and use string representing float with two decimals
    return (np.column_stack((cols, ['%.2f' % elem for elem in result])))


# df = pd.read_csv(
#     'csv/pitcher.csv',
#     converters={
#         'LOB%': convert_percent,
#         'LD%': convert_percent,
#         'GB%': convert_percent,
#         'FB%': convert_percent,
#         'IFFB%': convert_percent,
#         'HR/FB': convert_percent,
#         'IFH%': convert_percent,
#         'BUH%': convert_percent,
#         'O-Swing%': convert_percent,
#         'Z-Swing%': convert_percent,
#         'Swing%': convert_percent,
#         'O-Contact%': convert_percent,
#         'Z-Contact%': convert_percent,
#         'Contact%': convert_percent,
#         'Zone%': convert_percent,
#         'F-Strike%': convert_percent,
#         'SwStr%': convert_percent,
#         'K%': convert_percent,
#         'BB%': convert_percent,
#         'K-BB%': convert_percent,
#         'Pull%': convert_percent,
#         'Cent%': convert_percent,
#         'Oppo%': convert_percent,
#         'Soft%': convert_percent,
#         'Med%': convert_percent,
#         'Hard%': convert_percent
#     }
# )

df = pd.read_csv(
    'csv/batter.csv',
    converters={
        'BB%': convert_percent,
        'K%': convert_percent,
        'LD%': convert_percent,
        'GB%': convert_percent,
        'FB%': convert_percent,
        'IFFB%': convert_percent,
        'HR/FB': convert_percent,
        'IFH%': convert_percent,
        'BUH%': convert_percent,
        'O-Swing%': convert_percent,
        'Z-Swing%': convert_percent,
        'Swing%': convert_percent,
        'O-Contact%': convert_percent,
        'Z-Contact%': convert_percent,
        'Contact%': convert_percent,
        'Zone%': convert_percent,
        'F-Strike%': convert_percent,
        'SwStr%': convert_percent,                     
        'Pull%': convert_percent,
        'Cent%': convert_percent,
        'Oppo%': convert_percent,
        'Soft%': convert_percent,
        'Med%': convert_percent,
        'Hard%': convert_percent
    }
)

# df.info()
df = df.drop(['Name', 'Team'], 1)

# cols = list(df.columns)
# cols.remove('Season')
# cols.remove('playerid')
cols = ['GB%', 'LD%', 'K%']

# draw(df, 'BABIP')

result = calculate_all_cols(df, cols)

for x in range(len(result)):
    print(*result[x])
