from sklearn.linear_model import Ridge 
from sklearn.datasets import load_diabetes
import matplotlib.pyplot as plt
from sklearn.preprocessing import PolynomialFeatures

CONST_ALPHAS = [0, 0.1, 1, 10, 100]

# retrieve diabetes data
data_X, target_Y = load_diabetes(True)

# split diabetes set into training set and validation test
lenset = len(data_X)
split_point = int(lenset / 2)
training_set = {
    "x": data_X[0 : split_point - 1],
    "y": target_Y[0 : split_point - 1]
}

validation_set = {
    "x": data_X[split_point - 1 : lenset - 1],
    "y": target_Y[split_point - 1 : lenset -1]
}

model_scores = []

for alpha_value in CONST_ALPHAS:
    ridge_model = Ridge(alpha_value)
    ridge_model.fit(training_set["x"], training_set["y"])
    score = ridge_model.score(validation_set["x"],validation_set["y"])
    model_scores.append(score)

plt.plot(CONST_ALPHAS,model_scores)
plt.show()

