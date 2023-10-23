from sklearn import svm
import joblib
import json

with open('freq.json', 'r', encoding='utf-8') as f:
    d = json.load(f)
    train = d[0]
    test = d[1]

train_X = train['freqs']
train_y = train['labels']

clf= svm.SVC()
clf.fit(train_X,train_y)

# pred = clf.predict(test['freqs'])
# print(f'predict: {pred}')
joblib.dump(clf,'freq.pkl')
print('ok')
