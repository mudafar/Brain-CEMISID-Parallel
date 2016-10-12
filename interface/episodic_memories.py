import pickle

from cultural_network import CulturalNetwork,CulturalGroup,CulturalNeuron


class EpisodicMemoriesBlock(CulturalNetwork):

    def __init__(self):
        CulturalNetwork.__init__(self)

    def retrieve_memories(self, trigger_list):
        """ Return a list of memories (Cultural Groups) that contain the list of given
        memory triggers """
        # List of retrieved memories, initialized as and empty list
        retrieved_memories = []

        # For every trigger
        for trigger in trigger_list:
            # For every group (memory) in list of memories
            for group in self.group_list:
                # If the memory contains the given trigger
                if group.contains(trigger):
                    # Append the memory to list of retrieved memories
                    retrieved_memories.append(group)

        return retrieved_memories

    # Write methods for saving in hard disk

# Tests
if __name__ == '__main__':

    em = EpisodicMemoriesBlock()

    # Learn a set of memories related to school
    # and its given [B C F]

    em.bum()
    em.bip('pencil')
    em.bip('eraser')
    em.check('sharpener')
    bcf = [0.1, 1, 0.6]
    em.clack(bcf)

    em.bum()
    em.bip('board')
    em.bip('eraser')
    em.check('pupils')
    bcf = [0.5, 0.7, 0.4]
    em.clack(bcf)

    em.bum()
    em.bip('board')
    em.bip('notebook')
    em.check('pupils')
    bcf = [0.4, 0.7, 0.4]
    em.clack(bcf)

    # Test memories retrieval
    print "Retrieving memories related to 'house' "
    if len(em.retrieve_memories(['house'])) == 0:
        print "No memories found"
    else:
        for memory in em.retrieve_memories(['house']):
            for episode in memory:
                print episode.get_knowledge()

    print "Retrieving memories related to 'eraser'"
    if len(em.retrieve_memories(['eraser'])) == 0:
        print "No memories found"
    else:
        for memory in em.retrieve_memories(['eraser']):
            for episode in memory.group:
                print episode.get_knowledge()

    print "Retrieving memories related to 'board and eraser'"
    if len(em.retrieve_memories(['board', 'eraser'])) == 0:
        print "No memories found"
    else:
        for memory in em.retrieve_memories(['board', 'eraser']):
            for episode in memory.group:
                print episode.get_knowledge()