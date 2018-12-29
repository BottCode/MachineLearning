import csv
from sklearn import datasets
import numpy as np
from sklearn.svm import SVR
import matplotlib.pyplot as plt

data = datasets.load_boston(return_X_y = True)
X = data[0].tolist()
Y = data[1].tolist()

svr_rbf = SVR(kernel='rbf', C=1000, gamma=0.1)
svr_lin = SVR(kernel='linear', C=1000)
svr_lin_low_C = SVR(kernel='linear', C=1)
svr_pol_2 = SVR(kernel='poly', C=1000, degree=2)
svr_pol_3 = SVR(kernel='poly', C=1000, degree=3)

y_lin = svr_lin.fit(X, Y).predict(X)
y_lin_low_C = svr_lin_low_C.fit(X, Y).predict(X)
y_rbf = svr_rbf.fit(X, Y).predict(X)
y_pol_2 = svr_pol_2.fit(X, Y).predict(X)

plt.title("LINEAR with C = 1000")
plt.plot(X,Y,'ro')
plt.plot(X,y_lin,'go')
plt.show()

plt.clf()
plt.title("Linear with C = 1")
plt.plot(X,Y,'ro')
plt.plot(X,y_lin_low_C,'go')
plt.show()

plt.clf()
plt.title("rbf")
plt.plot(X,Y,'ro')
plt.plot(X,y_rbf,'go')
plt.show()

plt.clf()
plt.title("Polynomial degree = 2")
plt.plot(X,Y,'ro')
plt.plot(X,y_pol_2,'go')
plt.show()
