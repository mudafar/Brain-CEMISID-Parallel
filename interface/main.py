from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.togglebutton import ToggleButton

# Brain-CEMISID kernel imports
from rbf_network import RbfNetwork
from rbf_knowledge import RbfKnowledge
from rel_network import RelNetwork
from rel_knowledge import RelKnowledge
from analytical_neuron import AnalyticalNeuron
from cultural_network import CulturalNetwork

from bns import Bns

class MyPaintElement(Widget):
    def __init__(self, **kwargs):
        super(MyPaintElement, self).__init__(**kwargs)
        self.active = False

    def on_touch_down(self, touch):
        # Check if touch event is inside widget
        if self.collide_point(touch.x, touch.y):
            self._draw_rectange()

    def on_touch_move(self, touch):
        # Check if touch event is inside widget
        if self.collide_point(touch.x, touch.y):
            # If so, draw rectangle
            self._draw_rectange()

    def _draw_rectange(self):
        with self.canvas:
            # lets draw a semi-transparent red square
            Color(1, 1, 1, 1, mode='rgba')
            Rectangle(pos=self.pos, size=self.size)
        self.active = True

    def clear(self, color):
        with self.canvas:
            if color == "black":
                # lets draw a semi-transparent red square
                Color(0, 0, 0, 1, mode='rgba')
            else:
                Color(0, 0.2, 0.2, 1, mode='rgba')
            Rectangle(pos=self.pos, size=self.size)
        self.active = False

    def mark(self):
        self._draw_rectange()

class MyPaintWidget(GridLayout):

    CODING_SIZE = 4

    def __init__(self, size, **kwargs):
        super(MyPaintWidget, self).__init__(**kwargs)
        self.cols = size
        for index in range(self.cols * self.cols):
            self.add_widget(MyPaintElement())

    def clear(self):
        index = 0
        for child in self.children:
            if index % 2:
                child.clear("dark-turquoise")
            else:
                child.clear("black")
            index += 1

    def get_pattern(self):
        # Initial pattern is an empty list of integers
        pattern = []
        # Integer representation or first row of pattern (bottom)
        val = 0
        # Counter to obtain integer value from binary row
        count = 1
        # For each MyPaintElement instance, verify if active and
        # add integer value to val depending on its position (count)
        for child in self.children:
            if child.active:
                val += count
            count *= 2
            # If row over, append to pattern array and
            # start encoding new one
            if count == pow(2, MyPaintWidget.CODING_SIZE):
                pattern.append(val)
                val = 0
                count = 1
        return pattern

    def draw_pattern(self, pattern):
        """ Draw given pattern in painter"""
        for index in range(len(pattern)):
            # Get children in groups of four (As codification was made by groups of four)
            child_offset = index*MyPaintWidget.CODING_SIZE
            child_set = self.children[child_offset:child_offset+MyPaintWidget.CODING_SIZE]
            # Convert current number of pattern into binary
            format_str = "{0:0"+str(MyPaintWidget.CODING_SIZE)+"b}"
            bin_pattern_element = format_str.format(pattern[index])
            # Traverse binary, mark or clear corresponding child
            for j in range(len(bin_pattern_element)):
                if(bin_pattern_element[MyPaintWidget.CODING_SIZE-1-j]=="1"):
                    child_set[j].mark()
                else:
                    if j%2:
                        child_set[j].clear("dark-turquoise")
                    else:
                        child_set[j].clear("black")

