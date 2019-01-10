import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import plotly.plotly as py
import plotly.tools as tls
from sklearn.cluster import AgglomerativeClustering, KMeans
from sklearn.datasets import load_iris

def mostFrequent():
    i = 0
    most_frequent = []
    frequency_dict = {
        0: 0,
        1: 0,
        2: 0
    }
    for i in range(50):
        frequency_dict[KCluster[i]] = frequency_dict[KCluster[i]] + 1
    max_key = max(frequency_dict, key=lambda k: frequency_dict[k])
    most_frequent.append(max_key)
    # reset
    frequency_dict[0], frequency_dict[1], frequency_dict[2] = 0, 0, 0

    for i in range(50,100):
        frequency_dict[KCluster[i]] = frequency_dict[KCluster[i]] + 1
    max_key = max(frequency_dict, key=lambda k: frequency_dict[k])
    most_frequent.append(max_key)
    # reset
    frequency_dict[0], frequency_dict[1], frequency_dict[2] = 0, 0, 0
    
    for i in range(100,len(KCluster)):
        frequency_dict[KCluster[i]] = frequency_dict[KCluster[i]] + 1
    max_key = max(frequency_dict, key=lambda k: frequency_dict[k])
    most_frequent.append(max_key)

    return most_frequent

def replace():
    for i in range(len(AggCluster)):
        if AggCluster[i] == 1:
            AggCluster[i] = 0
        elif AggCluster[i] == 0:
            AggCluster[i] = 1
        
    clusterKmeans = mostFrequent()
    for i in range(len(KCluster)):
        if KCluster[i] == clusterKmeans[0]:
            KCluster[i] = 0
        elif KCluster[i] == clusterKmeans[1]:
            KCluster[i] = 1
        else:
            KCluster[i] = 2

        
def errors(data):
    num_of_misclassified, wrong_k1, wrong_k2, wrong_k3 = 0, 0, 0, 0
    for i in range(len(data)):
        if Y[i] != data[i]:
            num_of_misclassified = num_of_misclassified + 1
            if i < 50:
                wrong_k1 = wrong_k1 + 1
            elif i < 100:
                wrong_k2 = wrong_k2 + 1
            else:
                wrong_k3 = wrong_k3 + 1
            
    
    return [num_of_misclassified, wrong_k1/50, wrong_k2/50, wrong_k3/50]

def printErr(err_data):
    return "Misclassified points: " + str(err_data[0]) + "\n Error Percentual: (#data in the wrong cluster) / (# cluster size): \n Cluster 0: " + str(err_data[1]*100) + "%\n Cluster 1: " + str(err_data[2]*100) + "%\n Cluster 2: " + str(err_data[3]*100) + "%"

dataset = load_iris()
X = dataset.data
Y = dataset.target

AggCluster = AgglomerativeClustering(n_clusters = 3).fit_predict(X)
AggComplete = AgglomerativeClustering(n_clusters = 3, linkage = "complete").fit_predict(X)
AggAverage = AgglomerativeClustering(n_clusters = 3, linkage = "average").fit_predict(X)
AggSingle = AgglomerativeClustering(n_clusters = 3, linkage = "single").fit_predict(X)
KCluster= KMeans(n_clusters = 3).fit_predict(X)

replace()
compl_err = errors(AggComplete)
agg_err = errors(AggCluster)
avg_err = errors(AggAverage)
sng_err = errors(AggSingle)
k_err = errors(KCluster)

print("Ward Aggregative:\n",printErr(agg_err))
print("Complete Aggregative:\n",printErr(compl_err))
print("Average Aggregative:\n",printErr(avg_err))
print("Single Aggregative:\n",printErr(sng_err))
print("K-Means Aggregative:\n",printErr(k_err))

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