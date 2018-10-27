from sklearn.linear_model import Ridge 
from sklearn.datasets import load_diabetes
import matplotlib.pyplot as plt
from sklearn.preprocessing import PolynomialFeatures
from collections import defaultdict

# this two array has got the same length
CONST_ALPHAS = [0,1e-15, 1e-10, 1e-8, 1e-4, 1e-3,1e-2, 1, 5, 10, 20]

# retrieve diabetes data
data_X, target_Y = load_diabetes(True)

# split diabetes set into training set and validation test
lenset = len(data_X)
split_point = 2 * int(lenset / 3)
training_set = {
    "x": data_X[0 : split_point],
    "y": target_Y[0 : split_point]
}

validation_set = {
    "x": data_X[split_point + 1 : lenset - 1],
    "y": target_Y[split_point + 1 : lenset -1]
}

pipelines = []
linear_model_scores = []

# compute ridge linear model for each alpha in CONST_ALPHA
for alpha_value in CONST_ALPHAS:
    linear_model = Ridge(alpha = alpha_value)
    linear_model.fit(training_set["x"], training_set["y"])
    linear_score = linear_model.score(validation_set["x"],validation_set["y"])
    linear_model_scores.append(linear_score)

plt.title("Ridge regression")
plt.xlabel("Alphas values")
plt.ylabel("Score")
plt.plot(CONST_ALPHAS, linear_model_scores)
plt.show()
