from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import numpy as np

iris = load_iris()

df = pd.DataFrame(iris.data, columns=iris.feature_names)

# add column, 75% train, 25% test.
df['is_train'] = np.random.uniform(0, 1, len(df)) <= 0.75

# add label. target:[0,0,1,1,2,2,......] , target_names:[name1, name2, name3,....]
df['species'] = pd.Categorical.from_codes(iris.target, iris.target_names)

df['label'] = iris.target

train, test = df[df['is_train'] == True], df[df['is_train'] == False]

# last 2 column is is_train and species
features = df.columns[:4]

# create random forest
clf = RandomForestClassifier(n_jobs=2)

# transfer label to 0,1,2,3.....
train_y, _ = pd.factorize(train['species'])

test_y, _ = pd.factorize(test['species'])

clf.fit(train[features], train_y)

preds = clf.predict(test[features])

pred_name = iris.target_names[preds]

#compare test_y and preds
accuracy = sum([1 for i in range(len(preds)) if preds[i] == test_y[i]]) / len(test_y)
print(accuracy)

print(pd.crosstab(test['species'], pred_name, rownames=['actual'], colnames=['preds']))
