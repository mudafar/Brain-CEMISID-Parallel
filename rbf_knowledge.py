from math import fabs

class RbfKnowledge:
    # Size of data or knowledge in bytes
    PATTERN_SIZE = 4.0
    
    def __init__(self, rbf_pattern, rbf_class, rbf_set):
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
        
    def calc_manhattan_distance(self, pattern_or_knowledge ):
        """ Returns Manhattan distance from this piece of 
        knowledge to a given pattern """
        
        # If given parameter is of class knowledge, obtain pattern
        try:
            pattern = pattern_or_knowledge._pattern
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
            distance += fabs(self._pattern[index]-pattern[index])
        # Return distance
        return distance