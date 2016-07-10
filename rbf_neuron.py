from math import fabs

class RbfNeuron:
    """ Radial Base Function neuron class """
    # Number of class instances
    instances_count = 0
    # Size of data or knowledge in bytes
    DATA_SIZE = 4.0
    # Default radius
    DEFAULT_RADIUS = 0.5
    
    # Class constructor
    def __init__(self):
        # Neuron has no knowledge when created
        self.set_has_knowledge(False)
        # Neuron has default radius when created
        self.set_radius(RbfNeuron.DEFAULT_RADIUS)
        # Increment number of class instances
        RbfNeuron.instances_count += 1
        
    """ Returns whether neuron has knowledge or not """
    def has_knowledge(self):
        return self.has_knowledge
    
    """ Sets the has-knowledge (has_knowledge) internal flag """
    def set_has_knowledge(self, value ):
        self.has_knowledge = value
        
    """ Returns wheter neuron is memeber of set """
    def is_member(self, test_set):
        return (self.neuron_set == test_set)
        
    """ Sets neuron radius """
    def set_radius(self, new_radius):
        self.radius = new_radius
        
    """ Gets neuron radius """
    def get_radius(self):
        return self.radius
    
    """ Sets neuron class """
    def set_class(self, new_class ):
        self.neuron_class = new_class
        
    """ Gets neuron class """
    def get_class(self):
        if self.neuron_class == None:
            raise ValueError
        return self.neuron_class

    """ Sets neuron set """
    def set_set(self, new_set ):
        self.neuron_set = new_set
        
    """ Gets neuron set """
    def get_set(self):
        if self.neuron_set == None:
            raise ValueError
        return self.neuron_set
        
    """ Sets neuron data or 'center' of knowledge """
    def set_data(self, new_data):
        self.neuron_data = new_data
        
    """ Gets neuron data or 'center' of knowledge """
    def get_data(self, new_data):
        if self.neuron_data == None:
            raise ValueError
        return self.neuron_data
        
    """ Calculates Manhattan distance, private method """
    def _calculate_manhattan_distance(self, pattern):
    	# Given pattern must be of size equal to DATA_SIZE
        if len(pattern) != RbfNeuron.DATA_SIZE:
            raise ValueError
        # Initialize distance atribute to zero
        self.distance = 0
        # Calculate Manhattan distance
        for index in range(len(pattern)):
            self.distance += fabs(self.neuron_data[index]-pattern[index])
        # Return distance
        return self.distance
    
    """ Returns true if neuron recognizes given pattern """
    def recognize(self, pattern ):
    	# If Manhattan distance to pattern is less than neuron radius
    	# there is a hit
        if self._calculate_manhattan_distance(pattern) < self.get_radius():
            self.hit = True
        else:
            self.hit = False
        # Return whether there has been a hit or not
        return self.hit
    
    """ Learns a new pattern (knowledge, data), return true if
        the pattern was succesfully learned and false in any other case """
    def learn(self, pattern, class_, set_):
        # Tries to store pattern
        try:
            self.set_data(pattern)
        except TypeError:
            print "pattern must be a list of integers"
            return False
        # Tries to store pattern class 
        try:
            self.set_class(class_)
        except TypeError:
            print "class_ must be a string"
            return False
            
        # Tries to store class set
        try:
             self.set_set(set_)
        except TypeError:
            print "set_ must be a string"
            return False    
        # Indicate that this neuron has knowledge
        self.set_has_knowledge(True)
        # Return True to indicate proper learning process
        return True

    """ Reduces neuron radius by 'value' """
    def reduce_radius_by(self, value ):
        if value < 0 :
            raise ValueError("value must be positive")
        if self.radius < value :
            raise ValueError("value must be greater than radius of neuron")
        self.radius -= value
