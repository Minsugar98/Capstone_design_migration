from kivy.uix.screenmanager import Screen

class CameraScreen(Screen):
    def capture(self):
        '''
        Function to capture the images and give them the names
        according to their captured time and date.
        '''
        camera = self.ids['camera']
        camera.export_to_png("kv/img/save.png")
        camera.play = not camera.play


    pass