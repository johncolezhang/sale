from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
import xgboost as xgb
import matplotlib.pyplot as plt


# read in the iris data
iris = load_iris()

X = iris.data
y = iris.target
feature = list(map(lambda x: x.split(' (')[0],  iris.feature_names))

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)


params = {
    'booster': 'gbtree',
    'objective': 'multi:softmax',
    'num_class': 3,
    'gamma': 0.1,
    'max_depth': 6,
    'lambda': 2,
    'subsample': 0.7,
    'colsample_bytree': 0.7,
    'min_child_weight': 3,
    'silent': 1,
    'eta': 0.1,
    'seed': 1000,
    'nthread': 4,
}


dtrain = xgb.DMatrix(data=X_train, label=y_train, feature_names=feature)
num_rounds = 500
model = xgb.train(params, dtrain, num_rounds)



dtest = xgb.DMatrix(data=X_test, feature_names=feature)
ans = model.predict(dtest)

print("accuracy", sum([1 for i in range(len(y_test)) if ans[i] == y_test[i]]) / len(y_test))
xgb.plot_importance(model)
plt.show()