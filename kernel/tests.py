# Import rbf_neuron class
from rbf_neuron import RbfNeuron
# Import rbf_knowledge class
from rbf_knowledge import RbfKnowledge

 # Some tests
if __name__ == '__main__':
	# Create neuron
    n1 = RbfNeuron()
    # Learn that the pattern [1,1,1,1] is of class 'cat' from the set
    # of animals
    k1 = RbfKnowledge([1,1,1,1], "cat", "animal");
    
    n1.learn(k1)
    
    # States whether the pattern can be recognized
    if n1.recognize([0.9,0.8,1,1]):
        print "I can recognize a " + n1.get_class() + ", which is a kind of " + n1.get_set()
    else:
        print "I can't recognize the given pattern"
    
    # States whether the pattern can be recognized
    if n1.recognize([0.9,0.8,1,0.9]):
        print "I can recognize a " + n1.get_class() + ", which is a kind of " + n1.get_set()
    else:
        print "I can't recognize the given pattern"
    
    # Reduces neuron radio
    n1.reduce_radius_by(0.3)
    
    # States whether the pattern can be recognized
    if n1.recognize([0.9,0.8,1,0.9]):
        print "I can recognize a " + n1.get_class() + ", which is a kind of " + n1.get_set()
    else:
        print "I can't recognize the given pattern"
        