from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from lib.Edit_img import ImageSlicer
from lib.Edit_img_2 import ImageSlicer2
from lib.circle_detection import detect_and_draw_circles
import cv2
from config import AppConfig


class EditScreen(Screen):
    def Editimg(self):
        slicer = ImageSlicer(AppConfig.FILE_PATHS['save'])
        slicer.show()

    def Editimg2(self):
        slicer = ImageSlicer2(AppConfig.FILE_PATHS['save'])
        slicer.show()

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


    pass