from rbf_network import RbfNetwork
from rbf_knowledge import RbfKnowledge

class Bns:


    SIGHT_NEURON_COUNT = 100
    HEARING_NEURON_COUNT = 100

    def __init__(self, sight_bns_file="NoFile", hearing_bns_file="NoFile"):
        """Bns class constructor"""
        # Create sight neural blocks
        if (sight_bns_file != "NoFile"):
            self.bns_s = RbfNetwork.deserialize(sight_bns_file)
        else:
            self.bns_s = RbfNetwork(Bns.SIGHT_NEURON_COUNT)
        # Create hearing neural blocks
        if (hearing_bns_file != "NoFile"):
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

    def learn_sight(self, knowledge_h, pattern_s ):
        """ Learn hearing-sight patterns """
        self.bns_h.learn(knowledge_h)
        index_hearing = self.bns_h.get_last_learned_id()
        knowledge_s = RbfKnowledge(pattern_s, str(index_hearing) )
        return self.bns_s.learn(knowledge_s)

    def get_hearing_knowledge(self, pattern ):
        """ Return hearing knowledge related to given pattern,
        if recognized, and None in any other case """
        if self.bns_h.recognize(pattern) == "HIT":
            return self.bns_h.get_knowledge()
        return None

    def get_sight_knowledge(self, pattern ):
        """ Return sight knowledge related to given pattern,
         if recognized, and None in any other case """
        if self.bns_s.recognize(pattern) == "HIT":
            return self.bns_s.get_knowledge()
        return None

    def save(self, sight_bns_file, hearing_bns_file ):
        RbfNetwork.serialize(self.bns_s, sight_bns_file)
        RbfNetwork.serialize(self.bns_h, hearing_bns_file)
