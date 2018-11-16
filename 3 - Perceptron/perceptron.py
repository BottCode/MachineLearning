from random import choice, uniform 
from numpy import array, dot, random
from math import inf

e = 2.71828
MAX_IT = 10

class Perceptron:

    def __init__(self, weights, learning_rate):
        self._weights = weights
        self._learning_rate = learning_rate
    
    def sumWeightData(self,X): # the perceptron's inner function
        total = 0
        for i in range(len(X)):
            total = total + (X[i] * self._weights[i])
        return total


def stepFunction(x):
    if x > 0:
        return 1
    return 0

def logisticFunction(x):
    return 1 / (1 + e**(-x))

def isLearning(perceptron, training_data):
    for data in training_data:
        X = data[0]
        target = data[1]
        if stepFunction(perceptron.sumWeightData(X)) != target:
            return True
    return False

def squaredError(X, W):
    total = 0.0
    for data in training_data_OR:
        target = data[1]
        total += ((target - dot(X, W))**2)
    return total / (2*len(training_data_OR))

    
# ALGORITHM
x0 = 1
training_data_OR = [ # => [(x0,x1,x2),target]
    [(x0,0,0),0],
    [(x0,0,1),1],
    [(x0,1,0),1],
    [(x0,1,1),1]
]

# yields 3 random number in [-1,1] => they are the starting weights. The first one is the bias
weights = [random.uniform(-0.05,+0.05) for _ in range (3)]
old_w = weights.copy()
learning_rate = 0.01
perceptron = Perceptron(weights,learning_rate)
deltaw = [0 for _ in range(len(perceptron._weights))]
iterations = 0

print("###\nPerceptron with STEP function\n###\n")
print("Starting weights: ", perceptron._weights)

while isLearning(perceptron,training_data_OR):
    for data in training_data_OR:
        # data = ((input1, input2, bias), target)
        X = data[0]
        target = data[1]
        # perceptron prediction
        output = stepFunction(perceptron.sumWeightData(X))
        for i in range(len(deltaw)):
            deltaw[i] = deltaw[i] + learning_rate * (target - output) * X[i]
    for i in range(len(perceptron._weights)):
        perceptron._weights[i] += deltaw[i]
    iterations += 1

print("Final weights: ", perceptron._weights)
print(iterations,"Iterations\n")


print("###\nPerceptron with LOGISTIC function\n###\n")

weights = old_w
perceptron = Perceptron(weights,learning_rate)
deltaw = [0 for _ in range(len(perceptron._weights))]

print("Starting weights: ", perceptron._weights)

iterations = 0
error = inf
isNotOverStepped = True

while isNotOverStepped:
    for data in training_data_OR:
        # data = ((input1, input2, bias), target)
        X = data[0]
        target = data[1]
        # perceptron prediction
        y = perceptron.sumWeightData(X)
        output = logisticFunction(y)
        for i in range(len(deltaw)):
            deltaw[i] = deltaw[i] + learning_rate * (target - output) * output * (1-output) * X[i]
    for i in range(len(perceptron._weights)):
        perceptron._weights[i] += deltaw[i]
    new_err = squaredError(X, perceptron._weights)
    iterations += 1
    if new_err > error: # we have overstep the minimum
        isNotOverStepped = False 
    error = new_err
    
print("Final weights: ", perceptron._weights)
print(iterations,"Iterations")