class BrainInterface(GridLayout):
    def __init__(self, **kwargs):
        super(BrainInterface, self).__init__(**kwargs)
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

        # Main layout number of rows
        self.cols = 1

        self.declare_painters(grid_size)
        self.declare_inputs()
        self.declare_buttons()
        self.add_widgets_layouts()

        # bns
        self.bns = Bns("sight_bns.p", "hearing_bns.p" )
        #self.bns = Bns()
        # Relational Neural Block
        self.rnb = RelNetwork.deserialize("rnb.p")
        #self.rnb = RelNetwork(100)
        # Analytical neuron
        self.analytical_n = AnalyticalNeuron()
        # Addition by memory network
        #self.am_net = CulturalNetwork(100)
        self.am_net = CulturalNetwork.deserialize("am_net.p")
        self.enable_clack = False
        # Syllables net
        #self.syllables_net = CulturalNetwork(100)
        self.syllables_net = CulturalNetwork.deserialize("syllables_net.p")
        # Words net
        #self.words_net =  CulturalNetwork(100)
        self.words_net = CulturalNetwork.deserialize("words_net.p")
        # Sight-Syllables rel network
        self.ss_rnb = RelNetwork.deserialize("ss_rnb.p")
        #self.ss_rnb = RelNetwork(100)
        # _bbcc_words
        self._learning_words = False
        self._learning_syllables = False

    def declare_painters(self, grid_size):
        self.painters_layout = GridLayout(cols=2)
        self.sight_painter = MyPaintWidget(grid_size)
        self.hearing_painter = MyPaintWidget(grid_size)
        self.painters_layout.add_widget(self.sight_painter)
        self.painters_layout.add_widget(self.hearing_painter)

    def declare_inputs(self):
        self.sight_class_input = TextInput(text="")
        self.hearing_class_input = TextInput(text="Clase")

    def declare_buttons(self):
        # sight clear
        self.sight_clear_btn = Button(text="Clear Sight")
        self.sight_clear_btn.bind(on_release=self.sight_clear)

        # Hearing clear
        self.hearing_clear_btn = Button(text="Clear Hearing")
        self.hearing_clear_btn.bind(on_release=self.hearing_clear)

        # Bum btn
        self.bum_btn = Button(text="Bum")
        self.bum_btn.bind(on_release=self.bum)

        # Bip btn
        self.bip_btn = Button(text="Bip")
        self.bip_btn.bind(on_release=self.bip)

        # Check btn
        self.check_btn = Button(text="Check")
        self.check_btn.bind(on_release=self.check)

        # Clack btn
        self.clack_btn = Button(text="Clack")
        self.clack_btn.bind(on_release=self.clack)

        # Toggle button (Words, Numbers)
        self.words_tgl_btn = ToggleButton(text="words", group="bbcc_protocol", allow_no_selection=False)
        self.addition_tgl_btn = ToggleButton(text="addition", group="bbcc_protocol", state="down", allow_no_selection=False)

    def add_widgets_layouts(self):
        # Add widgets to bottom layout
        self.bottom_layout = GridLayout(rows=2)
        self.bottom_up_layout = GridLayout(cols=2)
        self.bottom_up_layout.add_widget(self.sight_class_input)
        self.bottom_up_layout.add_widget(self.hearing_class_input)
        self.bottom_up_layout.add_widget(self.sight_clear_btn)
        self.bottom_up_layout.add_widget(self.hearing_clear_btn)

        # Add bbcc buttons protocols to bbcc-layout
        self.bbcc_layout = GridLayout(cols=4)
        self.bbcc_layout.add_widget(self.bum_btn)
        self.bbcc_layout.add_widget(self.bip_btn)
        self.bbcc_layout.add_widget(self.check_btn)
        self.bbcc_layout.add_widget(self.clack_btn)
        self.bbcc_layout.add_widget(self.words_tgl_btn)
        self.bbcc_layout.add_widget(self.addition_tgl_btn)

        self.bottom_layout.add_widget(self.bottom_up_layout)
        self.bottom_layout.add_widget(self.bbcc_layout)

        self.add_widget(self.painters_layout)
        self.add_widget(self.bottom_layout)

    def hearing_recognize(self):
        pattern = self.hearing_painter.get_pattern()
        recognition_result = self.bns.recognize_hearing(pattern)
        if recognition_result == "HIT":
            knowledge = self.bns.get_hearing_knowledge(pattern)
            self.hearing_class_input.text = knowledge.get_class()
        else:
            self.hearing_class_input.text = recognition_result

    def sight_recognize(self):
        pattern = self.sight_painter.get_pattern()
        srecognize = self.bns.recognize_sight(pattern)
        if srecognize == "HIT":
            # Obtain id of neuron that recognized sight pattern
            sight_id = self.bns.bns_s.get_rneurons_ids()[0]
            # Obtain sight and hearing ids relationship from relational neural block
            sight_rel = self.rnb.get_sight_rels(sight_id)[0]
            # Get hearing id from relation
            hearing_id = sight_rel.get_h_id()
            # Get hearing knowledge related to recognized sight pattern from BNS
            hearing_knowledge = self.bns.get_hearing_knowledge(hearing_id, True)
            # Get sight knowledge related to recognized sight pattern from BNS
            sight_knowledge = self.bns.get_sight_knowledge(sight_id, True)
            # Draw hearing pattern
            self.hearing_painter.draw_pattern(hearing_knowledge.get_pattern())
            # Write sight knowledge's class
            self.sight_class_input.text = sight_knowledge.get_class()
            #write hearing knowledge's class
            self.hearing_class_input.text = hearing_knowledge.get_class()
        elif srecognize == "DIFF":
            # Get ids os sight neurons that recognized the pattern
            ids_recognize = self.bns.bns_s.get_rneurons_ids()
            # Initialize a vector of relational knowledge
            rel_knowledge_vector = []
            # Fill the vector with the relational knowledge of neurons that recognized the pattern
            for neuron_id in ids_recognize:
                rel_knowledge_vector += self.rnb.get_sight_rels(neuron_id)
            # Get hearing id from analytical neural block
            hearing_id = self.analytical_n.solve_ambiguity(rel_knowledge_vector)
            # Sight knowledge
            sight_knowledge = RbfKnowledge(pattern,str(hearing_id))
            # Learn
            self.bns.learn_sight(sight_knowledge)
            # Get sight id
            sight_id = self.bns.bns_s.get_last_learned_id()
            # Learn relation
            rel_knowledge = RelKnowledge(hearing_id, sight_id)
            self.rnb.learn(rel_knowledge)
        else:
            self.sight_class_input.text =  "No reconozco"

    def learn(self, obj):
        # CORREGIR PARA QUE FUNCIONE CUANDO EL PATRON DEL HEARING NO SE APRENDE SINO QUE YA SE CONOCE
        hearing_pattern = self.hearing_painter.get_pattern()
        sight_pattern = self.sight_painter.get_pattern()
        pattern_class = self.hearing_class_input.text
        self._learn(hearing_pattern, sight_pattern, pattern_class)
        (self.bns).save("sight_bns.p","hearing_bns.p")
        RelNetwork.serialize(self.rnb, "rnb.p")

    def _learn(self, hearing_pattern, sight_pattern, hearing_class):
        h_knowledge = RbfKnowledge(hearing_pattern, hearing_class)
        self.bns.learn(h_knowledge, sight_pattern)
        learned_ids = self.bns.get_last_learned_ids()
        rel_knowledge = RelKnowledge(learned_ids[0], learned_ids[1]);
        self.rnb.learn(rel_knowledge)

    def hearing_clear(self, obj):
        self.hearing_painter.clear()
        self.hearing_class_input.text = ""

    def sight_clear(self, obj):
        self.sight_painter.clear()
        self.sight_class_input.text = ""

    def bum(self,obj ):
        # Enable check and clack as a part of bbcc protocol
        # preventing their effect as standalone actions
        self.enable_clack = True
        if self.words_tgl_btn.state == "down":
            self.bum_words()
        else:
            self.bum_addition()

    def bip(self, obj):
        if not self.enable_clack:
            return
        # Get sight pattern's related hearing neuron id
        s_pattern = self.sight_painter.get_pattern()
        s_recognize = self.bns.recognize_sight(s_pattern)
        if s_recognize == "HIT":
            if self.words_tgl_btn.state == "down":
                self.bip_words()
            else:
                self.bip_addition()
        else:
            self.sight_class_input.text = s_recognize

    def bum_words(self):
        self._learning_words = True
        self._learning_syllables = True
        self.words_net.bum()
        self.syllables_net.bum()

    def bum_addition(self):
        self.am_net.bum()

    def bip_words(self):
        # Get id of neuron that recognized sight pattern
        sight_id = self.bns.bns_s.get_rneurons_ids()[0]
        # Get sight and hearing ids relationship from sight-hearing relational neural block
        s_h_rels = self.rnb.get_sight_rels(sight_id)
        # Get sight and syllables ids relationship from  sight-syllables relational neural block
        s_syll_rels = self.ss_rnb.get_sight_rels(sight_id)

        if len(s_h_rels) != 0 and self._learning_syllables:
            # Syllables
            hearing_id = s_h_rels[0].get_h_id()
            self.syllables_net.bip(hearing_id)
        else:
            self._learning_syllables = False

        if len(s_syll_rels) != 0 and self._learning_words:
            self._bbcc_words = True
            syll_hearing_id = s_syll_rels[0].get_h_id()
            self.words_net.bip(syll_hearing_id)
        else:
            self._learning_words = False

    def bip_addition(self):
        hearing_id = self.get_hearing_id_recognize()
        self.am_net.bip(hearing_id)


    def get_hearing_id_recognize(self):
        # Obtain id of neuron that recognized sight pattern
        sight_id = self.bns.bns_s.get_rneurons_ids()[0]
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

    def check(self, obj):
        # Part of complete bbcc protocol
        if self.enable_clack:
            s_pattern = self.sight_painter.get_pattern()
            s_recognize = self.bns.recognize_sight(s_pattern)
            if s_recognize == "HIT":
                if self.words_tgl_btn.state == "down":
                    self.check_words()
                else:
                    self.check_addition()
            else:
                self.sight_class_input.text = s_recognize
        # Not part of complete bbcc protocol, just recognize
        else:
            self.recognize()

    def check_addition(self):
        hearing_id = self.get_hearing_id_recognize()
        am_id = self.am_net.check(hearing_id)
        # If addition_by_memory doesn't have any knowledge related to the preceding bbc series, proceed with clack
        if am_id is None:
            return
        # If it in fact has some knowledge related, show it
        hearing_id = self.am_net.get_tail_knowledge(am_id)
        # Get hearing knowledge related to recognized sight pattern from BNS
        hearing_knowledge = self.bns.get_hearing_knowledge(hearing_id, True)
        # Draw hearing pattern
        self.hearing_painter.draw_pattern(hearing_knowledge.get_pattern())
        # write hearing knowledge's class
        self.hearing_class_input.text = hearing_knowledge.get_class()
        self.enable_clack = False

    def check_words(self):
        # Get id of neuron that recognized sight pattern
        sight_id = self.bns.bns_s.get_rneurons_ids()[0]
        # Get sight and hearing ids relationship from sight-hearing relational neural block
        s_h_rels = self.rnb.get_sight_rels(sight_id)
        # Get sight and syllables ids relationship from  sight-syllables relational neural block
        s_syll_rels = self.ss_rnb.get_sight_rels(sight_id)

        # Syllables
        if len(s_h_rels) != 0 and self._learning_syllables:
            # Syllables
            hearing_id = s_h_rels[0].get_h_id()
            syll_id = self.syllables_net.check(hearing_id)
            # If syllables net doesn't have any knowledge related to the preceding bbc series, proceed with clack
            if syll_id is None:
                self._learning_words = False
                return
            hearing_knowledge = self.syllables_net.get_tail_knowledge(syll_id)
            sight_id = self.ss_rnb.get_hearing_rels(syll_id)[0].get_s_id()
            sight_knowledge = self.bns.get_sight_knowledge(sight_id, True)
            # Draw hearing pattern
            self.hearing_painter.draw_pattern(hearing_knowledge.get_pattern())
            # write hearing knowledge's class
            self.hearing_class_input.text = hearing_knowledge.get_class()
            # Draw sight pattern
            self.sight_painter.draw_pattern(sight_knowledge.get_pattern())
            # Write sight knowledge class
            self.sight_class_input.text = sight_knowledge.get_class()
            self.enable_clack = False
            self._learning_syllables = False
        else:
            self._learning_syllables = False

        # Words
        if len(s_syll_rels) != 0 and self._learning_words:
            syll_hearing_id = s_syll_rels[0].get_h_id()
            word_id = self.words_net.check(syll_hearing_id)
            # If word net doesn't have any knowledge related to the preceding bbc series, proceed with clack
            if word_id is None:
                return
            sight_knowledge = self.words_net.get_tail_knowledge(word_id)
            self.sight_painter.draw_pattern(sight_knowledge.get_pattern())
            self.sight_class_input.text = sight_knowledge.get_class()
            self.enable_clack = False
            self._learning_words = False
        else:
            self._learning_words = False


    def clack(self, obj):
        if self.enable_clack:
                if self.words_tgl_btn.state == "down":
                    self.clack_words()
                else:
                    self.clack_addition()
        else:
            self.learn(None)
        self.enable_clack = False

    def clack_words(self):
        if self._learning_words:
            sight_pattern = self.sight_painter.get_pattern()
            sight_class = "None"
            sight_knowledge = RbfKnowledge(sight_pattern, sight_class )
            self.words_net.clack(sight_knowledge)
            CulturalNetwork.serialize(self.words_net, "words_net.p")
            self._learning_words = False
        else:
            hearing_pattern = self.hearing_painter.get_pattern()
            hearing_class = self.hearing_class_input.text
            hearing_knowledge = RbfKnowledge(hearing_pattern, hearing_class)
            self.syllables_net.clack(hearing_knowledge)
            CulturalNetwork.serialize(self.syllables_net, "syllables_net.p")
            syll_hearing_id = self.syllables_net.get_last_clack_id()
            sight_pattern = self.sight_painter.get_pattern()
            # Recognize
            if self.bns.recognize_sight(sight_pattern) == "HIT":
                sight_id = self.bns.bns_s.get_rneurons_ids()[0]
            else:
                sight_class = "syll_" + str(syll_hearing_id)
                sight_knowledge = RbfKnowledge(sight_pattern, sight_class)
                self.bns.learn_sight(sight_knowledge)
                sight_id = self.bns.bns_s.get_last_learned_id()
            (self.bns).save("sight_bns.p", "hearing_bns.p")
            # Learn relation in new net
            rel_knowledge = RelKnowledge(syll_hearing_id, sight_id)
            self.ss_rnb.learn(rel_knowledge)
            RelNetwork.serialize(self.ss_rnb, "ss_rnb.p")
            self._learning_syllables = False

    def clack_addition(self):
        s_pattern = self.sight_painter.get_pattern()
        s_recognize = self.bns.recognize_sight(s_pattern)
        if s_recognize == "HIT":
            hearing_id = self.get_hearing_id_recognize()
            self.am_net.clack(hearing_id)
            CulturalNetwork.serialize(self.am_net, "am_net.p")
        else:
            self.sight_class_input.text = s_recognize

    def recognize(self):
        # Get sight and hearing patterns
        s_pattern = self.sight_painter.get_pattern()
        h_pattern = self.hearing_painter.get_pattern()
        # If no patterns or both patterns given, do nothing
        if (BrainInterface.is_null_pattern(s_pattern) and BrainInterface.is_null_pattern(h_pattern)
            or not BrainInterface.is_null_pattern(s_pattern) and not BrainInterface.is_null_pattern(h_pattern)):
            return
        # If hearing pattern given, recognize hearing
        elif BrainInterface.is_null_pattern(s_pattern):
            self.hearing_recognize()
        # If sight pattern given, recognize sight
        else:
            self.sight_recognize()


class MyPaintApp(App):
    def build(self):
        brainUI = BrainInterface()
        return brainUI


if __name__ == '__main__':
    MyPaintApp().run()
