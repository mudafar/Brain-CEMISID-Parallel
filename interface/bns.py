from rbf_network import RbfNetwork
from rbf_knowledge import RbfKnowledge

class Bns:


    SIGHT_NEURON_COUNT = 100
    HEARING_NEURON_COUNT = 100

    def __init__(self, sight_bns_file="NoFile", hearing_bns_file="NoFile"):
        """Bns class constructor"""
        # Create sight neural blocks
        if sight_bns_file != "NoFile":
            self.bns_s = RbfNetwork.deserialize(sight_bns_file)
        else:
            self.bns_s = RbfNetwork(Bns.SIGHT_NEURON_COUNT)
        # Create hearing neural blocks
        if hearing_bns_file != "NoFile":
            self.bns_h = RbfNetwork.deserialize(hearing_bns_file)
        else:
            self.bns_h = RbfNetwork(Bns.SIGHT_NEURON_COUNT)

    def recognize_sight(self, pattern ):
        """ Return true if sight neural block recognizes
            given pattern """
        return self.bns_s.recognize(pattern)

    def recognize_hearing(self, pattern ):
        """ Return true if hearing neural block recognizes
                    given pattern """
        return self.bns_h.recognize(pattern)

    def learn_hearing(self, knowledge ):
        """ Learn hearing knowledge """
        return self.bns_h.learn(knowledge)

    def learn_sight(self, knowledge ):
        """ Learn sight knowledge """
        return self.bns_s.learn(knowledge)

    def learn(self, knowledge_h, pattern_s ):
        """ Learn hearing-sight patterns """
        # If hearing knowledge learned
        if self.bns_h.learn(knowledge_h):
            # Get index of hearing neuron that has learned
            index_hearing = self.bns_h.get_last_learned_id()
            # Relate sight pattern and index of hearing neuron in just one piece of RbfKnowledge
            knowledge_s = RbfKnowledge(pattern_s, str(index_hearing) )
            # Learn, get learn status (True, False)
            learned = self.bns_s.learn(knowledge_s)
            # Get index of sight neuron that has learned
            index_sight = self.bns_s.get_last_learned_id()
            if( learned ):
                # Store indexes of hearing and sight neurons that just learned
                self._last_learned_ids = (index_hearing, index_sight )
            # Return sight learning state
            return learned
        # Could not learn hearing knowledge
        return False

    def get_last_learned_ids(self):
        """ Return a 2-tuple of integeres representing the ids of hearing and sight neurons
            that learned in the las learn_sight() process """
        return self._last_learned_ids

    def get_hearing_knowledge(self, pattern_or_id, is_id=False ):
        """ Return hearing knowledge related to given pattern or neuron id,
        if pattern or neuron_id in hearing network, and None in any other case """
        # If given parameter pattern_or_id is id
        if is_id:
            neuron_id = pattern_or_id
            # If there is a neuron with corresponding id
            if neuron_id <= self.bns_h.get_last_learned_id():
                # If the neuron is not degraded
                if not self.bns_h.neuron_list[neuron_id].is_degraded():
                    # Return pattern
                    return self.bns_h.neuron_list[neuron_id].get_knowledge()
            return None
        else:
            pattern = pattern_or_id
            if self.bns_h.recognize(pattern) == "HIT":
                return self.bns_h.get_knowledge()
            return None

    def get_sight_knowledge(self, pattern_or_id, is_id=False ):
        """ Return hearing knowledge related to given pattern or neuron id,
        if pattern or neuron_id in sight network, and None in any other case """
        # If given parameter pattern_or_id is id
        if is_id:
            neuron_id = pattern_or_id
            # If there is a neuron with corresponding id
            if neuron_id < self.bns_s.get_index_ready_to_learn():
                # If the neuron is not degraded
                if not self.bns_s.neuron_list[neuron_id].is_degraded():
                    # Return pattern
                    return self.bns_s.neuron_list[neuron_id].get_knowledge()
            return None
        else:
            pattern = pattern_or_id
            if self.bns_s.recognize(pattern) == "HIT":
                return self.bns_s.get_knowledge()
            return None

    def save(self, sight_bns_file, hearing_bns_file ):
        RbfNetwork.serialize(self.bns_s, sight_bns_file)
        RbfNetwork.serialize(self.bns_h, hearing_bns_file)
