#Perceptron program to make a single neuron ANN with 5 boolean inputs
#Manan Isak
#02/17/2022
#https://www.kdnuggets.com/2019/11/build-artificial-neural-network-scratch-part-1.html

import random
import math

#Activation function
def activation(x):
    if x >= 0:
        return 1
    elif x < 0:
        return 0

#6 Correct Inputs (Output 1, otherwise output 0)
correctIn = ["01111", "10111", "11011", "11101", "11110", "11111"]

weights = ([random.random(),random.random(),random.random(),random.random(),random.random(),random.random()])    # 5 random initial input weights + threshold weight
threshold = -1
learningRate = 0.1

for gen in range(100):
    # Test each of the 32 possible values for training
    for i in range(32):
        x = 0
        y = 0
        desired = 0
        error = 0
        
        inputString = f'{i:05b}' # Formats the integer i into a binary number while adding 0s to the left to keep it 5 digits
        
        for j in range(5):  # For every bit in inputString
            x = x + (float(inputString[j]) * weights[j])
        y = activation(x + (threshold * weights[5]))


        for inp in correctIn:   # Calculating if the output SHOULD be a 0 or a 1
            if inputString == inp:
                desired = 1

        error = desired - y

        for j in range(5):  # For every weight
            weights[j] = weights[j] + (learningRate * float(inputString[j]) * error)

        weights[5] = weights[5] + (learningRate * -1 * error)

print(weights)

#Test after training
testIn = input("Enter a five bit number: ")

while testIn[0] == "0" or testIn[0] == "1":
    x = 0
    for i in range(5):
        x = x + (float(testIn[i]) * weights[i])
    print(activation(x + (threshold * weights[5])))
    testIn = input("Enter a five bit number: ")
