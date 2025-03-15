from kivy.app import App
from kivy.lang import Builder
import os

# 현재 파일의 디렉토리 경로를 가져옴
current_dir = os.path.dirname(os.path.abspath(__file__))

# KV 파일들 로드
kv_files = [
    'main.kv',
    os.path.join('screens', 'main_screen.kv'),
    os.path.join('screens', 'image_to_jum_screen.kv'),
    os.path.join('screens', 'koto_jum_txt_screen.kv'),
    os.path.join('screens', 'jum_txt_to_ko_screen.kv'),
    os.path.join('screens', 'album_screen.kv'),
    os.path.join('screens', 'edit_screen.kv'),
    os.path.join('screens', 'camera_screen.kv'),
    os.path.join('screens', 'result_screen.kv')
]

for kv_file in kv_files:
    kv_path = os.path.join(current_dir, 'kv', kv_file)
    if os.path.exists(kv_path):
        Builder.load_file(kv_path)
    else:
        print(f"Warning: KV file not found: {kv_path}")

class MyApp(App):
    def build(self):
        from screens.screen_manager import AppScreenManager
        return AppScreenManager()

if __name__ == '__main__':
    MyApp().run()