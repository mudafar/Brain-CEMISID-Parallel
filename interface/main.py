from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.togglebutton import ToggleButton

# Brain-CEMISID kernel imports
from kernel_braincemisid import KernelBrainCemisid
from rbf_knowledge import RbfKnowledge

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

class MyGroupPaintWidget(GridLayout):

    def __init__(self, **kwargs):
        super(MyGroupPaintWidget, self).__init__(**kwargs)
        self.rows = 1

    def show_rbf_knowledge(self, knowledge_vector):
        for knowledge in knowledge_vector:
            painter = MyPaintWidget(16)
            painter.draw_pattern(knowledge.get_pattern())
            self.add_widget(painter)

class BrainInterface(GridLayout):
    def __init__(self, **kwargs):
        super(BrainInterface, self).__init__(**kwargs)

        grid_size = 16

        self.kernel = KernelBrainCemisid()

        # Main layout number of columns
        self.cols = 1
        self.declare_painters(grid_size)
        self.declare_thinking_panel()
        self.declare_inputs()
        self.declare_buttons()
        self.add_widgets_layouts()


    def declare_painters(self, grid_size):
        self.painters_layout = GridLayout(cols=2)
        self.sight_painter = MyPaintWidget(grid_size)
        self.hearing_painter = MyPaintWidget(grid_size)
        self.painters_layout.add_widget(self.sight_painter)
        self.painters_layout.add_widget(self.hearing_painter)

    def declare_thinking_panel(self):
        self.thinking_panel = GridLayout(rows=2)
        self.thinking_s_panel = MyGroupPaintWidget()
        self.thinking_h_panel = MyGroupPaintWidget()
        self.thinking_panel.add_widget(self.thinking_s_panel)
        self.thinking_panel.add_widget(self.thinking_h_panel)

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

        self.senses_panel = GridLayout(cols=1)
        self.senses_panel.add_widget(self.painters_layout)
        self.senses_panel.add_widget(self.bottom_layout)
        self.add_widget(self.senses_panel)

    def learn(self,obj):
        return

    def hearing_clear(self, obj):
        self.hearing_painter.clear()
        self.hearing_class_input.text = ""

    def sight_clear(self, obj):
        self.sight_painter.clear()
        self.sight_class_input.text = ""

    def bum(self,obj):
        self.pass_kernel_inputs()
        self.kernel.bum()
        self.sight_class_input.text = self.kernel.state
        return

    def bip(self,obj):
        self.pass_kernel_inputs()
        self.kernel.bip()
        self.sight_class_input.text = self.kernel.state
        return

    def check(self,obj):
        self.pass_kernel_inputs()
        self.kernel.check()
        self.show_kernel_outputs()
        return

    def clack(self,obj):
        self.pass_kernel_inputs()
        self.kernel.clack()
        self.show_kernel_outputs()
        return

    def pass_kernel_inputs(self):
        # Set working domain
        if self.words_tgl_btn.state == "down":
           self.kernel.set_working_domain("WORDS")
        else:
            self.kernel.set_working_domain("ADDITION")
        # Get patterns
        hearing_pattern = self.hearing_painter.get_pattern()
        sight_pattern = self.sight_painter.get_pattern()
        hearing_class = self.hearing_class_input.text
        hearing_knowledge = RbfKnowledge(hearing_pattern, hearing_class)
        sight_knowledge = RbfKnowledge(sight_pattern, "NoClass")
        self.kernel.set_hearing_knowledge_in(hearing_knowledge)
        self.kernel.set_sight_knowledge_in(sight_knowledge)

    def show_kernel_outputs(self):
        self.sight_class_input.text = self.kernel.state
        if self.kernel.state == "HIT":
            h_knowledge = self.kernel.get_hearing_knowledge_out()
            s_knowledge = self.kernel.get_sight_knowledge_out()
            if h_knowledge is not None:
                self.hearing_painter.draw_pattern(h_knowledge.get_pattern())
                self.hearing_class_input.text = self.kernel.get_hearing_knowledge_out().get_class()
            if s_knowledge is not None:
                self.sight_painter.draw_pattern(s_knowledge.get_pattern())
                self.sight_painter.draw_pattern(self.kernel.get_sight_knowledge_out().get_pattern())
        return

class MyPaintApp(App):
    def build(self):
        brainUI = BrainInterface()
        return brainUI


if __name__ == '__main__':
    MyPaintApp().run()
