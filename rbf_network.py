from rbf_neuron import RbfNeuron

class RbfNetwork:
    """ Radial Base Function neural network class """
    
    def __init__(self, neuron_count):
        """ Class constructor, takes 'neuron_count' as parameter
        for setting network size """
        # Set data size of neuron to be created
        RbfNeuron.DATA_SIZE = 5.0
        # Set default radius of neurons
        RbfNeuron.DEFAULT_RADIUS = 0.7
        # Create neuron list
        self.neuron_list = []
        # Fill neuron list with RbfNeurons
        for index in range(neuron_count):
            self.neuron_list.append(RbfNeuron())
            
    def get_neuron_count(self):
        """ Returns number of neurons in network """
        return len(self.neuron_list)

# Some tests
if __name__ == '__main__':
    #Create a neural network of RbfNeurons
    n_count = 3
    net_1 = RbfNetwork(n_count)
    
    # Get number of neurons
    print "There are " + str(net_1.get_neuron_count()) + " neurons in the net"
        
    
        