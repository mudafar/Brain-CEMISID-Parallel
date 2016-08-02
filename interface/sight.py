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

class MyPaintElement(Widget):

    def __init__ (self, **kwargs):
        super(MyPaintElement, self).__init__ ( **kwargs)
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


    def __init__ (self, size, **kwargs):
        super(MyPaintWidget, self).__init__ ( **kwargs)
        self.cols = size
        for index in range(self.cols*self.cols):
            self.add_widget(MyPaintElement())

    def on_touch_down(self, touch):
        if self.collide_point(touch.x, touch.y):
            # Clear painter
            self.clear()
                  
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
            if count == pow(2,4):
                pattern.append(val)
                val = 0
                count = 1
        return pattern

class SightUI(GridLayout):

    def __init__ (self, grid_size, radius, **kwargs):
        super(SightUI, self).__init__ ( **kwargs)
        # Calculate pattern size based on grid_size and size of a byte (8)
        pattern_size = pow(grid_size,2)/4
        # Set neural network data size
        RbfNetwork.PATTERN_SIZE = pattern_size
        # Set neural network default radius
        RbfNetwork.DEFAULT_RADIUS = radius
        # Set pattern size in RBF knowledge
        RbfKnowledge.PATTERN_SIZE = pattern_size
        # Create neural network with 100 neurons
        self.neuron_count = 100;
        self.net = RbfNetwork(self.neuron_count)
        # Create instance of painter widget
        self.painter = MyPaintWidget(grid_size)
        # Main layout number of rows
        self.rows = 2
        # Add painter widget to first row of layout
        self.add_widget(self.painter)
        # Label for brain messages
        self.msg_label = Label(text="" )
        # Recognize button
        self.recognize_btn = Button(text='Reconocer')
        self.recognize_btn.bind(on_release=self.recognize_pattern)
        # Learn button
        self.learn_btn = Button(text='Aprender')
        self.learn_btn.bind(on_release=self.learn_pattern)
        # Class name input field
        self.class_name_input = TextInput(text="Clase")
        # Set name input field
        self.set_name_input = TextInput(text="Conjunto")
        # Bottom inputs layout
        self.bottom_layout = GridLayout(rows = 5)
        self.bottom_layout.add_widget(self.msg_label)
        self.bottom_layout.add_widget( self.class_name_input )
        self.bottom_layout.add_widget( self.set_name_input )
        self.bottom_layout.add_widget(self.recognize_btn)
        self.bottom_layout.add_widget(self.learn_btn)
        # Add bottom layout to main layout
        self.add_widget(self.bottom_layout)

    def recognize_pattern(self, obj):
        pattern = self.painter.get_pattern()
        if self.net.recognize(pattern) == "HIT":
            knowledge = self.net.get_knowledge()
            self.msg_label.text = "Reconozco un " + knowledge.get_class() + " que es un tipo de " + knowledge.get_set()
        else:
            self.msg_label.text = "No reconozco"

    def learn_pattern(self, obj):
        pattern = self.painter.get_pattern()
        pattern_class = self.class_name_input.text
        pattern_set = self.set_name_input.text
        knowledge = RbfKnowledge(pattern, pattern_class, pattern_set)
        self.net.learn(knowledge)

class MyPaintApp(App):

    def build(self):
        grid_size = 16
        # HEURISTICS: radius = (1/3)*2^(ENCODING_SIZE)
        # where ENCODING_SIZE is bit size of every pattern element (8 bits for us)
        radius = 16
        sight1 = SightUI(grid_size,radius)
        return sight1;


if __name__ == '__main__':
    MyPaintApp().run()

if __name__ == '__main__':
    MyPaintApp().run()