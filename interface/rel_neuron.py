from rel_knowledge import RelKnowledge

class RelNeuron:

    def __init__(self):
        """ Create RelNeuron instance """
        self._hit = False
        self._has_knowledge = False

    def learn(self, knowledge):
        """ Set knowledge of type RelKnowledge """
        if isinstance(knowledge, RelKnowledge):
            self._knowledge = knowledge
            self._has_knowledge = True
        else:
            raise ValueError("value must be of type RelKnowledge")


    def recognize_hearing(self, h_id ):
        """ Return true if h_id is recognized as the hearing-id part of the relational knowledge.
         Also set an internal flag to indicate whether the last recognition process was successful (True)
         or not (False). The value of the internal flag is accessible through the is_hit() method """
        if self.has_knowledge():
            self._hit = self._knowledge.is_equal_hearing(h_id)
        return self._hit

    def recognize_sight(self, s_id ):
        """ Return true if s_id is recognized as the sight-id part of the relational knowledge.
         Also set an internal flag to indicate whether the last recognition process was successful (True)
         or not (False). The value of the internal flag is accessible through the is_hit() method """
        if self.has_knowledge():
            self._hit = self._knowledge.is_equal_sight(s_id)
        return self._hit

    def get_h_id(self):
        """ Return hearing id if neuron has knowledge and an object of type None in any other case """
        if self.has_knowledge():
            # Increase weight everytime that the relation is somehow used
            self._knowledge.increase_weight()
            return self._knowledge.get_h_id()
        return None

    def get_s_id(self):
        """ Return sight id if neuron has knowledge and an object of type None in any other case """
        if self.has_knowledge():
            # Increase weight everytime that the relation is somehow used
            self._knowledge.increase_weight()
            return self._knowledge.get_s_id()
        return None

    def get_knowledge(self):
        """ Returns knowledge stored by neuron if neuron has knowledge,
        and None object in any other case """
        if self.has_knowledge():
            # Increase weight everytime that the relation is somehow used
            self._knowledge.increase_weight()
            return self._knowledge
        return None

    def get_weight(self):
        """ Return weight of relation if neuron has knowledge and an object of type None in any other case """
        if self.has_knowledge():
            return self._knowledge.get_weight()
        return None

    def set_h_id(self, h_id ):
        """ Set hearing id if neuron has knowledge. Raise an exception of type AttributeError if an attempt to
         set the hearing id to a neuron with no previous knowledge is made """
        if self.has_knowledge():
            self._knowledge.set_h_id(h_id)
        else:
            raise AttributeError("neuron has no knowledge")

    def set_s_id(self, s_id):
        """ Set sight id if neuron has knowledge. Raise an exception of type AttributeError if an attempt to
         set the sight id to a neuron with no previous knowledge is made """
        if self.has_knowledge():
            self._knowledge.set_s_id(s_id)
        else:
            raise AttributeError("neuron has no knowledge")

    def has_knowledge(self):
        """ Return true if the neuron has already learned some relational knowledge (RelKnowledge)
        and false in any other case """
        return self._has_knowledge

    def has_ids(self, h_id, s_id ):
        """ Return true if neuron has h_id and s_id as hearing and sight ids respectively """
        return self._knowledge.is_equal(h_id, s_id)

# Tests
if __name__ == '__main__':
    k1 = RelKnowledge(0,0,0)

    n1 = RelNeuron()

    print "N1 has knowledge: ", n1.has_knowledge()

    n1.learn(k1)

    print "N1 has knowledge: ", n1.has_knowledge()

    print "Neuron h_id ", n1.get_h_id()
    print "Neuron s_id ", n1.get_s_id()
    print "Neuron w ", n1.get_weight()

    n1.set_h_id(5)
    n1.set_s_id(-1)

    print "Neuron h_id ", n1.get_h_id()
    print "Neuron s_id ", n1.get_s_id()
    print "Neuron w ", n1.get_weight()
