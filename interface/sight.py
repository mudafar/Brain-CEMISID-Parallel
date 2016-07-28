from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

# Brain-CEMISID kernel imports
from ..kernel.rbf_network.py import RbfNetwork
from ..kernel.rbf_knowledge.py import RbfKnowledge

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

    ROW_LENGTH = 32

    def __init__ (self, **kwargs):
        super(MyPaintWidget, self).__init__ ( **kwargs)
        self.cols = MyPaintWidget.ROW_LENGTH
        for index in range(self.cols*self.cols):
            self.add_widget(MyPaintElement())
    
    def on_touch_down(self, touch):
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
            if count == pow(2,MyPaintWidget.ROW_LENGTH):
                pattern.append(val)
                val = 0
                count = 1
        return pattern

class SightUI(GridLayout):
    def __init__ (self, **kwargs):
        super(SightUI, self).__init__ ( **kwargs)
        # Create instance of painter widget
        self.painter = MyPaintWidget()
        # Main layout number of rows
        self.rows = 2
        # Add painter widget to first row of layout
        self.add_widget(self.painter)
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
        self.bottom_layout = GridLayout(rows = 4)
        self.bottom_layout.add_widget( self.class_name_input )
        self.bottom_layout.add_widget( self.set_name_input )
        self.bottom_layout.add_widget(self.recognize_btn)
        self.bottom_layout.add_widget(self.learn_btn)
        # Add bottom layout to main layout
        self.add_widget(self.bottom_layout)

    def recognize_pattern(self, obj):
        pattern = self.painter.get_pattern()
        self.class_name_input.text = '[' + ', '.join(str(x) for x in pattern) + ']'

    def learn_pattern(self, obj):
        pattern = self.painter.get_pattern()
        pattern_class = self.class_name_input.text
        pattern_set = self.set_name_input.text
        print pattern
        net = RbfNetwork()

class MyPaintApp(App):

    def build(self):
        sight1 = SightUI()
        return sight1;


if __name__ == '__main__':
    MyPaintApp().run()

if __name__ == '__main__':
    MyPaintApp().run()