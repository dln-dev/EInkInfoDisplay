# Frame creator and manipulator ("view")
# Here, all frames are created and displayed

#import shapes
import epd4in2b
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
#COLORED = 1
#UNCOLORED = 0
#
# Display dimensions (pixel)
WIDTH = epd4in2b.EPD_WIDTH
HEIGHT = epd4in2b.EPD_HEIGHT

epd = epd4in2b.EPD()
epd.init()

VERSION = "0.1a"

class Frame:
    def __init__(self, colors = "both"):
        if not colors == "red":
            self.__blackImg = Image.new('1', (WIDTH, HEIGHT), 255)    # 255: clear the frame
            self.__blackDraw = ImageDraw.Draw(self.__blackImg)
        if not colors == "black":
            self.__redImg = Image.new('1', (WIDTH, HEIGHT), 255)    # 255: clear the frame
            self.__redDraw = ImageDraw.Draw(self.__redImg)

        self.__shapes = []
        self.__drawn = False

    def addShape(self, shape):
        # shitty workaround for missing "textsize()" feature:
        #if shape.__class__.__name__ == "Text":
        #    shape.setCenter(self.__redDraw)
        self.__shapes.append(shape)
        self.__drawn = False

    def addShapes(self, shapes):
        for shape in  shapes:
            self.addShape(shape)

    def removeShape(self, shape):
        print("removeShape(shape) not yet implemented")
        #self.__drawn = False

    def draw(self):
        for shape in self.__shapes:
            shape.draw(self.__blackDraw, self.__redDraw)
            self.__drawn = True

    def display(self):
        if self.__drawn == False:
            self.draw()
        epd.display_frame(epd.get_frame_buffer(self.__blackImg), epd.get_frame_buffer(self.__redImg))



