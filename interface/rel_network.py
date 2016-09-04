from rel_neuron import RelNeuron

import pickle


class RelNetwork:

    def __init__(self, neuron_count, name_file="NoFile"):
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
            if( self.neuron_list[index].has_ids(knowledge.get_h_id(), knowledge.get_s_id())):
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

    from rel_knowledge import RelKnowledge
    # Create network of size 1
    net = RelNetwork(1)
    print "Size ", net.get_neuron_count()

    # Create vector of knowledge
    k = [RelKnowledge("1",2,5), RelKnowledge(1,3,5), RelKnowledge(2,2), RelKnowledge(2,3)]

    # Learn and see how network size increases
    for e in k:
        net.learn(e)
        print "Size ", net.get_neuron_count()

    # Get all hearing relations with id == 1
    for e in net.get_hearing_rels("1"):
        print "Sight:", e.get_s_id()
        print "Weight: ", e.get_weight()
