import pickle

from unconscious_filtering_block import UnconsciousFilteringBlock
from conscious_decisions_block import ConsciousDecisionsBlock

class DecisionsBlock:

    def __init__(self):
        # Ports
        self.input_memories = None
        self.conscious_output = None
        self.unconscious_output = None
        self.internal_state = None
        self.desired_state = None

        self.unconscious_block = UnconsciousFilteringBlock()
        self.conscious_block = ConsciousDecisionsBlock()

    def set_input_memories(self, input_memories):
        self.input_memories = input_memories

    def set_internal_state(self, internal_state ):
        self.internal_state = internal_state

    def set_desired_state(self, desired_state ):
        self.desired_state = desired_state

    def get_output_memory(self):
        self.unconscious_block.set_internal_state(self.internal_state)
        self.unconscious_block.set_desired_state(self.desired_state)
        self.unconscious_block.set_inputs(self.input_memories)
        self.unconscious_output = self.unconscious_block.get_outputs()
        self.conscious_block.set_desired_state(self.desired_state)
        self.conscious_block.set_internal_state(self.internal_state)
        conscious_inputs = []
        for memory in self.unconscious_output:
            conscious_inputs.append(memory.get_tail_knowledge())
        self.conscious_block.set_inputs(conscious_inputs)
        conscious_output_index = self.conscious_block.get_decision()
        self.conscious_output = self.unconscious_output[conscious_output_index]
        return self.conscious_output

# Tests
if __name__ == '__main__':
    from cultural_network import CulturalGroup
    from internal_state import InternalState,BiologyCultureFeelings

    # Memories
    MEMORIES_COUNT = 6
    memories = [CulturalGroup() for i in range(MEMORIES_COUNT)]
    import random

    bcf = []
    for i in range(MEMORIES_COUNT):
        memories[i].bum()
        memories[i].learn(i)
        bcf.append(BiologyCultureFeelings())
        new_state = [random.random(), random.random(), random.random()]
        bcf[i].set_state(new_state)
        memories[i].clack(bcf[i])
        print "Memory ", i, " bcf is", memories[i].get_tail_knowledge().get_state()

    d_block = DecisionsBlock()
    internal_state = InternalState()
    internal_state.set_state([0.5, 1, 1])
    d_block.set_internal_state(internal_state)
    desired_state = InternalState()
    desired_state.set_state([0.5, 1, 1])
    d_block.set_desired_state(desired_state)
    d_block.set_input_memories(memories)
    output = d_block.get_output_memory()
    print "Decisions Block output is ", output.get_tail_knowledge().get_state()
    print "made by ", d_block.conscious_block.get_last_decision_type()
    print "Unconscious decisions "
    for mem in d_block.unconscious_output:
        print mem.get_tail_knowledge().get_state()