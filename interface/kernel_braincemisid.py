# Brain-CEMISID kernel imports
from rbf_network import RbfKnowledge, RbfNeuron, RbfNetwork
from rel_network import RelKnowledge, RelNeuron, RelNetwork
from analytical_neuron import AnalyticalNeuron
from cultural_network import CulturalNetwork
from sensory_neural_block import SensoryNeuralBlock
from geometric_neural_block import GeometricNeuralBlock
from internal_state import InternalState, BiologyCultureFeelings
from episodic_memories import EpisodicMemoriesBlock
from decisions_block import DecisionsBlock


class KernelBrainCemisid:

    def __init__(self):
        grid_size = 16
        # HEURISTICS: radius = (1/3)*2^(ENCODING_SIZE)
        # where ENCODING_SIZE is bit size of every pattern element (8 bits for us)
        radius = 24
        # Calculate pattern size based on grid_size and size of a Nibble (4)
        pattern_size = pow(grid_size, 2) / 4
        # Set neural network data size
        RbfNetwork.PATTERN_SIZE = pattern_size
        # Set neural network default radius
        RbfNetwork.DEFAULT_RADIUS = radius
        # Set pattern size in RBF knowledge
        RbfKnowledge.PATTERN_SIZE = pattern_size

        #self.erase_all_knowledge()

        # SNB
        self.snb = SensoryNeuralBlock("sight_snb.p", "hearing_snb.p")
        # Relational Neural Block
        self.rnb = RelNetwork.deserialize("rnb.p")
        # Analytical neuron
        self.analytical_n = AnalyticalNeuron()
        # Addition by memory network
        self.am_net = CulturalNetwork.deserialize("am_net.p")
        # Geometric Neural Block
        self.gnb = GeometricNeuralBlock.deserialize("gnb.p")
        # Syllables net
        self.syllables_net = CulturalNetwork.deserialize("syllables_net.p")
        # Words net
        self.words_net = CulturalNetwork.deserialize("words_net.p")
        # Sight-Syllables rel network
        self.ss_rnb = RelNetwork.deserialize("ss_rnb.p")

        #################### INTENTIONS MODULES ########################################################################
        self.episodic_memory = EpisodicMemoriesBlock.deserialize("episodic_memory.p")
        self.decisions_block = DecisionsBlock()

        self.internal_state = InternalState()
        self.desired_state = InternalState([0.5,1,1])

        # Internal state "Ports" (Three components real valued vector)
        self._internal_state_in = None

        # Memory that stores short term bip inputs for making a decision
        self._intentions_short_term_memory = []
        self._output_memory = None
        ################################################################################################################

        # _bbcc_words
        self._learning_words = False
        self._learning_syllables = False
        self._enable_bbcc = False

        # Output "ports" (related to senses)
        self.s_knowledge_out = None
        self.h_knowledge_out = None

        # Input "ports" (senses)
        self.s_knowledge_in = None
        self.h_knowledge_in = None

        self._working_domain = "ADDITION"
        self.state = "MISS"

    def set_working_domain(self, domain):
        """ Sets a working domain for the bbcc protocol. It could be either "READING" or "ADDITION"
        :param domain: enum { "READING", "ADDITION", "COUNTING" }
        """
        if(domain != "READING" and domain != "ADDITION" and domain != "COUNTING"
                and domain != "EPISODES" and domain != "INTENTIONS"):
            return
        self._working_domain = domain

    def get_working_domain(self):
        """ Get bbcc protocol working domain
        :return: enum { "READING", "ADDITION", "COUNTING", "EPISODES", "INTENTIONS" }
        """
        return self._working_domain

    def set_sight_knowledge_in(self, knowledge):
        self.s_knowledge_in = knowledge

    def get_sight_knowledge_in(self):
        return self.s_knowledge_in

    def set_hearing_knowledge_in(self, knowledge):
        self.h_knowledge_in = knowledge

    def get_hearing_knowledge_in(self):
        return self.h_knowledge_in

    def get_sight_knowledge_out(self):
        return self.s_knowledge_out

    def get_hearing_knowledge_out(self):
        return self.h_knowledge_out

    ################### INTENTIONS CODE ################################################################################
    def set_internal_state_in(self, states_vector ):
        self._internal_state_in = states_vector

    def set_internal_state(self, states_vector ):
        """ Set internal state (Biology, Culture and Feelings)
        :param states_vector: three components vector: [Biology, Culture, Feelings].
         All components are in the real interval [0,1]
        :return: True if state properly set, False in any other case.
        """
        state_correctly_set = self.internal_state.set_state(states_vector)
        if state_correctly_set:
            self.decisions_block.set_internal_state(self.internal_state.get_state())
        return state_correctly_set

    def get_internal_state(self):
        return self.internal_state

    def feed_internal_state(self, states_vector ):
        state_correctly_fed = self.internal_state.average_state(states_vector)
        if state_correctly_fed:
            self.decisions_block.set_internal_state(self.internal_state.get_state())
        return state_correctly_fed

    def set_desired_state(self, states_vector ):
        """ Set desired state (Biology, Culture and Feelings)
        :param states_vector: three components vector: [Biology, Culture, Feelings].
         All components are in the real interval [0,1]
        :return: True if state properly set, False in any other case.
        """
        state_correctly_set = self.desired_state.set_state(states_vector)
        if state_correctly_set:
            self.decisions_block.set_desired_state(self.desired_state.get_state())
        return state_correctly_set

    def get_desired_state(self):
        return self.desired_state
    ####################################################################################################################

    def disable_bbcc(self):
        """ Disable bbcc protocol so that Check and Clack can be used as standalone actions """
        self._enable_bbcc = False

    def bum(self):
        """ Start bbcc protocol """
        # Enable check and clack as a part of bbcc protocol
        # preventing their effect as standalone actions
        self._enable_bbcc = True
        # Clean outputs
        self.s_knowledge_out = []
        self.h_knowledge_out = []
        # If working in the domain of READING
        # transmit bum signal to words networks
        if self._working_domain == "READING":
            self._bum_words()
        # Transmit it to addition networks
        elif self._working_domain == "ADDITION":
            self._bum_addition()
        # Else, transmit it to counting net
        elif self._working_domain == "COUNTING":
            self._bum_counting()
        #################### INTENTIONS ################################################################################
        # Else, episodic memory
        elif self._working_domain == "EPISODES":
            self._bum_episodes()
        # Intentions
        else:
            self._bum_intentions()

    def bip(self):
        """ Bip part of bbcc protocol (See bbcc protocol description) """
        # If protocol is not enabled, do nothing
        if not self._enable_bbcc:
            return
        # Clean outputs
        self.s_knowledge_out = []
        self.h_knowledge_out = []
        # Recognize given sight pattern
        self.state = self.snb.recognize_sight(self.s_knowledge_in.get_pattern())
        # If pattern is recognized, proceed with bbcc protocol
        if self.state == "HIT":
            # If currently working with words, send bip signal to words networks
            if self._working_domain == "READING":
                self._bip_words()
            # Send bip signal to addition networks (AM and GNB)
            elif self._working_domain == "ADDITION":
                self._bip_addition()
            # Else, transmit it to counting net
            elif self._working_domain == "COUNTING":
                self._bip_counting()
            #################### INTENTIONS ################################################################################
            # Else, episodic memory
            elif self._working_domain == "EPISODES":
                self._bip_episodes()
            else:
                self._bip_intentions()

    def check(self):
        """ Check if there is knowledge associated with the given sequence of patterns from
            bbcc protocol when self._enable_bbcc is True. Check if the Sensory Neural Block recognizes the
            given pattern when self._enable_bbcc is False """
        # Clean outputs
        self.s_knowledge_out = []
        self.h_knowledge_out = []
        # Part of complete bbcc protocol
        if self._enable_bbcc:
            self.state = self.snb.recognize_sight(self.s_knowledge_in.get_pattern())
            # If pattern is recognized, proceed with bbcc protocol
            if self.state == "HIT":
                if self._working_domain == "READING":
                    self._check_words()
                # Send bip signal to addition networks (AM and GNB)
                elif self._working_domain == "ADDITION":
                    self._check_addition()
                #################### INTENTIONS ################################################################################
                # Else, episodic memory
                elif self._working_domain == "EPISODES":
                    self._check_episodes()
                else:
                    self._check_intentions()
        # Not part of complete bbcc protocol, just recognize
        else:
            self.recognize()

    def clack(self):
        """ Execute clack action of bbcc protocol when self._enable_bbcc is True or Learn a piece of RbfKnowledge
        coming from the senses when self._enable_bbcc is False """
        # Clean outputs
        self.s_knowledge_out = []
        self.h_knowledge_out = []
        if self._enable_bbcc:
            if self._working_domain == "READING":
                self._clack_words()
                # Send bip signal to addition networks (AM and GNB)
            elif self._working_domain == "ADDITION":
                self._clack_addition()
            # Else, transmit it to counting net
            elif self._working_domain == "COUNTING":
                self._clack_counting()
            #################### INTENTIONS ################################################################################
            # Else, episodic memory
            elif self._working_domain == "EPISODES":
                self._clack_episodes()
            else:
                self._check_intentions()
        else:
            self.learn()
        self._enable_bbcc = False

    def _bum_words(self):
        """ Pass bum signal to syllables and words networks """
        self._learning_words = True
        self._learning_syllables = True
        self.words_net.bum()
        self.syllables_net.bum()

    def _bum_addition(self):
        """ Pass bum signal to addition networks """
        # self.am_net.bum()
        self.gnb.set_operation("ADD")
        self.gnb.bum()

    def _bip_words(self):
        """ Execute bip part of bbcc potocol in syllables and words networks """
        # Get id of neuron that recognized sight pattern
        sight_id = self.snb.snb_s.get_rneurons_ids()[0]
        # Get sight and hearing ids relationship from sight-hearing relational neural block
        s_h_rels = self.rnb.get_sight_rels(sight_id)
        # Get sight and syllables ids relationship from  sight-syllables relational neural block
        s_syll_rels = self.ss_rnb.get_sight_rels(sight_id)

        # If at least one relationship was found between sight pattern and a hearing piece of
        # knowledge and the kernel is currently learning syllables, execute bip just in the
        # syllables net
        if len(s_h_rels) != 0 and self._learning_syllables:
            # Syllables
            hearing_id = s_h_rels[0].get_h_id()
            self.syllables_net.bip(hearing_id)
        # If no relation found, the kernel is not learning syllables but words
        else:
            self._learning_syllables = False

        # If at least one relationship was found between sight pattern and a syllable
        # and the kernel is currently learning syllables, execute bip just in the
        # syllables net
        if len(s_syll_rels) != 0 and self._learning_words:
            self._bbcc_words = True
            syll_hearing_id = s_syll_rels[0].get_h_id()
            self.words_net.bip(syll_hearing_id)
        # If no relation found, the kernel is not learning syllables but words
        else:
            self._learning_words = False

        # If the kernel is neither learning words nor learning syllables,
        # disable bbcc protocol
        if not self._learning_syllables and not self._learning_words:
            self._enable_bbcc = False

    def _bip_addition(self):
        """ Pass bip signal to addition networks """
        hearing_id = self._get_hearing_id_recognize()
        # self.am_net.bip(hearing_id)
        self.gnb.bip(hearing_id)
        if len(self.gnb.addition_result) != 0:
            result = self.gnb.addition_result
            self.s_knowledge_out = []
            self.h_knowledge_out = []
            for digit_h_id in result:
                self.h_knowledge_out.append(self.snb.get_hearing_knowledge(digit_h_id, True))
                digit_s_id = self.rnb.get_hearing_rels(digit_h_id)[0].get_s_id()
                self.s_knowledge_out.append(self.snb.get_sight_knowledge(digit_s_id, True))

    def _check_addition(self):
        """ Check if addition by memory network has a result related
        to the operation given through the bbcc protocol """
        hearing_id = self._get_hearing_id_recognize()
        am_id = self.am_net.check(hearing_id)
        # If addition_by_memory doesn't have any knowledge related to the preceding bbc series, proceed with clack
        if am_id is None:
            self.state = "MISS"
            return
        # If it in fact has some knowledge related, show it
        hearing_id = self.am_net.get_tail_knowledge(am_id)
        # Get hearing knowledge related to recognized sight pattern from BNS
        self.h_knowledge_out = self.snb.get_hearing_knowledge(hearing_id, True)
        self._enable_bbcc = False

    def _check_words(self):
        """ Check if either syllables net or words net has a piece of knowledge related to
        the given bbcc input sequence """
        # Get id of neuron that recognized sight pattern
        sight_id = self.snb.snb_s.get_rneurons_ids()[0]
        # Get sight and hearing ids relationship from sight-hearing relational neural block
        s_h_rels = self.rnb.get_sight_rels(sight_id)
        # Get sight and syllables ids relationship from  sight-syllables relational neural block
        s_syll_rels = self.ss_rnb.get_sight_rels(sight_id)

        # Syllables
        if len(s_h_rels) != 0 and self._learning_syllables:
            # Syllables
            hearing_id = s_h_rels[0].get_h_id()
            syll_id = self.syllables_net.check(hearing_id)
            # If syllables net does not have any knowledge related to the preceding bbc series, proceed with clack
            if syll_id is None:
                self._learning_words = False
                self.state = "MISS"
                return
            self.state = "HIT"
            hearing_knowledge = self.syllables_net.get_tail_knowledge(syll_id)
            sight_id = self.ss_rnb.get_hearing_rels(syll_id)[0].get_s_id()
            self.s_knowledge_out = self.snb.get_sight_knowledge(sight_id, True)
            self.h_knowledge_out = hearing_knowledge
            self._enable_bbcc = False
            self._learning_words = False
        #
        self._learning_syllables = False

        # Words
        if len(s_syll_rels) != 0 and self._learning_words:
            syll_hearing_id = s_syll_rels[0].get_h_id()
            word_id = self.words_net.check(syll_hearing_id)
            # If word net doesn't have any knowledge related to the preceding bbc series, proceed with clack
            if word_id is None:
                self.state = "MISS"
                return
            self.s_knowledge_out = self.words_net.get_tail_knowledge(word_id)
            self._enable_bbcc = False
            self._learning_syllables = False
        #
        self._learning_words = False

    def _get_hearing_id_recognize(self):
        # Obtain id of neuron that recognized sight pattern
        sight_id = self.snb.snb_s.get_rneurons_ids()[0]
        # Obtain sight and hearing ids relationship from relational neural block
        sight_rel = self.rnb.get_sight_rels(sight_id)[0]
        # Get hearing id from relation
        return sight_rel.get_h_id()
        # Esto puede ser puesto en un modulo de 'utility functions'

    @staticmethod
    def is_null_pattern(pattern):
        for element in pattern:
            if element != 0:
                return False
        return True

    def _clack_words(self):
        """ Learn knowledge related to given bbcc sequence """
        if self._learning_words:
            sight_pattern = self.s_knowledge_in.get_pattern()
            sight_class = "None"
            sight_knowledge = RbfKnowledge(sight_pattern, sight_class)
            self.words_net.clack(sight_knowledge)
            CulturalNetwork.serialize(self.words_net, "words_net.p")
            self._learning_words = False
        else:
            hearing_pattern = self.h_knowledge_in.get_pattern()
            hearing_class = self.h_knowledge_in.get_class()
            hearing_knowledge = RbfKnowledge(hearing_pattern, hearing_class)
            self.syllables_net.clack(hearing_knowledge)
            CulturalNetwork.serialize(self.syllables_net, "syllables_net.p")
            syll_hearing_id = self.syllables_net.get_last_clack_id()
            sight_pattern = self.s_knowledge_in.get_pattern()
            # Recognize
            if self.snb.recognize_sight(sight_pattern) == "HIT":
                sight_id = self.snb.snb_s.get_rneurons_ids()[0]
            else:
                sight_class = "syll_" + str(syll_hearing_id)
                sight_knowledge = RbfKnowledge(sight_pattern, sight_class)
                self.snb.learn_sight(sight_knowledge)
                sight_id = self.snb.snb_s.get_last_learned_id()
            self.snb.save("sight_snb.p", "hearing_snb.p")
            # Learn relation in new net
            rel_knowledge = RelKnowledge(syll_hearing_id, sight_id)
            self.ss_rnb.learn(rel_knowledge)
            RelNetwork.serialize(self.ss_rnb, "ss_rnb.p")
            self._learning_syllables = False

    def _clack_addition(self):
        s_pattern = self.s_knowledge_in.get_pattern()
        self.state = self.snb.recognize_sight(s_pattern)
        if self.state == "HIT":
            hearing_id = self._get_hearing_id_recognize()
            self.am_net.clack(hearing_id)
            CulturalNetwork.serialize(self.am_net, "am_net.p")

    def recognize(self):
        # Get sight and hearing patterns
        s_pattern = self.s_knowledge_in.get_pattern()
        h_pattern = self.h_knowledge_in.get_pattern()
        # If no patterns or both patterns given, do nothing
        if (KernelBrainCemisid.is_null_pattern(s_pattern) and KernelBrainCemisid.is_null_pattern(h_pattern)
            or not KernelBrainCemisid.is_null_pattern(s_pattern) and not KernelBrainCemisid.is_null_pattern(h_pattern)):
                return
        # If hearing pattern given, recognize hearing
        elif KernelBrainCemisid.is_null_pattern(s_pattern):
            self.hearing_recognize()
        # If sight pattern given, recognize sight
        else:
            self.sight_recognize()

    def hearing_recognize(self):
        pattern = self.h_knowledge_in.get_pattern()
        self.state = self.snb.recognize_hearing(pattern)
        if self.state == "HIT":
            self.h_knowledge_out = self.snb.get_hearing_knowledge(pattern)
            ################# INTENTIONS ###############################################################################
            # Get hearing id of recognizing neuron
            hearing_id = self.snb.snb_h.get_rneurons_ids()[0]
            # Get memory related to hearing id
            memory = self.episodic_memory.retrieve_exact_memory([hearing_id])
            # Get bcf related to memory
            memory_bcf = memory.get_tail_knowledge().get_state()
            # Memory's bcf affects internal state
            self.feed_internal_state(memory_bcf)

    def sight_recognize(self):
        pattern = self.s_knowledge_in.get_pattern()
        self.state = self.snb.recognize_sight(pattern)
        if self.state == "HIT":
            # Obtain id of neuron that recognized sight pattern
            sight_id = self.snb.snb_s.get_rneurons_ids()[0]
            # Obtain sight and hearing ids relationship from relational neural block
            sight_rel = self.rnb.get_sight_rels(sight_id)[0]
            # Get hearing id from relation
            hearing_id = sight_rel.get_h_id()
            # Put hearing knowledge in output port
            self.h_knowledge_out = self.snb.get_hearing_knowledge(hearing_id, True)
            # Put sight knowledge in output port
            self.s_knowledge_out = self.snb.get_sight_knowledge(sight_id, True)
            ################# INTENTIONS ###############################################################################
            # Get memory related to hearing id
            memory = self.episodic_memory.retrieve_exact_memory([hearing_id])
            # Get bcf related to memory
            memory_bcf = memory.get_tail_knowledge().get_state()
            # Memory's bcf affects internal state
            self.feed_internal_state(memory_bcf)

        elif self.state == "DIFF":
            # Get ids os sight neurons that recognized the pattern
            ids_recognize = self.snb.snb_s.get_rneurons_ids()
            # Initialize a vector of relational knowledge
            rel_knowledge_vector = []
            # Fill the vector with the relational knowledge of neurons that recognized the pattern
            for neuron_id in ids_recognize:
                rel_knowledge_vector += self.rnb.get_sight_rels(neuron_id)
            # Get hearing id from analytical neural block
            hearing_id = self.analytical_n.solve_ambiguity(rel_knowledge_vector)
            # Sight knowledge
            sight_knowledge = RbfKnowledge(pattern, str(hearing_id))
            # Learn
            self.snb.learn_sight(sight_knowledge)
            # Get sight id
            sight_id = self.snb.snb_s.get_last_learned_id()
            # Learn relation
            rel_knowledge = RelKnowledge(hearing_id, sight_id)
            self.rnb.learn(rel_knowledge)
            # Try to recognize once again
            self.sight_recognize()

    def learn(self):
        # CORREGIR PARA QUE FUNCIONE CUANDO EL PATRON DEL HEARING NO SE APRENDE SINO QUE YA SE CONOCE
        self.snb.learn(self.h_knowledge_in, self.s_knowledge_in.get_pattern())
        learned_ids = self.snb.get_last_learned_ids()
        rel_knowledge = RelKnowledge(learned_ids[0], learned_ids[1])
        self.rnb.learn(rel_knowledge)
        RelNetwork.serialize(self.rnb, "rnb.p")
        self.snb.save("sight_snb.p", "hearing_snb.p")
        ################ INTENTIONS ####################################################################################
        # New learned item will produce changes in internal state
        self.feed_internal_state(self._internal_state_in)
        # New learned item and passed internal state should be related as an episode
        internal_state_in = InternalState(self._internal_state_in)
        self.episodic_memory.bum()
        self.episodic_memory.check(learned_ids[1])
        self.episodic_memory.clack(internal_state_in)
        EpisodicMemoriesBlock.serialize(self.episodic_memory, "episodic_memory.p")
        ################################################################################################################

    def erase_all_knowledge(self):
        # snb
        self.snb = SensoryNeuralBlock()
        self.snb.save("sight_snb.p", "hearing_snb.p")
        # Relational Neural Block
        self.rnb = RelNetwork(100)
        RelNetwork.serialize(self.rnb, "rnb.p")
        # Addition by memory network
        self.am_net = CulturalNetwork(100)
        CulturalNetwork.serialize(self.am_net, "am_net.p")
        # Syllables net
        self.syllables_net = CulturalNetwork(100)
        CulturalNetwork.serialize(self.syllables_net, "syllables_net.p")
        # Words net
        self.words_net = CulturalNetwork(100)
        CulturalNetwork.serialize(self.words_net, "words_net.p")
        # Sight-Syllables rel network
        self.ss_rnb = RelNetwork(100)
        RelNetwork.serialize(self.ss_rnb, "ss_rnb.p")
        # Geometric Neural Block
        self.gnb = GeometricNeuralBlock()
        GeometricNeuralBlock.serialize(self.gnb, "gnb.p")
        ################ INTENTIONS ####################################################################################
        self.episodic_memory = EpisodicMemoriesBlock()
        EpisodicMemoriesBlock.serialize(self.episodic_memory, "episodic_memory.p")

    # GEOMETRIC NEURAL BLOCK RELATED METHODS
    def set_add_operator(self):
        s_pattern = self.s_knowledge_in.get_pattern()
        self.state = self.snb.recognize_sight(s_pattern)
        if self.state == "HIT":
            hearing_id = self._get_hearing_id_recognize()
            self.gnb.set_add_operator(hearing_id)
            GeometricNeuralBlock.serialize(self.gnb, "gnb.p")
            return True
        return False

    def set_equal_sign(self):
        s_pattern = self.s_knowledge_in.get_pattern()
        self.state = self.snb.recognize_sight(s_pattern)
        if self.state == "HIT":
            hearing_id = self._get_hearing_id_recognize()
            self.gnb.set_equal_sign(hearing_id)
            GeometricNeuralBlock.serialize(self.gnb, "gnb.p")
            return True
        return False

    def set_zero(self):
        s_pattern = self.s_knowledge_in.get_pattern()
        self.state = self.snb.recognize_sight(s_pattern)
        if self.state == "HIT":
            hearing_id = self._get_hearing_id_recognize()
            self.gnb.set_zero(hearing_id)
            GeometricNeuralBlock.serialize(self.gnb, "gnb.p")
            return True
        return False

    def _bum_counting(self):
        self.gnb.set_operation("COUNT")
        self.gnb.bum()
        return

    def _bip_counting(self):
        self.gnb.bip()
        return

    def _clack_counting(self):
        hearing_id = self._get_hearing_id_recognize()
        self.gnb.clack(hearing_id)
        GeometricNeuralBlock.serialize(self.gnb, "gnb.p")
        return

    ########################## INTENTIONS ##############################################################################
    def _bum_episodes(self):
        """ Pass bum signal to episodic memory """
        self.episodic_memory.bum()

    def _bip_episodes(self):
        """ Pass bip signal to episodic memory """
        hearing_id = self._get_hearing_id_recognize()
        self.episodic_memory.bip(hearing_id)

    def _check_episodes(self):
        """ Check if epsodic memory network has a result related
                to the operation given through the bbcc protocol """
        hearing_id = self._get_hearing_id_recognize()
        em_id = self.episodic_memory.check(hearing_id)
        # If addition_by_memory doesn't have any knowledge related to the preceding bbc series, proceed with clack
        if em_id is None:
            self.state = "MISS"
            return
            # Get bcf related to episode
        episode_bcf = self.episodic_memory.get_tail_knowledge(em_id).get_state()
        # Memory's bcf affects internal state
        self.feed_internal_state(episode_bcf)
        # Disable bbcc
        self._enable_bbcc = False

    def _clack_episodes(self):
        episode_bcf = BiologyCultureFeelings(self.internal_state.get_state())
        self.episodic_memory.clack(episode_bcf)
        EpisodicMemoriesBlock.serialize(self.episodic_memory, "episodic_memory.p")

    def _bum_intentions(self):
        self._intentions_short_term_memory = []
        return

    def _bip_intentions(self):
        hearing_id = self._get_hearing_id_recognize()
        self._intentions_short_term_memory.append(hearing_id)
        return

    def _check_intentions(self):
        # Get memories
        memories = self.episodic_memory.retrieve_memories(self._intentions_short_term_memory)
        self.decisions_block.set_desired_state(self.desired_state)
        self.decisions_block.set_internal_state(self.internal_state)
        self.decisions_block.set_input_memories(memories)
        self._output_memory = self.decisions_block.get_output_memory()
        # Obtain sight and hearing ids relationship from relational neural block
        hearing_id = self._output_memory.group[0].get_knowledge()
        hearing_rel = self.rnb.get_hearing_rels(hearing_id)[0]
        # Get hearing id from relation
        sight_id = hearing_rel.get_s_id()
        # Put hearing knowledge in output port
        self.h_knowledge_out = self.snb.get_hearing_knowledge(hearing_id, True)
        # Put sight knowledge in output port
        self.s_knowledge_out = self.snb.get_sight_knowledge(sight_id, True)
        return

    def _clack_intentions(self):
        return