import pandas as pd
import numpy as np
import sklearn
from sklearn import linear_model
from sklearn.utils import shuffle
import os
import sys
import matplotlib.pyplot as pyplot
import pickle
from matplotlib import style


#print()
#print(sys.argv[0])
#print(os.path.dirname(sys.argv[0]))
#print()

os.chdir(os.path.dirname(sys.argv[0]))

'''
Student Performance Data Set is from 
https://archive.ics.uci.edu/ml/datasets/Student+Performance
'''

data = pd.read_csv("student-mat.csv", sep=";")
#print(data.head())

data = data[['G1', 'G2', 'G3', 'studytime', 'failures', 'absences']]

#print(data.head())

predict = 'G3'

X = np.array(data.drop([predict], axis=1))
y = np.array(data[predict])
x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(
    X, y, test_size=0.1)

""" 
best = 0

for _ in range(30):
    x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(X, y, test_size=0.1)


    linear = linear_model.LinearRegression()

    linear.fit(x_train, y_train)
    acc = linear.score(x_test, y_test)
    print(acc)

    if acc > best:
        best = acc
        with open('studentmodel.pickle', 'wb') as f:
            pickle.dump(linear, f)
 """

pickle_in = open('studentmodel.pickle', 'rb')
linear = pickle.load(pickle_in)

print('Coefficient: \n', linear.coef_)
print('Intercept: \n', linear.intercept_)
print()

predictions = linear.predict(x_test)

for x in range(len(predictions)):
    print(predictions[x], x_test[x], y_test[x])

p = 'absences'
#p = 'G1'
style.use('ggplot')
pyplot.scatter(data[p], data['G3'])
pyplot.xlabel(p)
pyplot.ylabel('Final Grade')
pyplot.show()
