import numpy as np
import matplotlib.pyplot as plt
# Though the following import is not directly being used, it is required
# for 3D projection to work
from mpl_toolkits.mplot3d import Axes3D

from sklearn.cluster import AgglomerativeClustering, KMeans
from sklearn.datasets import load_iris

def replace():
    for i in range(len(AggCluster)):
        if AggCluster[i] == 1:
            AggCluster[i] = 0
        elif AggCluster[i] == 0:
            AggCluster[i] = 1

dataset = load_iris()
X = dataset.data
Y = dataset.target


AggCluster = AgglomerativeClustering(n_clusters = 3).fit_predict(X)
KCluster= KMeans(n_clusters = 3).fit_predict(X)

print(KCluster)
replace()
print(KCluster)
'''print(AggCluster)
print(KCluster)
print(Y)'''

#print(X[:, 3],"ccccccc\n", X[:, 0],"cccccccccc\n", X[:, 2])
#print(X)

colors=["#0000FF", "#00FF00", "#FF0066"]
sepal_length = X[: , 0]
petal_lenght = X[: , 2]
petal_width = X[: , 3]



fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

plt.title("Real Classification")
for i in range(len(Y)):
    ax.scatter(petal_width[i], sepal_length[i], petal_lenght[i], color = colors[Y[i]])
ax.set_xlabel('Petal width')
ax.set_ylabel('Sepal length')
ax.set_zlabel('Petal length')
plt.show()


fig2 = plt.figure()
ax2 = fig2.add_subplot(111, projection='3d')
plt.title("K-Means Classification")
for i in range(len(Y)):
    ax2.scatter(petal_width[i], sepal_length[i], petal_lenght[i], color = colors[KCluster[i]])
ax2.set_xlabel('Petal width')
ax2.set_ylabel('Sepal length')
ax2.set_zlabel('Petal length')
plt.show()


fig3 = plt.figure()
ax3 = fig3.add_subplot(111, projection='3d')
plt.title("Agglomerative Classification")
for i in range(len(Y)):
    ax3.scatter(petal_width[i], sepal_length[i], petal_lenght[i], color = colors[AggCluster[i]])
ax3.set_xlabel('Petal width')
ax3.set_ylabel('Sepal length')
ax3.set_zlabel('Petal length')
plt.show()