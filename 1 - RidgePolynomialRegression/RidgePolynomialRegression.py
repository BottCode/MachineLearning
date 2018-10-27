from sklearn.linear_model import Ridge 
from sklearn.datasets import load_diabetes
import matplotlib.pyplot as plt
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline

# this two array has got the same length
CONST_ALPHAS = [0, 0.1, 1, 5, 10, 20, 50]
CONST_DEGREE = list(range(2, len(CONST_ALPHAS) + 2))
CONST_EXPERIMENT = len(CONST_ALPHAS)

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

pipelines = []
linear_model_scores = []
polynomial_model_scores = {}

for i in list(range(CONST_EXPERIMENT)):
    alpha_value = CONST_ALPHAS[i]
    degree_value = CONST_DEGREE[i]
    pip = make_pipeline(PolynomialFeatures(degree=degree_value), Ridge(alpha = alpha_value))
    # pip.steps[1][1] is the Ridge linear Model
    # pip.steps[0][1] is the Polynomial model 
    polynomial_model = pip.steps[0][1]
    linear_model = pip.steps[1][1]

    # compute ridge linear model with alpha = CONST_ALPHAS[i]
    linear_model.fit(training_set["x"], training_set["y"])
    linear_score = linear_model.score(validation_set["x"],validation_set["y"])
    linear_model_scores.append(linear_score)

    # compute polynomial model with degree = CONST_DEGREE[i]
    # the main idea is the following: http://scikit-learn.org/stable/modules/linear_model.html#polynomial-regression-extending-linear-models-with-basis-functions
    # Hence the following is a "linearized" polynomial model
    linearized_plm = Ridge() # alpha = 1
    new_trainX = polynomial_model.fit_transform(training_set["x"]) # this method "transform" the superlinear coeff into linear coeff 
    linearized_plm.fit(new_trainX, training_set["y"])
    polynomial_score = linearized_plm.score(polynomial_model.fit_transform(validation_set["x"]), validation_set["y"])
    polynomial_model_scores[degree_value] = polynomial_score

    pipelines.append(pip)

plt.xlabel("Alphas values")
plt.ylabel("Score")
plt.plot(CONST_ALPHAS, linear_model_scores)
plt.show()

plt.xlabel("Polynomial degree")
plt.ylabel("Score")
plt.plot(CONST_DEGREE,polynomial_model_scores.values())
plt.show()