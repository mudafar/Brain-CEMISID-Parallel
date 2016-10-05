import pickle
from math import fabs

from neuron import Neuron


class RbfKnowledge:
    # Size of data or knowledge in bytes
    PATTERN_SIZE = 4.0

    def __init__(self, rbf_pattern, rbf_class, rbf_set="NoSet"):
        self.set_pattern(rbf_pattern)
        self.set_class(rbf_class)
        self.set_set(rbf_set)

    def set_pattern(self, pattern):
        self._pattern = pattern

    def set_class(self, rbf_class):
        self._class = rbf_class

    def set_set(self, rbf_set):
        self._set = rbf_set

    def get_pattern(self):
        return self._pattern

    def get_class(self):
        return self._class

    def get_set(self):
        return self._set

    def calc_manhattan_distance(self, pattern_or_knowledge):
        """ Returns Manhattan distance from this piece of
        knowledge to a given pattern """

        # If given parameter is of class knowledge, obtain pattern
        try:
            pattern = pattern_or_knowledge.get_pattern()
        # Else it must be a pattern
        except AttributeError:
            pattern = pattern_or_knowledge
        # Check patterns sizes are equal
        if len(pattern) != RbfKnowledge.PATTERN_SIZE:
            return False
        # Initialize distance variable to zero
        distance = 0
        # Calculate Manhattan distance
        for index in range(len(self._pattern)):
            distance += fabs(self._pattern[index] - pattern[index])
        # Return distance
        return distance


class RbfNeuron(Neuron):
    """ Radial Base Function neuron class """
    # Number of class instances
    instances_count = 0
    # Default radius
    DEFAULT_RADIUS = 10

    # Default radius
    MIN_RADIUS = 1

    # Default radius
    MAX_RADIUS = 50

    # Class constructor
    def __init__(self):
        super(RbfNeuron, self).__init__()
        # Neuron has no knowledge when created
        self._has_knowledge = False
        # Neuron has default radius when created
        self.set_radius(RbfNeuron.DEFAULT_RADIUS)
        # Increment number of class instances
        RbfNeuron.instances_count += 1
        # Initialize degraded state
        self._degraded = False

    def is_member(self, test_set):
        """ Returns wheter neuron is memeber of set """
        return self.get_set() == test_set

    def set_radius(self, radius):
        """ Sets neuron radius """
        self._radius = radius

    def get_radius(self):
        """ Gets neuron radius """
        return self._radius

    def get_class(self):
        """ Returns class of knowledge if neuron has
        knowledge, and None in any other case """
        if self.has_knowledge():
            return self._knowledge.get_class()
        else:
            return None

    def get_set(self):
        """ Returns set of knowledge if neuron has
        knowledge, and None in any other case """
        if self.has_knowledge():
            return self._knowledge.get_set()
        else:
            return None

    def get_pattern(self):
        """ Returns set of knowledge if neuron has
        knowledge, and None in any other case """
        if (self.has_knowledge()):
            return self._knowledge.get_pattern()
        else:
            return None

    def is_hit(self):
        """ Returns True if last call to recognize() was a hit
        and False in any other case """
        return self._hit

    def learn(self, knowledge):
        """ Learns a new piece of knowledge, return true if
        succesfully learned and false in any other case """
        self._knowledge = knowledge
        # Indicate that this neuron has knowledge
        self._has_knowledge = True
        # Return True to indicate proper learning process
        return True

    def recognize(self, pattern):
        """ Returns true if neuron recognizes given pattern """
        # If neuron degraded, do not recognize
        if self._degraded:
            return False

        # If Manhattan distance to pattern is less than neuron radius,
        # there is a hit
        self._distance = self._knowledge.calc_manhattan_distance(pattern)
        if self._distance < self.get_radius():
            self._hit = True
        else:
            self._hit = False
        # Return whether there has been a hit or not
        return self._hit

    def get_distance(self):
        return self._distance

    def reduce_radius_last_distance(self):
        """Reduces radius to distance from last recognized pattern"""
        if not self._hit:
            return False
        try:
            success = self.reduce_radius_by(self._radius-self._distance)
        except:
            return False
        return success

    def reduce_radius_by(self, value):
        # type: (value) -> integer
        """ Reduces neuron radius by 'value' """
        if value < 0:
            raise ValueError("value must be positive")
        if self._radius < value:
            raise ValueError("value must be less than radius of neuron")
        self._radius -= value
        # If radius of neuron is under minimum allowed value,
        # the neuron has been degraded and is no longer functional
        if self._radius < RbfNeuron.MIN_RADIUS:
            self._degraded = True
        # Return true if neuron has not been degraded after radiud reduction and false
        # in any other case
        return not self._degraded

    def increase_radius_by(self, value):
        """ Increases neuron radius by 'value' """
        if value < 0:
            raise ValueError("value must be positive")
        self._radius += value
        # If radius of neuron is over maximum allowed value,
        # the neuron has been degraded and is no longer functional
        if self._radius > RbfNeuron.MAX_RADIUS:
            self._degraded = True

    def is_degraded(self):
        # Returns wheter neuron is degraded
        return self._degraded


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
        # Id of neuron that learned last given knowledge
        self._last_learned_id = -1

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
        if self._state == 'MISS':
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
                    self._last_learned_id = index
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
                min_distance = RbfNeuron.DEFAULT_RADIUS
                # Reduce radius to all recognizing neurons
                for index in self._index_recognize:
                    neuron = self.neuron_list[index]
                    neuron.reduce_radius_last_distance()
                    # Get distance
                    neuron_distance = neuron.get_distance()
                    # If distance is less than current minimum distance, store
                    if neuron_distance < min_distance:
                        min_distance = neuron_distance
                # Learn new knowledge with radius = min_distance
                self._learn_ready_to_learn(knowledge, min_distance)
            return True

    def _learn_ready_to_learn(self, knowledge, radius=RbfNeuron.DEFAULT_RADIUS):
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
            self._last_learned_id = self._index_ready_to_learn
            self._index_ready_to_learn += 1
        # Return whether net succesfully learned the given pattern
        return learned

    def get_rneurons_ids(self):
        """ Returns indexes of neurons that recognized a pattern in the last
        recognition process """
        return self._index_recognize

    def get_last_learned_id(self):
        """ Return index of last neuron with knowledge """
        return self._last_learned_id

    def get_index_ready_to_learn(self):
        return self._index_ready_to_learn

    @classmethod
    def serialize(cls, obj, name):
        pickle.dump(obj, open(name, "wb"))

    @classmethod
    def deserialize(cls, name):
        return pickle.load(open(name, "rb"))
