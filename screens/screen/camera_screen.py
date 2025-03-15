from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.logger import Logger
from kivy.graphics.texture import Texture
from config import AppConfig
import cv2
import os

class CameraScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.camera = None
        self.image = None
        self.is_capturing = False

    def on_enter(self):
        Logger.info('CameraScreen: 화면 진입')
        Clock.schedule_once(self.init_camera, 0.5)
        
    def init_camera(self, dt):
        try:
            # OpenCV 카메라 초기화
            Logger.info('Camera: OpenCV 카메라 초기화 중...')
            self.camera = cv2.VideoCapture(0)  # 첫 번째 카메라

            if self.camera.isOpened():
                # 카메라 설정
                self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
                
                # 이미지 위젯 설정 (카메라 위젯 대체)
                camera_layout = self.ids.camera_layout
                camera_layout.clear_widgets()
                
                self.image = Image(size_hint=(1, 1))
                camera_layout.add_widget(self.image)
                
                # 프레임 업데이트 시작
                self.is_capturing = True
                Clock.schedule_interval(self.update, 1.0/30.0)  # 30 FPS
                Logger.info('Camera: OpenCV 카메라 시작됨')
            else:
                Logger.error('Camera: OpenCV 카메라를 열 수 없음')
                self.show_camera_error()
        except Exception as e:
            Logger.error(f'Camera: 초기화 실패 - {e}')
            self.show_camera_error()
            
    def update(self, dt):
        if self.camera and self.is_capturing:
            ret, frame = self.camera.read()
            if ret:
                # OpenCV는 BGR, Kivy는 RGB 사용하므로 변환 필요
                buf = cv2.flip(frame, 0)  # 상하 반전 (Kivy 좌표계에 맞춤)
                buf = cv2.cvtColor(buf, cv2.COLOR_BGR2RGB)
                
                # 텍스처로 변환하여 이미지 위젯에 표시
                texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='rgb')
                texture.blit_buffer(buf.tobytes(), colorfmt='rgb', bufferfmt='ubyte')
                
                # 이미지 업데이트
                self.image.texture = texture
                
    def capture(self):
        if self.camera and self.is_capturing:
            try:
                if not os.path.exists('../../assets/img'):
                    os.makedirs('../../assets/img')
                    
                ret, frame = self.camera.read()
                if ret:
                    cv2.imwrite(AppConfig.FILE_PATHS['save'], frame)
                    Logger.info('Camera: 이미지 저장 완료')
            except Exception as e:
                Logger.error(f'Camera: 이미지 저장 실패 - {e}')
                
    def show_camera_error(self):
        from kivy.uix.label import Label
        
        camera_layout = self.ids.camera_layout
        camera_layout.clear_widgets()
        
        error_label = Label(
            text="카메라를 표시할 수 없습니다.", 
            font_size=24,
            color=(1, 0, 0, 1)  # 빨간색
        )
        camera_layout.add_widget(error_label)
                
    def on_leave(self):
        # 카메라 정리
        self.is_capturing = False
        Clock.unschedule(self.update)
        if self.camera:
            self.camera.release()
            self.camera = None
        Logger.info('Camera: 종료됨')