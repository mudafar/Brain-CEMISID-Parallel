import pickle

from neuron import Neuron


class RelKnowledge:

    def __init__(self, h_id, s_id, weight=0):
        """ Create RelKnowledge instance given
        a hearing id (id_h), sight id (id_s) and weight which defaults to zero"""
        self.set_h_id(h_id)
        self.set_s_id(s_id)
        self.set_weight(weight)

    def set_h_id(self, h_id):
        """ Set hearing id """
        self._h_id = h_id

    def set_s_id(self, s_id):
        """ Set sight id """
        self._s_id = s_id

    def set_weight(self, w):
        """ Set weight """
        if w >= 0:
            self._weight = w
        else:
            raise ValueError("Invalid value for w")

    def increase_weight(self, amount=1):
        """ Increase weight of relation by the amount given as a parameter. The default amount value is 1 """
        if self._weight + amount >= 0:
            self._weight += amount

    def get_h_id(self):
        """ Get hearing id """
        return self._h_id

    def get_s_id(self):
        """ Get sight id """
        return self._s_id

    def get_weight(self):
        """ Get relation weight """
        return self._weight

    def is_equal_hearing(self, h_id):
        """ Return true if knowledge's hearing id is equal to given parameter h_id and
        false in any other case """
        return self._h_id == h_id

    def is_equal_sight(self, s_id):
        """ Return true if knowledge sight id is equal to given parameter s_id and
        false in any other case """
        return self._s_id == s_id

    def is_equal(self, h_id, s_id):
        """ Return true if knowledge's sight id is equal to given parameter s_id and
                knowledge's hearing id is equal to given parameter h_id. Return false in any other case """
        return self._h_id == h_id and self._s_id == s_id


class RelNeuron(Neuron):

    def __init__(self):
        super(RelNeuron, self).__init__()
        """ Create RelNeuron instance """
        self._hit = False

    def learn(self, knowledge):
        """ Set knowledge of type RelKnowledge """
        if isinstance(knowledge, RelKnowledge):
            self._knowledge = knowledge
            self._has_knowledge = True
        else:
            raise ValueError("value must be of type RelKnowledge")

    def set_knowledge(self, knowledge):
        self.learn(knowledge)

    def recognize_hearing(self, h_id):
        """ Return true if h_id is recognized as the hearing-id part of the relational knowledge.
         Also set an internal flag to indicate whether the last recognition process was successful (True)
         or not (False). The value of the internal flag is accessible through the is_hit() method """
        if self.has_knowledge():
            self._hit = self._knowledge.is_equal_hearing(h_id)
        return self._hit

    def recognize_sight(self, s_id):
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

    def set_h_id(self, h_id):
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

    def has_ids(self, h_id, s_id):
        """ Return true if neuron has h_id and s_id as hearing and sight ids respectively """
        return self._knowledge.is_equal(h_id, s_id)


class RelNetwork:

    def __init__(self, neuron_count):
        """ Class constructor, takes 'neuron_count' as parameter
                for setting network size """
        # Create neuron list
        self.neuron_list = []
        # Fill neuron list with nre RelNeuron instances
        for index in range(neuron_count):
            self.neuron_list.append(RelNeuron())
        # Index of ready to learn neuron
        self._index_ready_to_learn = 0

    def learn(self, knowledge):
        """ Learn new knowledge in ready-to-learn neuron """
        # If there is no capacity in neuron list, double size
        if self._index_ready_to_learn == (len(self.neuron_list)-1):
            new_list = []
            # Fill neuron list with nre RelNeuron instances
            for index in range(len(self.neuron_list)):
                new_list.append(RelNeuron())
            self.neuron_list = self.neuron_list + new_list
        # Check for neurons that already have given knowledge ids
        for index in range(self._index_ready_to_learn):
            if self.neuron_list[index].has_ids(knowledge.get_h_id(), knowledge.get_s_id()):
                return False
        # If there are no neurons with given pair of ids, learn
        self.neuron_list[self._index_ready_to_learn].learn(knowledge)
        self._index_ready_to_learn += 1
        return True

    def get_hearing_rels(self, h_id):
        """ Return a list of all knowledge in net such that it has parameter h_id as hearing id """
        # List of hearing relations
        hearing_rels = []
        for index in range(self._index_ready_to_learn):
            if self.neuron_list[index].recognize_hearing(h_id):
                hearing_rels.append(self.neuron_list[index].get_knowledge())
        return hearing_rels

    def get_sight_rels(self, s_id):
        """ Return a list of all knowledge in net such that it has parameter s_id as sight id """
        # List of sight relations
        sight_rels = []
        for index in range(self._index_ready_to_learn):
            if self.neuron_list[index].recognize_sight(s_id):
                sight_rels.append(self.neuron_list[index].get_knowledge())
        return sight_rels

    def get_neuron_count(self):
        """ Returns number of neurons in network """
        return len(self.neuron_list)

    @classmethod
    def serialize(cls, obj, name):
        pickle.dump(obj, open(name, "wb"))

    @classmethod
    def deserialize(cls, name):
        return pickle.load(open(name, "rb"))


# Tests
if __name__ == '__main__':

    k1 = RelKnowledge(0, 0, 0)

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

    # Create network of size 1
    net = RelNetwork(1)
    print "Size ", net.get_neuron_count()

    # Create vector of knowledge
    k = [RelKnowledge("1", 2, 5), RelKnowledge(1, 3, 5), RelKnowledge(2, 2), RelKnowledge(2, 3)]

    # Learn and see how network size increases
    for e in k:
        net.learn(e)
        print "Size ", net.get_neuron_count()

    # Get all hearing relations with id == 1
    for e in net.get_hearing_rels("1"):
        print "Sight:", e.get_s_id()
        print "Weight: ", e.get_weight()
