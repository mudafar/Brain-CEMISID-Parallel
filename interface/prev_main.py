class BrainInterface(GridLayout):
    def __init__(self, **kwargs):
        super(BrainInterface, self).__init__(**kwargs)

        grid_size = 16

        self.kernel = KernelBrainCemisid()

        # Main layout number of columns
        self.rows = 2
        self.load_icons()
        self.declare_thinking_panel()
        self.declare_painters(grid_size)
        self.declare_inputs()
        self.declare_buttons()
        self.add_widgets_layouts()
        # Clear painters when window draw
        self.win_show_uid = Window.fbind('on_draw',self.clear)

    def load_icons(self):
        self.img_eye = Image(source='icons/eye.png')
        self.img_ear = Image(source='icons/ear.png')
        self.img_eye.size_hint = (None,None)
        self.img_ear.size_hint = (None,None)
        self.img_eye.width = 60
        self.img_ear.width = 60

    def declare_painters(self, grid_size):
        self.sight_painter = MyPaintWidget(grid_size)
        self.sight_painter.size_hint = (None, None)
        self.sight_painter.size = (200,200)
        self.hearing_painter = MyPaintWidget(grid_size)
        self.hearing_painter.size_hint = (None, None)
        self.hearing_painter.size = (200,200)

    def declare_thinking_panel(self):
        self.thinking_panel = GridLayout(rows=2, size_hint_x=0.6, padding=20)
        self.thinking_sight = MyGroupPaintWidget(padding=2*self.height/3)
        self.thinking_hearing = MyGroupPaintWidget(padding=2*self.height/3)
        self.thinking_panel.add_widget(self.thinking_sight)
        self.thinking_panel.add_widget(self.thinking_hearing)

    def declare_inputs(self):
        self.hearing_class_input = TextInput(text="Class?")
        self.hearing_class_input.size_hint = (None,None)
        self.hearing_class_input.height = 25

    def declare_buttons(self):
        # sight clear
        self.sight_clear_btn = Button(text="Clear S")
        self.sight_clear_btn.bind(on_release=self.sight_clear)

        # Hearing clear
        self.hearing_clear_btn = Button(text="Clear H")
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

        # Set-zero button
        self.zero_btn = Button(text="0 sign")
        self.zero_btn.bind(on_release=self.set_zero)

        # Set-equal-sign button
        self.equal_btn = Button(text="= sign")
        self.equal_btn.bind(on_release=self.set_equal_sign)

        # Set-add-operator button
        self.add_operator_btn = Button(text="+ sign")
        self.add_operator_btn.bind(on_release=self.set_add_operator)

        # Toggle button (Words, Numbers)
        self.words_tgl_btn = ToggleButton(text="Reading", group="bbcc_protocol", allow_no_selection=False)
        self.addition_tgl_btn = ToggleButton(text="Addition", group="bbcc_protocol", state="down", allow_no_selection=False)
        self.counting_tgl_btn = ToggleButton(text="Counting", group="bbcc_protocol", allow_no_selection=False)

    def add_widgets_layouts(self):
        # Sight panel
        self.sight_panel = GridLayout(rows=1, padding=10, spacing=10)
        self.sight_panel.add_widget(self.img_eye)
        self.sight_panel.add_widget(self.sight_painter)
        # Hearing panel
        self.hearing_painter_text = GridLayout(cols=1)
        self.hearing_painter_text.add_widget(self.hearing_painter)
        self.hearing_painter_text.add_widget(self.hearing_class_input)
        self.hearing_panel = GridLayout(rows=1, padding=10, spacing=10)
        self.hearing_class_input.font_size = 12
        self.hearing_panel.add_widget(self.img_ear)
        self.hearing_panel.add_widget(self.hearing_painter_text)

        self.main_panel = GridLayout(cols=2, size_hint=(1,0.9))
        self.senses_panel = GridLayout(rows=2, padding=10, size_hint_x=0.4)
        self.senses_panel.add_widget(self.sight_panel)
        self.senses_panel.add_widget(self.hearing_panel)
        self.main_panel.add_widget(self.senses_panel)
        self.main_panel.add_widget(self.thinking_panel)

        # Add widgets to bottom layout
        self.buttons_panel = GridLayout(rows=1, size_hint=(1,0.1))
        self.buttons_panel.add_widget(self.bum_btn)
        self.buttons_panel.add_widget(self.bip_btn)
        self.buttons_panel.add_widget(self.check_btn)
        self.buttons_panel.add_widget(self.clack_btn)
        self.buttons_panel.add_widget(self.sight_clear_btn)
        self.buttons_panel.add_widget(self.hearing_clear_btn)
        self.buttons_panel.add_widget(self.zero_btn)
        self.buttons_panel.add_widget(self.add_operator_btn)
        self.buttons_panel.add_widget(self.equal_btn)
        self.buttons_panel.add_widget(self.words_tgl_btn)
        self.buttons_panel.add_widget(self.addition_tgl_btn)
        self.buttons_panel.add_widget(self.counting_tgl_btn)
        self.add_widget(self.main_panel)
        self.add_widget(self.buttons_panel)

    def learn(self,obj):
        return

    def hearing_clear(self, obj):
        self.hearing_painter.clear()
        self.hearing_class_input.text = "Class?"
        self.thinking_hearing.clear()

    def sight_clear(self, obj):
        self.sight_painter.clear()
        self.thinking_sight.clear()

    def bum(self,obj):
        self.pass_kernel_inputs()
        self.kernel.bum()
        #self.sight_class_input.text = self.kernel.state
        return

    def bip(self,obj):
        self.pass_kernel_inputs()
        self.kernel.bip()
        self.show_kernel_outputs()
        #self.sight_class_input.text = self.kernel.state
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
           self.kernel.set_working_domain("READING")
        elif self.addition_tgl_btn.state == "down":
            self.kernel.set_working_domain("ADDITION")
        else:
            self.kernel.set_working_domain("COUNTING")
        # Get patterns
        hearing_pattern = self.hearing_painter.get_pattern()
        sight_pattern = self.sight_painter.get_pattern()
        hearing_class = self.hearing_class_input.text
        hearing_knowledge = RbfKnowledge(hearing_pattern, hearing_class)
        sight_knowledge = RbfKnowledge(sight_pattern, "NoClass")
        self.kernel.set_hearing_knowledge_in(hearing_knowledge)
        self.kernel.set_sight_knowledge_in(sight_knowledge)

    def show_kernel_outputs(self):
        self.thinking_clear()
        self.hearing_class_input.text = self.kernel.state
        if self.kernel.state == "HIT":
            h_knowledge = self.kernel.get_hearing_knowledge_out()
            s_knowledge = self.kernel.get_sight_knowledge_out()
            if h_knowledge is not None:
                self.thinking_hearing.show_rbf_knowledge(h_knowledge)
            if s_knowledge is not None:
                self.thinking_sight.show_rbf_knowledge(s_knowledge)

    def thinking_clear(self):
        self.thinking_sight.clear()
        self.thinking_hearing.clear()

    def clear(self, obj):
        self.sight_clear(None)
        self.hearing_clear(None)
        self.thinking_clear()
        Window.unbind_uid('on_draw', self.win_show_uid)

    def set_zero(self, obj):
        self.pass_kernel_inputs()
        self.kernel.set_zero()
        return

    def set_add_operator(self, obj):
        self.pass_kernel_inputs()
        self.kernel.set_add_operator()
        return

    def set_equal_sign(self, obj):
        self.pass_kernel_inputs()
        self.kernel.set_equal_sign()
        return
