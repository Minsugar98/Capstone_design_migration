from kivy.uix.screenmanager import Screen
from kivy.uix.checkbox import CheckBox
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color, Rectangle
from lib.BrailleToKor_Python_main.src.BrailleToKorean.BrailleToKor import BrailleToKor
from config import AppConfig
class JumtxttokoScreen(Screen):
    result = [0, 0, 0, 0, 0, 0]
    def on_enter(self, *args):
        self.start()

    def cursor_number(self, *args):
        pos = self.text_input1.cursor_index()
        my_string = self.print_result()
        self.text_input1.text = self.text_input1.text[:pos] + my_string + self.text_input1.text[pos:]
        self.retranslation()
        # print(pos)

    def retranslation(self):  ## 이부분 수정중 .. 점자 수정후 -> 다시 번역했을때 텍스트인풋2에 들어가야함 .. 하지만 출력은 잘나오는데 수정을 못하겠음
        trans = self.text_input1.text
        b = BrailleToKor()
        korean_text = b.translation(trans)
        self.remove_widget(self.text_input2)  # 기존의 text_input2 삭제
        self.text_input2 = TextInput(text=korean_text, disabled=True, font_name=AppConfig.FONT_PATHS['fontName2'], font_size=80, size =(900,120), size_hint=(None,None),
                                     x=500,
                                     y=300)  # 새로운 text_input2 생성
        self.add_widget(self.text_input2)
        # print(korean_text)

    def print_result(self, *args):
        # 체크박스 상태 확인 및 결과 출력
        self.result[0] = int(self.checkbox1.active)
        self.result[3] = int(self.checkbox2.active)
        self.result[1] = int(self.checkbox3.active)
        self.result[4] = int(self.checkbox4.active)
        self.result[2] = int(self.checkbox5.active)
        self.result[5] = int(self.checkbox6.active)

        # print(self.result)

        braille_code = ''.join(map(str, self.result))
        # print(braille_code)
        for code, char in AppConfig.BRAILLE:
            if code == braille_code:
                self.string = char  
                # print(char)
                return char



#### 여기서부터해..
    def start(self):
        with self.canvas:
            Color(148/255, 193/255, 1, 1)  # 백그라운드 컬러 설정
            Rectangle(pos=(180,300),
                      size=(300, 120))  # text_input1에 대한 사각형 그리기
            Rectangle(pos=(180,700),
                      size=(300, 120))  # text_input2에 대한 사각형 그리기

        label = Label(text="한글", color=(0, 0, 0, 1), font_name=AppConfig.FONT_PATHS['fontName2'], font_size=50, size_hint=(None, None),
                      x=275, y=315, )
        self.add_widget(label)
        label = Label(text="점자", color=(0, 0, 0, 1), font_name=AppConfig.FONT_PATHS['fontName2'], font_size=50, size_hint=(None, None),
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

        #self.button = Button(text='번역', font_name=fontName2, size_hint=(None, None), size=(200, 120), x=700, y=500)
        #self.button.bind(on_press=lambda _: self.retranslation())
        #self.add_widget(self.button)
        self.checkbox1 = CheckBox(group='group1')
        self.checkbox2 = CheckBox(group='group2')
        self.checkbox3 = CheckBox(group='group3')
        self.checkbox4 = CheckBox(group='group4')
        self.checkbox5 = CheckBox(group='group5')
        self.checkbox6 = CheckBox(group='group6')

        grid = GridLayout(cols=2, rows=3, spacing=10, size_hint=(None, None), size=(100, 200))
        grid.add_widget(self.checkbox1)
        grid.add_widget(self.checkbox2)
        grid.add_widget(self.checkbox3)
        grid.add_widget(self.checkbox4)
        grid.add_widget(self.checkbox5)
        grid.add_widget(self.checkbox6)

        grid.x = self.width - grid.width - 800
        grid.y = (self.height - grid.height) / 2-30
        self.add_widget(grid)

        self.button = Button(text='입력', font_name=AppConfig.FONT_PATHS['fontName2'], size_hint=(None, None), size=(100, 180), x=850, y=480)
        self.button.bind(on_press=self.cursor_number)
        self.add_widget(self.button)
    pass