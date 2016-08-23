from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

# Brain-CEMISID kernel imports
from rbf_network import RbfNetwork
from rbf_knowledge import RbfKnowledge
from rel_network import RelNetwork
from rel_knowledge import RelKnowledge
from analytical_neuron import AnalyticalNeuron

from bns import Bns

class MyPaintElement(Widget):
    def __init__(self, **kwargs):
        super(MyPaintElement, self).__init__(**kwargs)
        self.active = False

    def on_touch_down(self, touch):
        # Check if touch event is inside widget
        if self.collide_point(touch.x, touch.y):
            # If so, draw rectangle
            with self.canvas:
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

    def clear(self):
        with self.canvas:
            # lets draw a semi-transparent red square
            Color(0, 0, 0, 1, mode='rgba')
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
        for child in self.children:
            child.clear()

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
                    child_set[j].clear()

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
        self.rows = 3;

        self.declare_painters(grid_size)
        self.declare_inputs()
        self.declare_buttons()
        self.add_widgets_layouts()

        # bns
        self.bns = Bns()
        # Relational Neural Block
        self.rnb = RelNetwork(100)
        # Analytical neuron
        self.analytical_n = AnalyticalNeuron()

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
        # Sight recognize
        self.sight_recognize_btn = Button(text="Reconocer Vista")
        self.sight_recognize_btn.bind(on_release=self.sight_recognize)

        # hearing recognize
        self.hearing_recognize_btn = Button(text="Reconocer Oido")
        self.hearing_recognize_btn.bind(on_release=self.hearing_recognize)

        # sight clear
        self.sight_clear_btn = Button(text="Limpiar Vista")
        self.sight_clear_btn.bind(on_release=self.sight_clear)

        # Hearing clear
        self.hearing_clear_btn = Button(text="Limpiar Oido")
        self.hearing_clear_btn.bind(on_release=self.hearing_clear)

        # Learn btn
        self.learn_btn = Button(text="Aprender", size_hint_y=None, height=70)
        self.learn_btn.bind(on_release=self.learn)

    def add_widgets_layouts(self):
        # Add widgets to bottom layout
        self.bottom_layout = GridLayout(cols=2)
        self.bottom_layout.add_widget(self.sight_class_input)
        self.bottom_layout.add_widget(self.hearing_class_input)
        self.bottom_layout.add_widget(self.sight_recognize_btn)
        self.bottom_layout.add_widget(self.hearing_recognize_btn)
        self.bottom_layout.add_widget(self.sight_clear_btn)
        self.bottom_layout.add_widget(self.hearing_clear_btn)

        self.add_widget(self.painters_layout)
        self.add_widget(self.bottom_layout)
        self.add_widget(self.learn_btn)

    def hearing_recognize(self, obj):
        pattern = self.hearing_painter.get_pattern()
        if self.bns.recognize_hearing(pattern) == "HIT":
            knowledge = self.bns.get_hearing_knowledge(pattern)
            self.hearing_class_input.text = knowledge.get_class()
        else:
            self.hearing_class_input.text = "No reconozco "

    def sight_recognize(self, obj):
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
            rel_knowledge = RelKnowledge(hearing_id, sight_id);
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

    def _learn(self, hearing_pattern, sight_pattern, hearing_class ):
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

    def paint_sight(self):
        hearing_pattern = self.hearing_painter.get_pattern()
        self.sight_painter.draw_pattern(hearing_pattern)

class MyPaintApp(App):
    def build(self):
        brainUI = BrainInterface();

        return brainUI;


if __name__ == '__main__':
    MyPaintApp().run()
