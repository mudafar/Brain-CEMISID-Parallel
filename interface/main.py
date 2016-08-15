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


class MyPaintWidget(GridLayout):
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
            if count == pow(2, 4):
                pattern.append(val)
                val = 0
                count = 1
        return pattern


class BasicUI(GridLayout):
    def __init__(self, grid_size, radius, name_net_file="NoFile", **kwargs):
        super(BasicUI, self).__init__(**kwargs)

        # Create instance of painter widget
        self.painter = MyPaintWidget(grid_size)
        # Main layout number of rows
        self.rows = 2

        # Label for brain messages
        self.msg_label = Label(text="")
        self.pattern_label = TextInput(text="")
        # Recognize button
        self.recognize_btn = Button(text='Reconocer')
        self.recognize_btn.bind(on_release=self.recognize_pattern)
        # Clear canvas button
        self.clear_btn = Button(text='Limpiar')
        self.clear_btn.bind(on_release=self.clear_painter)
        # Class name input field
        self.class_name_input = TextInput(text="Clase")
        # Set name input field
        self.set_name_input = TextInput(text="Conjunto")
        # Bottom inputs layout
        self.bottom_layout = GridLayout(rows=5)
        self.buttons_layout = GridLayout(cols=3)
        self.bottom_layout.add_widget(self.msg_label)
        self.bottom_layout.add_widget(self.pattern_label)
        self.bottom_layout.add_widget(self.class_name_input)
        self.bottom_layout.add_widget(self.set_name_input)
        self.buttons_layout.add_widget(self.recognize_btn)
        self.buttons_layout.add_widget(self.learn_btn)
        self.buttons_layout.add_widget(self.clear_btn)
        self.bottom_layout.add_widget(self.buttons_layout)
        # Add painter widget to last row of layout
        self.add_widget(self.painter)
        # Add bottom layout to main layout
        self.add_widget(self.bottom_layout)

    def recognize_pattern(self, obj):
            pattern = self.painter.get_pattern()
            self.pattern_label.text = str(pattern)
            if self.net.recognize(pattern) == "HIT":
                knowledge = self.net.get_knowledge()
                self.msg_label.text = "Clase: " + knowledge.get_class() + " Conjunto: " + knowledge.get_set() + " " + str(
                    self.net.get_rneurons_ids())
            else:
                self.msg_label.text = "No reconozco " + self.net.get_state()

    def learn_pattern(self, obj):
        pattern = self.painter.get_pattern()
        pattern_class = self.class_name_input.text
        pattern_set = self.set_name_input.text
        knowledge = RbfKnowledge(pattern, pattern_class, pattern_set)
        self.net.learn(knowledge)
        RbfNetwork.serialize(self.net, "net.p")

    def clear_painter(self, obj):
        self.painter.clear()


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

        # Kernel
        self.bns = Bns()

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
        if self.bns.recognize_sight(pattern) == "HIT":
            knowledge = self.bns.get_sight_knowledge(pattern)
            self.sight_class_input.text = knowledge.get_class()
        else:
            self.sight_class_input.text = "No reconozco"

    def learn(self, obj):
        hearing_pattern = self.hearing_painter.get_pattern()
        sight_pattern = self.sight_painter.get_pattern()
        pattern_class = self.hearing_class_input.text
        h_knowledge = RbfKnowledge(hearing_pattern, pattern_class)
        self.bns.learn_sight(h_knowledge, sight_pattern )
        (self.bns).save("sight_bns.p","hearing_bns.p")

    def hearing_clear(self, obj):
        self.hearing_painter.clear()

    def sight_clear(self, obj):
        self.sight_painter.clear()


class MyPaintApp(App):
    def build(self):
        brainUI = BrainInterface();

        return brainUI;


if __name__ == '__main__':
    MyPaintApp().run()
