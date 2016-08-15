from rbf_neuron import RbfNeuron

import pickle

class RbfNetwork:
    """ Radial Base Function neural network class """
    
    # Size of data or knowledge in bytes
    PATTERN_SIZE = 4.0
    # Default radius
    DEFAULT_RADIUS = 0.5

    
    def __init__(self, neuron_count):
        """ Class constructor, takes 'neuron_count' as parameter
        for setting network size """
        # Set data size of neuron to be created
        RbfNeuron.PATTERN_SIZE = RbfNetwork.PATTERN_SIZE
        # Set default radius of neurons
        RbfNeuron.DEFAULT_RADIUS = RbfNetwork.DEFAULT_RADIUS
        # Create neuron list
        self.neuron_list = []
        # Create list of neurons' indexes that recognized knowledge
        self._index_recognize = []
        # Set network state as MISS
        self._state = "MISS"
        # Fill neuron list with nre RbfNeuron instances
        for index in range(neuron_count):
            self.neuron_list.append(RbfNeuron())
        # Set index of neuron ready to learn as 0
        self._index_ready_to_learn = 0

    def get_neuron_count(self):
        """ Returns number of neurons in network """
        return len(self.neuron_list)

    def recognize(self, pattern):
        """ Returns 'HIT' if the given pattern is recognized, 
        'MISS' if the network does not recognize the pattern and
        'DIFF' if the network identifys the pattern as representing
        different classes """
        # Erase indexes of neurons that recognized in previous recognition processes
        self._index_recognize = []
        for index in range(self._index_ready_to_learn):
            if self.neuron_list[index].recognize(pattern):
                # Store all knowledge recognized
                self._index_recognize.append(index)

        # If no knowledge recognized
        if len(self._index_recognize) == 0:
            self._state = "MISS"
            return self._state

        # Check if all neurons recognize pattern as related to the same
        # class and set
        recognized_class = self.neuron_list[self._index_recognize[0]].get_class()
        recognized_set = self.neuron_list[self._index_recognize[0]].get_set()
        for index in self._index_recognize:
            neuron = self.neuron_list[index]
            if neuron.get_class() != recognized_class or neuron.get_set() != recognized_set:
                self._state = "DIFF"
                return self._state
        self._state = "HIT"
        return self._state

    def get_knowledge(self):
        if self._state == "HIT":
            return self.neuron_list[self._index_recognize[0]].get_knowledge()
        else:
            return None

    def get_state(self):
        return self._state

    def learn(self, knowledge):
        """ Learns a new pattern as pertaining to the given 
        pattern class and pattern set """
        # Learn procedure when pattern has not been recognized
        self.recognize(knowledge.get_pattern())
        # If the pattern has not been recognized by any neuron in the net
        if  self._state == 'MISS':
            # Learn in ready-to-learn neuron
            return self._learn_ready_to_learn(knowledge)
        # If various neurons have recognized the pattern as pertaining to different classes
        elif self._state == 'DIFF':
            # Get correct class
            correct_class = knowledge.get_class()
            # Correct class identified by at least one neuron flag
            correct_flag = False
            # Reduce radius of all neurons that do not recognize the pattern
            for index in self._index_recognize:
                neuron = self.neuron_list[index]
                if neuron.get_class() != correct_class:
                    neuron.reduce_radius_last_distance()
                else:
                    correct_flag = True
            if correct_flag:
                return True
            # If correct class was not identified by any recognizing neuron, learn
            return self._learn_ready_to_learn(knowledge)

        # If at least one neuron recognizes the pattern as pertaining to a unique class
        else:
            correct_class = knowledge.get_class()
            # If the class to be learned is different from the class identified
            if correct_class != self.neuron_list[self._index_recognize[0]].get_class():
                # Min distance from recognizing neurons to class
                min_distance = RbfNeuron.DEFAULT_RADIUS;
                # Reduce radius to all recognizing neurons
                for index in self._index_recognize:
                    neuron = self.neuron_list[index]
                    neuron.reduce_radius_last_distance()
                    # Get distance
                    neuron_distance =  neuron.get_distance()
                    # If distance is less than current minimum distance, store
                    if neuron_distance < min_distance:
                        min_distance = neuron_distance
                # Learn new knowledge with radius = min_distance
                self._learn_ready_to_learn(knowledge, min_distance)
            return True


    def _learn_ready_to_learn(self, knowledge, radius = RbfNeuron.DEFAULT_RADIUS):
        """Learn new knowledge in ready-to-learn neuron """
        # Learn new pattern in ready-to-learn neuron
        # Select ready-to-learn neuron
        ready_to_learn_neuron = self.neuron_list[self._index_ready_to_learn]
        # Learn and store result (True or False) in auxiliary variable 'ret_val'
        learned = ready_to_learn_neuron.learn(knowledge)
        # Set radius
        ready_to_learn_neuron.set_radius(radius)
        # Increment ready-to-learn neuron index
        if learned:
            self._index_ready_to_learn += 1
        # Return whether net succesfully learned the given pattern
        return learned

    def get_rneurons_ids(self):
        """ Returns indexes of neurons that recognized a pattern in the last
        recognition process """
        return self._index_recognize

    def get_last_learned_id(self):
        """ Return index of last neuron with knowledge """
        return self._index_ready_to_learn - 1

    @classmethod
    def  serialize(cls, obj, name):
        pickle.dump(obj, open(name, "wb"))

    @classmethod
    def deserialize(cls, name):
        return pickle.load(open(name, "rb"))
