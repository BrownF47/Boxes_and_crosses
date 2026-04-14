import numpy as np

# Simple neural net with 3 hidden layers, that get progessively smaller #

# Final output is a probabilty of winning from a given state # 

class NeuralNet():

    def __init__(self):
        
        self.layer_1 = np.zeros(24)
        self.layer_2 = np.zeros(12)
        self.layer_3 = np.zeros(6)
        self.output = np.zeros(1)

        self.weights_1 = np.random.rand(24,24)
        self.weights_2 = np.random.rand(24,12)
        self.weights_3 = np.random.rand(12,6)
        self.weights_4 = np.random.rand(6,1)

        self.biases_1 = np.random.rand(24,1)
        self.biases_2 = np.random.rand(12,1)
        self.biases_3 = np.random.rand(6,1)
        
    def ReLU(self, x):
        if x < 0:
            return 0
        else: 
            return x
        
    def propagate_forward(self):
        pass
        
    
