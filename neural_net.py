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
        
    def ReLU(self, x):
        return np.maximum(0, x)
        
    def propagate_layer_forward(self, weights, biases, previous_layer):
        #print(np.shape(weights))
        #print(np.shape(previous_layer))
        next_layer = self.ReLU(np.matmul(previous_layer, weights) + biases)

        return next_layer
    
    def propagate_network_forward(self, state):
        hidden_layer_1 = self.propagate_layer_forward(self.weights_1, self.biases_1, state)
        hidden_layer_2 = self.propagate_layer_forward(self.weights_2, self.biases_2, hidden_layer_1)
        hidden_layer_3 = self.propagate_layer_forward(self.weights_3, self.biases_3, hidden_layer_2)
        output = self.propagate_layer_forward(self.weights_4, self.biases_4, hidden_layer_3)
        return output
        

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


        
        
    
