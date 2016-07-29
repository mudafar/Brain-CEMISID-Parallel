
from rbf_knowledge import RbfKnowledge

class RbfNeuron:
    """ Radial Base Function neuron class """
    # Number of class instances
    instances_count = 0
    # Default radius
    DEFAULT_RADIUS = 0.5
    
    # Class constructor
    def __init__(self):
        # Neuron has no knowledge when created
        self._has_knowledge = False
        # Neuron has default radius when created
        self.set_radius(RbfNeuron.DEFAULT_RADIUS)
        # Increment number of class instances
        RbfNeuron.instances_count += 1
        
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
        if( self.has_knowledge() ):
            return self._knowledge
        else:
            return None
            
    def get_class(self):
        """ Returns class of knowledge if neuron has 
        knowledge, and None in any other case """
        if( self.has_knowledge() ):
            return self._knowledge.get_class()
        else:
           return None 

    def get_set(self):
        """ Returns set of knowledge if neuron has 
        knowledge, and None in any other case """
        if( self.has_knowledge() ):
            return self._knowledge.get_set()
        else:
           return None     
    
    def get_pattern(self):
        """ Returns set of knowledge if neuron has 
        knowledge, and None in any other case """
        if( self.has_knowledge() ):
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
    
    def recognize(self, pattern ):
        """ Returns true if neuron recognizes given pattern """
    	# If Manhattan distance to pattern is less than neuron radius
    	# there is a hit
        if self._knowledge.calc_manhattan_distance(pattern) < self.get_radius():
            self._hit = True
        else:
            self._hit = False
        # Return whether there has been a hit or not
        return self._hit

    def reduce_radius_by(self, value ):
        """ Reduces neuron radius by 'value' """
        if value < 0 :
            raise ValueError("value must be positive")
        if self._radius < value :
            raise ValueError("value must be greater than radius of neuron")
        self._radius -= value
        
    def increase_radius_by(self, value):
        """ Increases neuron radius by 'value' """
        if value < 0 :
            raise ValueError("value must be positive")
        self._radius += value