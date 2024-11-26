#Breakout ANN with back propagation program to make a 8 neuron ANN with 5 boolean inputs, 5 hidden nodes and 3 output nodes
#Manan Isak & Kate Le
#04/25/2022

import random
import math

#Activation function
def activation(x):
    if x >= 0:
        return 1
    elif x < 0:
        return 0

def activationSigmoid(x):
    return 1/(1+math.exp(-x))

#12 Correct Inputs (Output 1, otherwise output 0)
correctIn = ["01111", "10111", "11011", "11101", "11110", "11111", "00000", "10000", "01000", "00100", "00010", "00001"]

# 5 lots of 5 input weights + 1 threshold weight THEN 3 lots of 5 input weights + 1 threshold weight
'''
weights = ([[random.random(),random.random(),random.random(),random.random(),random.random(),random.random()],
           [random.random(),random.random(),random.random(),random.random(),random.random(),random.random()],
           [random.random(),random.random(),random.random()]])
'''

weights = [[random.random()] * 6 for i in range(8)] #6 weights for each of 8 nodes. 48 total

threshold = -1
learningRate = 0.1

for epoch in range(10000):
    # Test each of the 32 possible values for training
    for i in range(32):
        hiddenOut = [0,0]   # The hidden outputs for both hidden nodes
        inputString = f'{i:05b}' # Formats the integer i into a binary number while adding 0s to the left to keep it 5 digits
        
        # Find outputs of the two hidden nodes first
        for j in range(2):
            x = 0
            
            for k in range(5):  # For every bit in inputString
                x = x + (float(inputString[k]) * weights[j][k])
            hiddenOut[j] = activationSigmoid(x + (threshold * weights[j][5]))

        # Test the final output node and calculate error then back propagate
        desired = 0
        error = 0
        x = 0
        y = 0

        x = (hiddenOut[0]*weights[2][0]) + (hiddenOut[1]*weights[2][1])
        y = activationSigmoid(x + (threshold * weights[2][2]))
        
        for inp in correctIn:   # Calculating if the output SHOULD be a 0 or a 1
            if inputString == inp:
                desired = 1

        error = desired - y
        dk = y * (1-y) * error

        # Adjusting input weights for neuron k
        for j in range(2):
            weights[2][j] = weights[2][j] + (learningRate * hiddenOut[j] * dk)

        # Adjusting threshold weight for neuron k
        weights[2][2] = weights[2][2] + (learningRate * threshold * dk)

        
        # Adjusting input weights for hidden layer
        for j in range(2):
            for k in range(5):  # For every weight 
                weights[j][k] = weights[j][k] + (learningRate * float(inputString[k]) * hiddenOut[j] * (1-hiddenOut[j]) * dk * weights[2][j])

            # The two threshold weights
            weights[j][5] = weights[j][5] + (learningRate * threshold * hiddenOut[j] * (1-hiddenOut[j]) * dk * weights[2][j])

print(weights)

#Test after training
testIn = input("Enter a five bit number: ")

while testIn[0] == "0" or testIn[0] == "1":
    hiddenOut = [0]*5   # The hidden outputs for five hidden nodes
    finalOut = [0]*5 # The final outputs of the five output nodes
    # Find outputs of the five hidden nodes first
    for j in range(len(hiddenOut)):
        x = 0
        
        for k in range(len(testIn)):  # Take an input from an array of the 5 breakout inputs
            x = x + (float(testIn[k]) * weights[j][k])
        hiddenOut[j] = activationSigmoid(x + (threshold * weights[j][5])) # Or some other activation function

    # Find the outputs of the five output nodes
    for j in range(len(finalOut)):
        x = 0
        
        for k in range(len(hiddenOut)):  # Take an input from an array of the 5 hidden outputs
            x = x + (float(hiddenOut[k]) * weights[j+5][k])
        finalOut[j] = activationSigmoid(x + (threshold * weights[j+5][5]))
    
    testIn = input("Enter a five bit number: ")
