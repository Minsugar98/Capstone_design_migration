import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from config import AppConfig

class ImageSlicer2:
    def __init__(self, img_path):
        self.img = mpimg.imread(img_path)
        self.fig, self.ax = plt.subplots()
        self.ax.imshow(self.img)
        self.coords = []

        self.fig.canvas.mpl_connect('button_press_event', self.on_press)
        self.fig.canvas.mpl_connect('button_release_event', self.on_release)

    def on_press(self, event):
        if event.button == 1: # left click
            self.coords = [event.xdata, event.ydata]

    def on_release(self, event):
        if event.button == 1: # left click
            self.coords += [event.xdata, event.ydata]
            self.draw_rect()
            self.save_cropped_img()

    def draw_rect(self):
        x1, y1, x2, y2 = self.coords
        rect = plt.Rectangle((x1, y1), x2-x1, y2-y1, linewidth=1, edgecolor='r', facecolor='none')
        self.ax.add_patch(rect)
        self.fig.canvas.draw()

    def save_cropped_img(self):
        x1, y1, x2, y2 = self.coords
        xmin, xmax = sorted([x1, x2])
        ymin, ymax = sorted([y1, y2])
        cropped_img = self.img[int(ymin):int(ymax), int(xmin):int(xmax)]
        mpimg.imsave(AppConfig.FILE_PATHS['upload2'], cropped_img)
        print('Image saved.')

    def show(self):
        plt.show()
