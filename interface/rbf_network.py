from rbf_neuron import RbfNeuron

class RbfNetwork:
    """ Radial Base Function neural network class """
    
    # Size of data or knowledge in bytes
    PATTERN_SIZE = 4.0
    # Default radius
    DEFAULT_RADIUS = 0.5
    # Index of neuron ready to learn
    _index_ready_to_learn = 0;
    
    def __init__(self, neuron_count):
        """ Class constructor, takes 'neuron_count' as parameter
        for setting network size """
        # Set data size of neuron to be created
        RbfNeuron.PATTERN_SIZE = RbfNetwork.PATTERN_SIZE
        # Set default radius of neurons
        RbfNeuron.DEFAULT_RADIUS = RbfNetwork.DEFAULT_RADIUS
        # Create neuron list
        self.neuron_list = []
        # Create list of recognized knowledge
        self._knowledge_recognized = []
        # Set network state as MISS
        self._state = "MISS"
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
        # Erase knowledge from previous recognitions
        self._knowledge_recognized = []
        for index in range(RbfNetwork._index_ready_to_learn):
            if self.neuron_list[index].recognize(pattern):
                # Store all knowledge recognized
                self._knowledge_recognized.append(self.neuron_list[index].get_knowledge())

        # If no knowledge recognized
        if len(self._knowledge_recognized) == 0:
            self._state = "MISS"
            return self._state

        # Check if all neurons recognize pattern as related to the same
        # class and set
        recognized_class = self._knowledge_recognized[0].get_class()
        recognized_set = self._knowledge_recognized[0].get_set()
        for knowledge in self._knowledge_recognized:
            if recognized_class != knowledge.get_class() or recognized_set != knowledge.get_set():
                self._state = "DIFF"
                return self._state

        self._state = "HIT"
        return self._state

    def get_knowledge(self):
        if self._state == "HIT":
            return self._knowledge_recognized[0]
        else:
            return None

    def learn(self, knowledge):
        """ Learns a new pattern as pertaining to the given 
        pattern class and pattern set """
        # Learn procedure when pattern has not been recognized
        if self.recognize(knowledge.get_pattern()) == 'MISS':
            # Select ready-to-learn neuron
            ready_to_learn_neuron = self.neuron_list[RbfNetwork._index_ready_to_learn] 
            # Learn and store result (True or False) in auxiliar variable 'ret_val'
            learned = ready_to_learn_neuron.learn(knowledge)
            # Increment ready-to-learn neuron index
            if learned:
                RbfNetwork._index_ready_to_learn += 1
            # Return whether net succesfully learned the given pattern
            return learned
        else:
            return False
    
