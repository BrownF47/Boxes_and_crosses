import numpy as np

# Simple neural net with 3 hidden layers, that get progessively smaller #

# Final output is a probabilty of winning from a given state # 

class NeuralNet():

    def __init__(self):
        
        self.layer_1 = np.zeros((1,24))
        self.layer_2 = np.zeros((1,12))
        self.layer_3 = np.zeros((1,6))
        self.output = np.zeros((1,1))

        self.weights_1 = np.random.rand(24,24)
        self.weights_2 = np.random.rand(24,12)
        self.weights_3 = np.random.rand(12,6)
        self.weights_4 = np.random.rand(6,1)

        self.biases_1 = np.random.rand(1,24)
        self.biases_2 = np.random.rand(1,12)
        self.biases_3 = np.random.rand(1,6)
        self.biases_4 = np.zeros((1,1))

        self.alpha = 0.0001
        
    def ReLU(self, x):
        return np.maximum(0, x)
    
    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))
        
    def propagate_layer_forward(self, weights, biases, previous_layer):
        next_layer = np.matmul(previous_layer, weights) + biases

        return next_layer
    
    def propagate_network_forward(self, state):
        self.layer_1 = self.propagate_layer_forward(self.weights_1, self.biases_1, state)
        self.layer_2 = self.propagate_layer_forward(self.weights_2, self.biases_2, self.ReLU(self.layer_1))
        self.layer_3 = self.propagate_layer_forward(self.weights_3, self.biases_3, self.ReLU(self.layer_2))
        output = self.sigmoid(self.propagate_layer_forward(self.weights_4, self.biases_4, self.ReLU(self.layer_3)))
        return output
        
    def binary_cross_entropy(self, prediction, truth):
        return -np.mean(truth * np.log(prediction) + (1 - truth) * np.log(1 - prediction))
    
    def back_prop(self):
        pass

    def binary_cross_entropy_gradient(self, prediction, truth):
        return -((truth/prediction)-(1-truth)/(1-prediction))
    
    def sigmoid_gradient(self, x):
        return self.sigmoid(x) * (1-self.sigmoid(x))
    


    def test_net(self, test_input):
        self.output = self.propagate_network_forward(test_input)
        print(self.output)
        return self.output
        
        
if __name__ == "__main__":
    test_input = np.zeros((1, 24))
    test_input[0,1] = 1
    test_input[0,2] = 1
    test_input[0,5] = 1
    test_input[0,8] = 1
    test_input[0,12] = 1
    test_input[0,15] = 1
    test_input[0,16] = 1
    test_input[0,23] = 1
    print(test_input)

myNet = NeuralNet()
myNet.test_net(test_input)


        
        
    
