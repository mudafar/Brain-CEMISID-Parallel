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
        

    def has_knowledge(self):
        """ Returns whether neuron has knowledge or not """
        return self.has_knowledge
    
    def set_has_knowledge(self, value ):
        """ Sets the has-knowledge (has_knowledge) internal flag """
        self.has_knowledge = value        

    def is_member(self, test_set):
        """ Returns wheter neuron is memeber of set """
        return (self.neuron_set == test_set)
        
    def set_radius(self, new_radius):
        """ Sets neuron radius """
        self.radius = new_radius
        
    def get_radius(self):
        """ Gets neuron radius """
        return self.radius
    
    def set_class(self, new_class ):
        """ Sets neuron class """
        self.neuron_class = new_class
        
    def get_class(self):
        """ Gets neuron class """
        if self.neuron_class == None:
            raise ValueError
        return self.neuron_class

    def set_set(self, new_set ):
        """ Sets neuron set """
        self.neuron_set = new_set
        
    def get_set(self):
        """ Gets neuron set """
        if self.neuron_set == None:
            raise ValueError
        return self.neuron_set
        
    def set_data(self, new_data):
        """ Sets neuron data or 'center' of knowledge """
        self.neuron_data = new_data
        
    def get_data(self, new_data):
        """ Gets neuron data or 'center' of knowledge """
        if self.neuron_data == None:
            raise ValueError
        return self.neuron_data
        
    def _calculate_manhattan_distance(self, pattern):
        """ Calculates Manhattan distance, private method """
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
    
    def recognize(self, pattern ):
        """ Returns true if neuron recognizes given pattern """
    	# If Manhattan distance to pattern is less than neuron radius
    	# there is a hit
        if self._calculate_manhattan_distance(pattern) < self.get_radius():
            self.hit = True
        else:
            self.hit = False
        # Return whether there has been a hit or not
        return self.hit
    
    def learn(self, pattern, class_, set_):
        """ Learns a new pattern (knowledge, data), return true if
        the pattern was succesfully learned and false in any other case """
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

 
    def reduce_radius_by(self, value ):
        """ Reduces neuron radius by 'value' """
        if value < 0 :
            raise ValueError("value must be positive")
        if self.radius < value :
            raise ValueError("value must be greater than radius of neuron")
        self.radius -= value