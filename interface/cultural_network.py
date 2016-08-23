

class CulturalNeuron:
    def __init__(self, knowledge=None):
        if knowledge == None:
            self._has_knowledge = False
            self._knowledge = None
        else:
            self.set_knowledge(knowledge)
        return

    def set_knowledge(self, knowledge):
        self._has_knowledge = True
        self._knowledge = knowledge

    def get_knowledge(self):
        return self._knowledge

    def has_knowledge(self):
        return self._has_knowledge


class CulturalGroup:
    def __init__(self):
        """ CulturalGroup class constructor """
        self._group = []
        self._index_bip = 0

    def learn(self, knowledge):
        """ Learn new piece of cultural knowledge as part of the cultural group
        :param knowledge: Object of type CulturalKnowledge. Knowledge to be learned
        """
        self._group.append(CulturalNeuron(knowledge))

    def bum(self, knowledge):
        """ Compare given knowledge with the one stored in the head neuron of the group,
            return True if equal, False in any other case
        :param knowledge: Piece of cultural knowledge to be compared
        :return: Boolean
        """
        # Reinitialize bip index
        self._index_bip = 0
        if len(self._group) > 0:
            return self._group[0].get_knowledge() == knowledge
        return False

    def bip(self, knowledge):
        # Increase bip index
        self._index_bip += 1
        if (self._index_bip+1) < len(self._group):
            return self._group[self._index_bip].get_knowledge() == knowledge
        self._index_bip = 0
        return False

    def check(self, knowledge):
        return self.bip(knowledge) and (len(self._group)-1) == (self._index_bip+1)

    def clack(self, knowledge):
        """ Learn new piece of cultural knowledge as part of the cultural group
        :param knowledge: Object of type CulturalKnowledge. Knowledge to be learned
        """
        self.learn(knowledge)

    def get_tail_knowledge(self):
        return self._group[len(self._group)].get_knowledge()

    def reinit(self):
        self._group = []
        self._index_bip = 0


class CulturalNetwork:
    def __init__(self, group_count=1):
        """ CulturalNetwork class constructor """
        self.group_list = []
        for index in range(group_count):
            self.group_list.append(CulturalGroup())
        self._index_ready_to_learn = 0
        self._clack = False
        self._recognized_indexes = []

    def bum(self, knowledge):
        # Renintialize ready lo learn group
        self.group_list[self._index_ready_to_learn].reinit()
        # Indexes of neural groups that recognized bum
        self._recognized_indexes = []
        for group_index in range(self._index_ready_to_learn):
            if self.group_list[group_index].bum(knowledge):
                self._recognized_indexes.append(group_index)
        # Learn in ready to learn neuron
        self.group_list[self._index_ready_to_learn].learn(knowledge)

    def bip(self, knowledge):
        # Indexes
        bip_indexes = []
        for group_index in self._recognized_indexes:
            if self.group_list[group_index].bip(knowledge):
                bip_indexes.append(group_index)
        # Store bip_indexes in instance attribute _recognized_indexes
        self._recognized_indexes = bip_indexes
        # Learn in ready to learn neuron
        self.group_list[self._index_ready_to_learn].learn(knowledge)

    def check(self, knowledge):
        # Indexes
        check_indexes = []
        for group_index in self._recognized_indexes:
            if self.group_list[group_index].check(knowledge):
                check_indexes.append(group_index)
        self._recognized_indexes = check_indexes
        # If no group has the knowledge related to the given sequence, keep learning
        if len(check_indexes) == 0:
            # Learn
            self.group_list[self._index_ready_to_learn].learn(knowledge)
            # Enable clack
            self._clack = True
            return None
        elif len(check_indexes) == 1:
            # Do not learn
            self.group_list[self._index_ready_to_learn].reinit()
            # Return index of neuron that has recognized the process
            return check_indexes[0]
        else:
            raise AttributeError("CulturalNet net has an inconsistent state")

    def clack(self, knowledge):
        if not self._clack:
            return
        # Learn
        self.group_list[self._index_ready_to_learn].learn(knowledge)
        self._clack = False
        self._index_ready_to_learn += 1

    def get_tail_knowledge(self, group_id):
        return self.group_list[group_id].get_tail_knowledge()


# Tests
if __name__ == '__main__':

    net = CulturalNetwork(5)

    net.bum("c")
    net.check("a")
    net.clack("ca")

    net.bum("b")
    net.check("a")
    net.clack("ba")

    net.bum("l")
    net.bip("l")
    net.check("o")
    net.clack("llo")

    net.bum("c")
    net.check("a")
    net.clack("Ka")

    i = 1


