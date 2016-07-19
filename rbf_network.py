from rbf_neuron import RbfNeuron

class RbfNetwork:
    """ Radial Base Function neural network class """
    
    # Size of data or knowledge in bytes
    DATA_SIZE = 4.0
    # Default radius
    DEFAULT_RADIUS = 0.5
    # Index of neuron ready to learn
    _index_ready_to_learn = 0;
    
    def __init__(self, neuron_count):
        """ Class constructor, takes 'neuron_count' as parameter
        for setting network size """
        # Set data size of neuron to be created
        RbfNeuron.DATA_SIZE = RbfNetwork.DATA_SIZE
        # Set default radius of neurons
        RbfNeuron.DEFAULT_RADIUS = RbfNetwork.DEFAULT_RADIUS
        # Create neuron list
        self.neuron_list = []
        # Fill neuron list with nre RbfNeuron instances
        for index in range(neuron_count):
            self.neuron_list.append(RbfNeuron())
        # Set index of neuron ready to learn as 0
        RbfNetwork._index_ready_to_learn = 0
        
    def get_neuron_count(self):
        """ Returns number of neurons in network """
        return len(self.neuron_list)

    def recognize(self, pattern):
        """ Returns 'HIT' if the given pattern is recognized, 
        'MISS' if the network does not recognize the pattern and
        'DIFF' if the network identifys the pattern as representing
        different classes """
        for index in range(RbfNetwork._index_ready_to_learn):
            if self.neuron_list[index].recognize(pattern):
                return 'HIT'
        return 'MISS'
        
        
    def learn(self, knowledge):
        """ Learns a new pattern as pertaining to the given 
        pattern class and pattern set """
        # Learn procedure when pattern has not been recognized
        if self.recognize(knowledge.get_pattern()) == 'MISS':
            # Select ready-to-learn neuron
            ready_to_learn_neuron = self.neuron_list[RbfNetwork._index_ready_to_learn] 
            # Learn and store result (True or False) in auxiliar variable 'ret_val'
            learned = ready_to_learn_neuron.learn(pattern, pattern_class, pattern_set)
            # Increment ready-to-learn neuron index
            if learned:
                RbfNetwork._index_ready_to_learn += 1
            # Return whether net succesfully learned the given pattern
            return learned
        else:
            return False
    
   
     
# Some tests
if __name__ == '__main__':
    
    #Create a neural network of RbfNeurons
    n_count = 10
    net_1 = RbfNetwork(n_count)

    # Get number of neurons
    print "There are " + str(net_1.get_neuron_count()) + " neurons in the net"
    k1 = RbfKnowledge([1,2,3,4], "caballo", "animal" )
    k1 = RbfKnowledge([2,3,4,5], "vaca", "animal" )
    
    if( net_1.recognize([1.1,2.1,3,4]) == "HIT" ):
        print "reconozco"
    if( net_1.recognize([2.2,3.2,4,5]) == "HIT" ):
        print "reconozco"
    else:
        print "no reconozco"