import pickle

class BiclassPerceptronNetwork():
    """ One layer perceptron network with two outputs for classification of inputs
     in up to three different categories """

    def __init__(self, inputs_number):
        """ BiclassPerceptronNetwork constructor
        :param inputs_number: number of inputs in perceptron network
        """
        # Number of inputs in perceptron net must be a positive integer
        if type(inputs_number) is not int or inputs_number <= 0:
            raise TypeError('BiclassPerceptronNetwork constructor expects inputs_number to be a positive number')
        # Weight vector for outputs 1 and 2
        self.weights_1 = [0 for index in range(inputs_number)]
        self.weights_2 = [0 for index in range(inputs_number)]
        # Inputs
        self.inputs = [0 for index in range(inputs_number)]
        # Output
        self.outputs = [0, 0]

    def get_inputs(self):
        return self.inputs

    def set_inputs(self, new_inputs):
        self.inputs = new_inputs

    def get_outputs(self):
        self.outputs = self._calc_output()
        return self.outputs

    def training(self, training_set):

        for input_vector, desired_output in training_set:
            current_output = self._calc_output(input_vector)
            error = [do_j-co_j for do_j, co_j in zip(desired_output, current_output)]
            self.update_weights(input_vector, error)

    def _calc_output(self, input_vector=None):
        if input_vector is None:
            input_vector = self.inputs
        dot_product_1 = sum(input_j * weight_j for input_j, weight_j in zip(input_vector, self.weights_1))
        dot_product_2 = sum(input_j * weight_j for input_j, weight_j in zip(input_vector, self.weights_2))
        return [self._activation_function(dot_product_1), self._activation_function(dot_product_2)]

    def _activation_function(self, val):
        if val <= 0:
            return 0
        return 1

    def update_weights(self, input_vector, error):
        # Update weights in order to match desired output
        for index in range(len(self.weights_1)):
            self.weights_1[index] = self.weights_1[index] + error[0]*input_vector[index]
            self.weights_2[index] = self.weights_2[index] + error[1]*input_vector[index]

# Tests
if __name__ == '__main__':
    net = BiclassPerceptronNetwork(3)

    training_set = [([0.9,0.5,0.4],[1,0]), ([0.5,0.7,0.4],[0,1]), ([0.1,0.3,0.8],[0,0]), ([0.7,0.3,0.1],[1,0]), ([0.35,0.8,0.2],[0,1]), ([0.20,0.35,0.83],[0,0]), ([0.97,0.52,0.43],[1,0]), ([0.4,0.9,0.5],[0,1]), ([0.6,0.3,0.8],[0,0])]

    print "Before training"
    net.inputs =[1,1,1]
    print "Inputs = [1,1,1], Outputs = ", net.get_outputs()

    net.training(training_set)
    print "After training"
    print "Weights1: ", net.weights_1, "Weights2", net.weights_2
    net.inputs = [0.7, 0.3, 0.2]
    print "Inputs = ", net.inputs, "Outputs = ", net.get_outputs()
    net.inputs = [0.1, 0.8, 0.2]
    print "Inputs = ", net.inputs, "Outputs = ", net.get_outputs()
    net.inputs = [0.3, 0.1, 0.7]
    print "Inputs = ", net.inputs, "Outputs = ", net.get_outputs()
    net.inputs = [0.3,0.1,0.4]
    print "Inputs = ", net.inputs, "Outputs = ", net.get_outputs()


