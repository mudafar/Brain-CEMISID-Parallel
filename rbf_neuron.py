from math import fabs

class RbfNeuron:
    """ Radial Base Function neuron class """
    # Number of class instances
    nNum = 0
    # Size of data or knowledge in bytes
    DATA_SIZE = 4.0
    # Default radius
    DEFAULT_RADIUS = 0.5
    
    # Class constructor
    def __init__(self):
        # Neuron has no knowledge when created
        self.setHasKnowledge(False)
        # Neuron has default radius when created
        self.setRadius(RbfNeuron.DEFAULT_RADIUS)
        # Increment number of class instances
        RbfNeuron.nNum += 1
        
    """ Returns whether neuron has knowledge or not """
    def hasKnowledge(self):
        return self.hasKnowl
    
    """ Sets the has-knowledge (hasKnowl) internal flag """
    def setHasKnowledge(self, value ):
        self.hasKnowl = value
        
    """ Returns wheter neuron is memeber of set """
    def isMember(self, testSet):
        return (self.nSet == testSet)
        
    """ Sets neuron radius """
    def setRadius(self, nRadius):
        self.radius = nRadius
        
    """ Gets neuron radius """
    def getRadius(self):
        return self.radius
    
    """ Sets neuron class """
    def setClass(self, nClass ):
        self.nClass = nClass
        
    """ Gets neuron class """
    def getClass(self):
        if self.nClass == None:
            raise ValueError
        return self.nClass

    """ Sets neuron set """
    def setSet(self, nSet ):
        self.nSet = nSet
        
    """ Gets neuron set """
    def getSet(self):
        if self.nSet == None:
            raise ValueError
        return self.nSet
        
    """ Sets neuron data or 'center' of knowledge """
    def setData(self, data):
        self.data = data
        
    """ Gets neuron data or 'center' of knowledge """
    def getData(self, data):
        if self.data == None:
            raise ValueError
        return self.data
        
    """ Calculates Manhattan distance, private method """
    def _calcManhattanDist(self, pattern):
    	# Given pattern must be of size equal to DATA_SIZE
        if len(pattern) != RbfNeuron.DATA_SIZE:
            raise ValueError
        # Initialize distance atribute to zero
        self.distance = 0
        # Calculate Manhattan distance
        for index in range(len(pattern)):
            self.distance += fabs(self.data[index]-pattern[index])
        return self.distance
    
    """ Returns true if neuron recognizes given pattern """
    def recognize(self, pattern ):
    	# If Manhattan distance to pattern is less than neuron radius
    	# there is a hit
        if self._calcManhattanDist(pattern) < self.radius:
            self.hit = True
        else:
            self.hit = False
        return self.hit
    
    """ Learns a new pattern (knowledge, data), return true if
        the pattern was succesfully learned and false in any other case """
    def learn(self, pattern, class_, set_):
        # Tries to store pattern
        try:
            self.setData(pattern)
        except TypeError:
            print "pattern_ must be a list of integers"
            return False
        
        # Tries to store pattern class 
        try:
            self.setClass(class_)
        except TypeError:
            print "class_ must be a string"
            return False
            
        # Tries to store class set
        try:
             self.setSet(set_)
        except TypeError:
            print "set_ must be a string"
            return False
            
        # Indicate that this neuron has knowledge
        self.setHasKnowledge(True)
    """ Reduces neuron radius by 'value' """
    def reduceRadiusBy(self, value ):
        if value < 0 :
            raise ValueError("value must be positive")
        if self.radius < value :
            raise ValueError("value must be greater than radius of neuron")
        self.radius -= value
        
 # Some tests
if __name__ == '__main__':
	# Create neuron
    n1 = RbfNeuron()
    # Learn that the pattern [1,1,1,1] is of class 'cat' from the set
    # of animals
    n1.learn([1,1,1,1], "cat", "animal")
    
    # States whether the pattern can be recognized
    if n1.recognize([0.9,0.8,1,1]):
        print "I can recognize a " + n1.getClass() + ", which is a kind of " + n1.getSet()
    else:
        print "I can't recognize the given pattern"
    
    # States whether the pattern can be recognized
    if n1.recognize([0.9,0.8,1,0.9]):
        print "I can recognize a " + n1.getClass() + ", which is a kind of " + n1.getSet()
    else:
        print "I can't recognize the given pattern"
    
    # Reduces neuron radio
    n1.reduceRadiusBy(0.3)
    
    # States whether the pattern can be recognized
    if n1.recognize([0.9,0.8,1,0.9]):
        print "I can recognize a " + n1.getClass() + ", which is a kind of " + n1.getSet()
    else:
        print "I can't recognize the given pattern"
        
