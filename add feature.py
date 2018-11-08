import pandas as pd
from sklearn.metrics import accuracy_score
import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split
import os

train = pd.read_csv('nTrain.csv')
target = 'winner'
final_test = pd.read_csv('nTest.csv')

hero_columns = [x for x in train.columns if x not in ['winner', 'cluster_id', 'game_mode', 'game_type']]
X = train[hero_columns]
y = train[['winner']]

# ===============================================================
def Add_Feature_Hero_Advantage(XX):
    X = XX[hero_columns]

    def create_dict(path):
        dict = {}
        relation_df = pd.read_csv(path, index_col=['heros'])
        for i in relation_df.index.values:
            key = i
            value = {'overcome': relation_df.overcome.loc[key], 'be_overcome': relation_df.be_overcome.loc[key]}
            dict[key] = value
        return dict

    def get_advantage_value(df, X):

        v = 0
        list1 = []
        list2 = []

        for index, hero in enumerate(df):
            if hero == 1:
                list1.append(index)
            if hero == -1:
                list2.append(index)
        list_radiant = X.columns.values[list1]  # radiant是1吧？？？
        list_dire = X.columns.values[list2]

        for i in list_radiant:
            if dict[i]['overcome'] in list_dire:
                v += 1
            if dict[i]['be_overcome'] in list_dire:
                v -= 1
        for i in list_dire:
            if dict[i]['overcome'] in list_radiant:
                v -= 1
            if dict[i]['be_overcome'] in list_radiant:
                v += 1
        return v

    def get_new_column(X):
        new_feature_col = []
        for row in range(len(X)):
            df = X.iloc[row]
            v = get_advantage_value(df, X)
            new_feature_col.append(v)
        return new_feature_col

    path = 'C:/Users/jiang/Desktop/overcome_data.csv'
    dict = create_dict(path)
    new_feature = get_new_column(X)
    XX['advantage_value'] = new_feature

    return XX

# ====================================================

def Add_Feature_Combo_Advantage(XX):
    X = XX[hero_columns]

    BEST_COMBO = [['keep_of_the_light', 'axe'], ['tusk', 'techies'], ['tiny', 'techies'], ['dazzle', 'huskar'],
                  ['bane', 'mirana', 'pudge'], ['tusk', 'legion_ commander'], ['viper', 'venomancer'],
                  ['spirit_breaker', 'life_stealer'], ['axe', 'shadow_demon', 'dazzle'], ['dark_seer', 'broodmother']]

    def creat_combo_col(combo, X):

        # 对每个combo列
        INDEX_L = []

        for row in range(len(X)):
            # 对行

            df = X.iloc[row]

            # 每一行计算 两方lane
            list1 = []
            list2 = []

            for index, hero in enumerate(df):
                if hero == 1:
                    list1.append(index)
                if hero == -1:
                    list2.append(index)
            list_radiant = X.columns.values[list1]
            list_dire = X.columns.values[list2]

            # 每行产生 index
            INDEX = 0

            if set(combo).issubset(list_radiant):
                INDEX = 1
            if set(combo).issubset(list_dire):
                INDEX = -1

            INDEX_L.append(INDEX)

        col_name = str(combo)
        XX[col_name] = INDEX_L

    for combo in BEST_COMBO:
        creat_combo_col(combo, X)

    return XX

# =======================================================
X = Add_Feature_Combo_Advantage(X)
X = Add_Feature_Hero_Advantage(X)
# X.to_csv('classifer_TrainData.csv')
# X = pd.read_csv('classifer_TrainData.csv',index_col = 0)

# =======================================================

y = y.replace(-1, 0)

x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.33,random_state=22)


def acc(model):
    y_pred = model.predict(x_test)
    pred_score = accuracy_score(y_pred, y_test)
    print('accuracy')
    print(pred_score)


from sklearn.linear_model import LogisticRegression

clf = LogisticRegression(penalty='l2')
clf.fit(x_train, y_train)
acc(clf)

print(X.shape)