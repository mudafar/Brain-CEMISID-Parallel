from rbf_knowledge import RbfKnowledge


class RbfNeuron:
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
        # Neuron has no knowledge when created
        self._has_knowledge = False
        # Neuron has default radius when created
        self.set_radius(RbfNeuron.DEFAULT_RADIUS)
        # Increment number of class instances
        RbfNeuron.instances_count += 1
        # Initialize degraded state
        self._degraded = False

    def has_knowledge(self):
        """ Returns whether neuron has knowledge or not """
        return self._has_knowledge

    def is_member(self, test_set):
        """ Returns wheter neuron is memeber of set """
        return (self.get_set() == test_set)

    def set_radius(self, radius):
        """ Sets neuron radius """
        self._radius = radius

    def get_radius(self):
        """ Gets neuron radius """
        return self._radius

    def get_knowledge(self):
        """ Returns neuron knowledge """
        if (self.has_knowledge()):
            return self._knowledge
        else:
            return None

    def get_class(self):
        """ Returns class of knowledge if neuron has 
        knowledge, and None in any other case """
        if (self.has_knowledge()):
            return self._knowledge.get_class()
        else:
            return None

    def get_set(self):
        """ Returns set of knowledge if neuron has 
        knowledge, and None in any other case """
        if (self.has_knowledge()):
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
        return self._distance;

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
            raise ValueError("value must be greater than radius of neuron")
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