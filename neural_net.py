import numpy as np

# Simple neural net with 3 hidden layers, that get progessively smaller #

# Final output is a probabilty of winning from a given state # 

class NeuralNet():

    def __init__(self):
        
        # Column vector layers #

        self.layer_1 = np.zeros((24,1))
        self.layer_2 = np.zeros((12,1))
        self.layer_3 = np.zeros((6,1))
        self.output = np.zeros((1,1))

        # Matching column vector biases # 

        self.biases_1 = np.zeros((24,1))
        self.biases_2 = np.zeros((12,1))
        self.biases_3 = np.zeros((6,1))
        self.biases_4 = np.zeros((1,1))

        # Weight matrices #

        self.weights_1 = np.random.randn(24,24) * np.sqrt(1/24)
        self.weights_2 = np.random.randn(12,24) * np.sqrt(1/24)
        self.weights_3 = np.random.randn(6,12) * np.sqrt(1/12)
        self.weights_4 = np.random.randn(1,6) * np.sqrt(1/6)

        self.pre_sigmoid_output = np.zeros((1,1))

        self.alpha = 0.0001
        
    def ReLU(self, x):
        return np.maximum(0, x)
    
    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))
        
    def propagate_layer_forward(self, weights, biases, previous_layer):
        next_layer = np.matmul(weights, previous_layer) + biases
        return next_layer
    
    def propagate_network_forward(self, state):
        self.layer_1 = self.propagate_layer_forward(self.weights_1, self.biases_1, state)
        self.layer_2 = self.propagate_layer_forward(self.weights_2, self.biases_2, self.ReLU(self.layer_1))
        self.layer_3 = self.propagate_layer_forward(self.weights_3, self.biases_3, self.ReLU(self.layer_2))
        self.pre_sigmoid_output = self.propagate_layer_forward(self.weights_4, self.biases_4, self.ReLU(self.layer_3))
        self.output = self.sigmoid(self.pre_sigmoid_output)
        return self.output
        
    def binary_cross_entropy(self, prediction, truth):
        prediction = np.clip(prediction, 1e-7, 1 - 1e-7)
        return -np.mean(truth * np.log(prediction) + (1 - truth) * np.log(1 - prediction))
    
    def back_prop(self, prediction, truth):
        loss_gradiant = self.binary_cross_entropy_gradient(prediction, truth)
        print(f"Loss gradient: {loss_gradiant}")
        sigmoid_gradient = self.sigmoid_gradient(self.pre_sigmoid_output)
        print(f"Sigmoid gradient: {sigmoid_gradient}")
        delta_gradient = loss_gradiant * sigmoid_gradient
        
        # output weights #
        
        weight_4_gradient = delta_gradient * self.layer_3
        biases_4_gradient = delta_gradient
        
        
        self.weights_4 = self.weights_4 - (self.alpha * weight_4_gradient)
        self.biases_4 = self.biases_4 - (self.alpha * biases_4_gradient)

        # layer 3 weights # 


        


    def binary_cross_entropy_gradient(self, prediction, truth):
        prediction = np.clip(prediction, 1e-7, 1 - 1e-7)
        return -((truth/prediction)-(1-truth)/(1-prediction))
    
    def sigmoid_gradient(self, x):
        return self.sigmoid(x) * (1-self.sigmoid(x))
    
    def test_net(self, test_input):
        self.output = self.propagate_network_forward(test_input)
        print(self.output)
        truth = np.zeros((1,1))
        print(truth)
        loss = self.binary_cross_entropy(self.output, truth)
        print(f"Loss: {loss}")
        self.back_prop(self.output, truth)

        
        
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
    #print(test_input)

myNet = NeuralNet()
myNet.test_net(test_input.T)


        
        
    
