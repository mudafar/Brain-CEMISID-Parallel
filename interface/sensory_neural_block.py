from rbf_network import RbfKnowledge, RbfNetwork


class SensoryNeuralBlock:

    SIGHT_NEURON_COUNT = 100
    HEARING_NEURON_COUNT = 100

    def __init__(self, sight_snb_file="NoFile", hearing_snb_file="NoFile"):
        """SNB class constructor"""
        # Create sight neural blocks
        if sight_snb_file != "NoFile":
            self.snb_s = RbfNetwork.deserialize(sight_snb_file)
        else:
            self.snb_s = RbfNetwork(SensoryNeuralBlock.SIGHT_NEURON_COUNT)
        # Create hearing neural blocks
        if hearing_snb_file != "NoFile":
            self.snb_h = RbfNetwork.deserialize(hearing_snb_file)
        else:
            self.snb_h = RbfNetwork(SensoryNeuralBlock.SIGHT_NEURON_COUNT)
        self._last_learned_ids = None

    def recognize_sight(self, pattern ):
        """ Return true if sight neural block recognizes
            given pattern """
        return self.snb_s.recognize(pattern)

    def recognize_hearing(self, pattern ):
        """ Return true if hearing neural block recognizes
                    given pattern """
        return self.snb_h.recognize(pattern)

    def learn_hearing(self, knowledge ):
        """ Learn hearing knowledge """
        return self.snb_h.learn(knowledge)

    def learn_sight(self, knowledge ):
        """ Learn sight knowledge """
        return self.snb_s.learn(knowledge)

    def learn(self, knowledge_h, pattern_s ):
        """ Learn hearing-sight patterns """
        # If hearing knowledge learned
        if self.snb_h.learn(knowledge_h):
            # Get index of hearing neuron that has learned
            index_hearing = self.snb_h.get_last_learned_id()
            # Relate sight pattern and index of hearing neuron in just one piece of RbfKnowledge
            knowledge_s = RbfKnowledge(pattern_s, str(index_hearing) )
            # Learn, get learn status (True, False)
            learned = self.snb_s.learn(knowledge_s)
            # Get index of sight neuron that has learned
            index_sight = self.snb_s.get_last_learned_id()
            if learned:
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

    def get_hearing_knowledge(self, pattern_or_id, is_id=False):
        """ Return hearing knowledge related to given pattern or neuron id,
        if pattern or neuron_id in hearing network, and None in any other case """
        # If given parameter pattern_or_id is id
        if is_id:
            neuron_id = pattern_or_id
            # If there is a neuron with corresponding id
            if neuron_id <= self.snb_h.get_last_learned_id():
                # If the neuron is not degraded
                if not self.snb_h.neuron_list[neuron_id].is_degraded():
                    # Return pattern
                    return self.snb_h.neuron_list[neuron_id].get_knowledge()
            return None
        else:
            pattern = pattern_or_id
            if self.snb_h.recognize(pattern) == "HIT":
                return self.snb_h.get_knowledge()
            return None

    def get_sight_knowledge(self, pattern_or_id, is_id=False):
        """ Return hearing knowledge related to given pattern or neuron id,
        if pattern or neuron_id in sight network, and None in any other case """
        # If given parameter pattern_or_id is id
        if is_id:
            neuron_id = pattern_or_id
            # If there is a neuron with corresponding id
            if neuron_id < self.snb_s.get_index_ready_to_learn():
                # If the neuron is not degraded
                if not self.snb_s.neuron_list[neuron_id].is_degraded():
                    # Return pattern
                    return self.snb_s.neuron_list[neuron_id].get_knowledge()
            return None
        else:
            pattern = pattern_or_id
            if self.snb_s.recognize(pattern) == "HIT":
                return self.snb_s.get_knowledge()
            return None

    def save(self, sight_snb_file, hearing_snb_file):
        RbfNetwork.serialize(self.snb_s, sight_snb_file)
        RbfNetwork.serialize(self.snb_h, hearing_snb_file)
