import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder
from kivy.resources import resource_add_path
from kivy.logger import Logger  # 로깅 추가

# 현재 파일의 디렉토리 경로를 가져옴
current_dir = os.path.dirname(os.path.abspath(__file__))
# 프로젝트 루트 디렉토리
project_root = os.path.dirname(current_dir)
kv_path = os.path.join(project_root, 'kv')

# 디버깅을 위한 print문 추가
print(f"Loading KV files from: {kv_path}")

# 디버깅을 위한 로깅
Logger.info(f'Current directory: {current_dir}')
Logger.info(f'Project root: {project_root}')
Logger.info(f'Image path: {os.path.join(project_root, "kv", "images")}')

try:
    # 각 KV 파일 로드 시도
    for kv_file in [
        'main.kv',
        os.path.join('screens', 'main_screen.kv'),
        os.path.join('screens', 'image_to_jum_screen.kv'),
        os.path.join('screens', 'koto_jum_txt_screen.kv'),
        os.path.join('screens', 'jum_txt_to_ko_screen.kv'),
        os.path.join('screens', 'album_screen.kv'),
        os.path.join('screens', 'edit_screen.kv'),
        os.path.join('screens', 'camera_screen.kv'),
        os.path.join('screens', 'result_screen.kv'),
        os.path.join('components', 'upper_bar.kv'),
        os.path.join('components', 'help_popup.kv')
    ]:
        full_path = os.path.join(kv_path, kv_file)
        print(f"Loading: {full_path}")
        if os.path.exists(full_path):
            Builder.load_file(full_path)
        else:
            print(f"File not found: {full_path}")
except Exception as e:
    print(f"Error loading KV files: {e}")

from screens.screen.main_screen import MainScreen
from screens.screen.image_to_jum_screen import ImagetojumScreen
from screens.screen.koto_jum_txt_screen import KotojumtxtScreen
from screens.screen.jum_txt_to_ko_screen import JumtxttokoScreen
from screens.screen.album_screen import AlbumScreen
from screens.screen.edit_screen import EditScreen
from screens.screen.camera_screen import CameraScreen
from screens.screen.result_screen import ResultScreen
from screens.components.upper_bar import UpperBar
from screens.components.help_popup import HelpPopup

class AppScreenManager(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        print("Initializing AppScreenManager")
        screens = [
            MainScreen(name='main'),
            ImagetojumScreen(name='itoj'),
            KotojumtxtScreen(name='ktojt'),
            JumtxttokoScreen(name='jttok'),
            CameraScreen(name='came'),
            AlbumScreen(name='alb'),
            ResultScreen(name='Res'),
            EditScreen(name='ed')
        ]
        for screen in screens:
            print(f"Adding screen: {screen.name}")
            self.add_widget(screen)

class MainApp(App):
    def build(self):
        return AppScreenManager()

if __name__ == '__main__':
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    image_path = os.path.join(project_root, 'kv', 'img')

    if os.path.exists(image_path):
        Logger.info(f'Images in directory: {os.listdir(image_path)}')
        resource_add_path(image_path)
    else:
        Logger.error(f'Image directory not found: {image_path}')
    MainApp().run()