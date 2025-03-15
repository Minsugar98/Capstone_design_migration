from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle
from kivy.core.text import LabelBase
from kivy.resources import resource_add_path
from kivy.uix.behaviors import FocusBehavior
from lib.KorToBraille.KorToBraille import KorToBraille
from config import AppConfig


class KotojumtxtScreen(Screen):
    def on_enter(self, *args):
        self.start()

    def KortoBraille(self):
        result_text = self.text_input1.text
        b = KorToBraille()
        result_braille = b.korTranslate(result_text)
        self.remove_widget(self.text_input2)
        self.text_input2 = TextInput()
        self.text_input2 = TextInput(text=result_braille, font_name=AppConfig.FONT_PATHS['fontName'], font_size=80, size=(900, 120), size_hint=(
            None, None),
                                     x=500,
                                     y=300)
        self.add_widget(self.text_input2)

    def cursor_number(self, *args):
        pos = self.text_input1.cursor_index()
        my_string = self.print_result()
        self.text_input1.text = self.text_input1.text[:pos] + my_string + self.text_input1.text[pos:]
        print(pos)





    def start(self):
        with self.canvas:
            Color(148/255, 193/255, 1, 1)  # 백그라운드 컬러 설정
            Rectangle(pos=(180,300),
                      size=(300, 120))  # text_input1에 대한 사각형 그리기
            Rectangle(pos=(180,700),
                      size=(300, 120))  # text_input2에 대한 사각형 그리기

        label = Label(text="점자", color=(0, 0, 0, 1), font_name=AppConfig.FONT_PATHS['fontName2'], font_size=50, size_hint=(None, None),
                      x=275, y=315, )
        self.add_widget(label)
        label = Label(text="한글", color=(0, 0, 0, 1), font_name=AppConfig.FONT_PATHS['fontName2'], font_size=50, size_hint=(None, None),
                      x=275, y=715)
        self.add_widget(label)

        self.text_input1 = TextInput()
        self.text_input1 = TextInput(text='', font_name = AppConfig.FONT_PATHS['fontName2'], font_size = 80, size = (900, 120), size_hint = (
        None, None),
        x = 500,
        y = 700)
        self.add_widget(self.text_input1)

        self.text_input2 = TextInput(text='', font_name=AppConfig.FONT_PATHS['fontName2'], font_size=80, size=(900, 120), size_hint=(
            None, None),
                                     x=500,
                                     y=300)
        self.add_widget(self.text_input2)

        self.button = Button(text='번역', font_name=AppConfig.FONT_PATHS['fontName2'], size_hint=(None, None), size=(200, 120), x=700, y=500)
        self.button.bind(on_press=lambda _: self.KortoBraille())
        self.add_widget(self.button)





        pass
