import pandas as pd

dfr = pd.read_csv('C:/Users/dell/Desktop/5012/radiant_heros.csv')
dfd = pd.read_csv('C:/Users/dell/Desktop/5012/dire_heros.csv')

# df_match
x = [1, 2, 3]
y = [0, 1, 2, 3]

dfr.drop(dfr.columns[x], axis=1, inplace=True)
dfd.drop(dfd.columns[y], axis=1, inplace=True)
df_match = pd.concat([dfr, dfd], axis=1)
df_match.columns = ['winner', 'radiant_hero_1', 'radiant_hero_2', 'radiant_hero_3', 'radiant_hero_4', 'radiant_hero_5',
                    'dire_hero_1', 'dire_hero_2', 'dire_hero_3', 'dire_hero_4', 'dire_hero_5']
# print(df_match.loc[df_match['winner']==1,['radiant_hero_1','radiant_hero_2'	,
#                         'radiant_hero_3','radiant_hero_4','radiant_hero_5']])
# columns=['hero_1','hero_2','hero_3','hero_4','hero_5']
# df_match=pd.concat([df_match, pd.DataFrame(columns=['hero_1','hero_2','hero_3','hero_4','hero_5'])])
print(df_match.iloc[0,][1:6])
df_match['hero_1'] = None
df_match['hero_2'] = None
df_match['hero_3'] = None
df_match['hero_4'] = None
df_match['hero_5'] = None
t = ['hero_1', 'hero_2', 'hero_3', 'hero_4', 'hero_5']
# df_lose
for i in range(len(t)):
    df_match[t[i]] = df_match.apply(lambda x: x[i + 1] if x[0] == -1 else x[int(i + 6)], axis=1)
# df_match
# for i in range(len(t)):
#     df_match[t[i]] = df_match.apply(lambda x: x[i + 1] if x[0] == 1 else x[int(i + 6)], axis=1)
df_match.drop(['winner',
               'radiant_hero_1', 'radiant_hero_2', 'radiant_hero_3', 'radiant_hero_4', 'radiant_hero_5',
               'dire_hero_1', 'dire_hero_2', 'dire_hero_3', 'dire_hero_4', 'dire_hero_5'], axis=1, inplace=True)
df_match.to_csv('C:/Users/dell/Desktop/5012/df_lose.csv', index=None)
