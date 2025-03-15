import sys
import os

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from screens.screen.main_screen import MainScreen
from screens.screen.image_to_jum_screen import ImagetojumScreen
from screens.screen.koto_jum_txt_screen import KotojumtxtScreen
from screens.screen.jum_txt_to_ko_screen import JumtxttokoScreen
from screens.screen.album_screen import AlbumScreen
from screens.screen.edit_screen import EditScreen
from screens.screen.camera_screen import CameraScreen
from screens.screen.result_screen import ResultScreen