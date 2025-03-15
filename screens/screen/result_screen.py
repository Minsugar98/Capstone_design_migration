from kivy.uix.screenmanager import Screen
from lib.circle_detection import detect_and_draw_circles
import cv2
from config import AppConfig
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.checkbox import CheckBox
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from lib.BrailleToKor_Python_main.src.BrailleToKorean.BrailleToKor import BrailleToKor
from lib.compare_text import compare_text
import pytesseract
from lib.crm import braille_to_korean

class ResultScreen(Screen):
    def on_enter(self, *args):
        self.imgtoText()
    my_list = []
    result = [0, 0, 0, 0, 0, 0]

    def braille(self):
        detect_and_draw_circles(AppConfig.FILE_PATHS['upload'], AppConfig.FILE_PATHS['output'])
        img1 = cv2.imread(AppConfig.FILE_PATHS['output'], cv2.IMREAD_COLOR)
        # img1 = 125 - img1
        mask = cv2.imread(AppConfig.FILE_PATHS['output'], cv2.IMREAD_GRAYSCALE)
        mask = 255 - mask
        dst = cv2.imread(AppConfig.FILE_PATHS['resize'], cv2.IMREAD_COLOR)

        h, w = img1.shape[:2]

        crop = dst[0:h, 0:w]

        cv2.copyTo(img1, mask, crop)
        cv2.imwrite(AppConfig.FILE_PATHS['resize'], dst)

    def add_list(self, instance):
        self.my_list.append(self.textinput.text)
        self.textinput.text = ""

    def print_list(self, instance):
        print(self.my_list)

    def add_list(self):
        self.my_list.append(self.text_input4.text)
        self.text_input4.text = ""

    def print_list(self):
        my_list_text = '\n'.join(self.my_list)
        label = Label(text=my_list_text, font_name=AppConfig.FONT_PATHS['fontName2'])

        # create a popup widget and add the label to it
        popup = Popup(title='Log', content=label, size_hint=(0.8, 0.8))

        # open the popup
        popup.open()

    def add_text(self, *args):
        text_to_add = self.result.text
        self.textinput1.text += text_to_add

    def print_result(self, *args):
        # 체크박스 상태 확인 및 결과 출력
        self.result[0] = int(self.checkbox1.active)
        self.result[3] = int(self.checkbox2.active)
        self.result[1] = int(self.checkbox3.active)
        self.result[4] = int(self.checkbox4.active)
        self.result[2] = int(self.checkbox5.active)
        self.result[5] = int(self.checkbox6.active)

        print(self.result)

        braille_code = ''.join(map(str, self.result))
        print(braille_code)
        for code, char in AppConfig.BRAILLE:
            if code == braille_code:
                self.string = char
                print(char)
                return char

    def retranslation(self):  ## 이부분 수정중 .. 점자 수정후 -> 다시 번역했을때 텍스트인풋2에 들어가야함 .. 하지만 출력은 잘나오는데 수정을 못하겠음
        trans = self.text_input1.text
        b = BrailleToKor()
        korean_text = b.translation(trans)
        self.remove_widget(self.text_input2)  # 기존의 text_input2 삭제
        self.text_input2 = TextInput(text=korean_text, disabled=True, font_name=AppConfig.FONT_PATHS['fontName2'], font_size=80, size =(900,120), size_hint=(None,None),
                                     x=450,
                                     y=600)  # 새로운 text_input2 생성
        self.add_widget(self.text_input2)
        print(korean_text)




    def cursor_number(self, *args):
        pos = self.text_input1.cursor_index()
        my_string = self.print_result()
        self.text_input1.text = self.text_input1.text[:pos] + my_string + self.text_input1.text[pos:]
        self.retranslation()
        print(pos)

    def retest(self):
        print("3",self.text_input3.text)
        print("2",self.text_input2.text)
        test_input2 = self.text_input2.text.strip()
        print("result",test_input2)
        result2 = compare_text(self.text_input3.text, test_input2)
        popup_label = Label(text=result2, font_name=AppConfig.FONT_PATHS['fontName2'], font_size=40)
        popup = Popup(title='', content=popup_label, size_hint=(None, None), size=(600, 600), title_align='right',
                      auto_dismiss=True)

        popup.open()

    def imgtoText(self):

        a = braille_to_korean(AppConfig.FILE_PATHS['resize'])
        b = BrailleToKor()
        korean_text = b.translation("⠑⠕⠠⠝⠬")

        OCR_text = pytesseract.image_to_string(AppConfig.FILE_PATHS['upload2'], lang='kor')
        # print(OCR_text)
        OCR_text = OCR_text.strip()
        print(OCR_text)
        # print(a[0])
        # print(a[1])
        self.text_input = TextInput()
        self.text_input2 = TextInput()
        self.text_input3 = TextInput()
        self.ids.textinput = TextInput()
        self.ids.textinput2 = TextInput()
        self.ids.textinput3 = TextInput()

        self.text_input1 = TextInput(text="⠑⠕⠠⠝⠬", font_name=AppConfig.FONT_PATHS['fontName'], font_size=80, size =(900,120), size_hint=(None,None),
                                     x=450,
                                     y=800)
        self.add_widget(self.text_input1)

        self.text_input2 = TextInput(text=korean_text,  disabled=True,font_name=AppConfig.FONT_PATHS['fontName2'], font_size=80, size =(900,120), size_hint=(None,None),
                                     x=450,
                                     y=600)
        self.add_widget(self.text_input2)
        self.text_input3 = TextInput(text=OCR_text, font_name=AppConfig.FONT_PATHS['fontName2'], font_size=80, size =(900,120), size_hint=(None,None),
                                     x=450,
                                     y=400)
        self.add_widget(self.text_input3)
        text_input2 = self.text_input2.text
        text_input2 = text_input2.strip()
        result = compare_text(OCR_text, text_input2)

        self.text_input4 = TextInput(text="", font_name=AppConfig.FONT_PATHS['fontName2'], size_hint_y=None, size_hint_x=None, size=(900, 240), x=450, y=100)
        self.add_widget(self.text_input4)


        ###### 텍스트 인풋에 일치한지.. 출력하는거 팝업창으로 만들었기때문에 필요없음. 만약 보고싶다면 주석풀고 사용.
        # text_input3 = TextInput(text=result, font_name=fontName2, font_size=80, height=120, size_hint_y=None, x=0, y=312)
        # self.add_widget(text_input3)
        #################

        # print(text_input2)

        # 문자 비교 text_input

        popup_label = Label(text=result, font_name=AppConfig.FONT_PATHS['fontName2'], font_size=40)
        popup = Popup(title='', content=popup_label, size_hint=(None, None), size=(600, 600), title_align='right',
                      auto_dismiss=True)

        popup.open()

        print(result)

        #### 그룹체크박승 생성
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

        self.button = Button(text='입력', font_name=AppConfig.FONT_PATHS['fontName2'], size_hint=(None, None), size=(200, 60), x=1380, y=550)
        self.button.bind(on_press=self.cursor_number)
        self.add_widget(self.button)

        self.button = Button(text='재비교', font_name=AppConfig.FONT_PATHS['fontName2'], size_hint=(None, None), size=(200, 60), x=1380, y=490)
        self.button.bind(on_press=lambda _: self.retest())
        self.add_widget(self.button)

        self.button = Button(text='메모저장', font_name=AppConfig.FONT_PATHS['fontName2'], size_hint=(None, None), size=(200, 120), x=1380, y=220)
        self.button.bind(on_press=lambda _: self.add_list())
        self.add_widget(self.button)

        self.button = Button(text='메모출력', font_name=AppConfig.FONT_PATHS['fontName2'], size_hint=(None, None), size=(200, 120), x=1380, y=100)
        self.button.bind(on_press=lambda _: self.print_list())
        self.add_widget(self.button)

        grid.x = self.width - grid.width - 50
        grid.y = (self.height - grid.height) / 2 +180



        self.add_widget(grid)

        label = Label(text="인식 점자", color=(0,0,0,1),font_name=AppConfig.FONT_PATHS['fontName2'], font_size=50, size_hint=(None, None),x=210,y=820,)
        self.add_widget(label)
        label = Label(text="점자 번역", color=(0, 0, 0, 1), font_name=AppConfig.FONT_PATHS['fontName2'], font_size=50, size_hint=(None, None),
                      x=210, y=620)
        self.add_widget(label)
        label = Label(text="인식 문자", color=(0, 0, 0, 1), font_name=AppConfig.FONT_PATHS['fontName2'], font_size=50, size_hint=(None, None),
                      x=210, y=420)
        self.add_widget(label)
        label = Label(text="메모", color=(0, 0, 0, 1), font_name=AppConfig.FONT_PATHS['fontName2'], font_size=50, size_hint=(None, None),
                      x=210, y=180, )
        self.add_widget(label)
    pass