# Controller, catches signals and acts accordingly
# This is planned to use a gesture sensor APDS-9660

import epd4in2b
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw


WIDTH = epd4in2b.EPD_WIDTH
HEIGHT = epd4in2b.EPD_HEIGHT

# SETUP
image_red = Image.new('1', (WIDTH, HEIGHT), 255)    # 255: clear the frame
draw_red = ImageDraw.Draw(image_red)
image_black = Image.new('1', (WIDTH, HEIGHT), 255)    # 255: clear the frame
draw_black = ImageDraw.Draw(image_black)
#titleFont = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', 24)
#setFont = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', 18)


class Rect:
    def __init__(self, \
                 upperLeftX = 0, \
                 upperLeftY = 0, \
                 lowerRightX = WIDTH - 1, \
                 lowerRightY = HEIGHT - 1, \
                 color = "black", \
                 fill = 0, \
                 outline = 0):
        self.__coords = (upperLeftX, upperLeftY, lowerRightX, lowerRightY)
        self.__color = color
        self.__fill = fill
        self.__outline = outline

    def getCoords(self):
        return self.__coords

    def getCenter(self):
        return (self.__coords[0] + (self.__coords[2] - self.__coords[0]) // 2, \
                self.__coords[1] + (self.__coords[3] - self.__coords[1]) // 2)

    def getDrawRect(self):
        return self.__coords, self.__fill, self.__outline

    def setColor(self, color):
        self.__color = color

    def setFill(self, fill):
        self.__fill = fill

    def draw(self):
        if self.__color == "red":
            self.__drawRed()
        else:
            self.__drawBlack()

    def __drawRed(self):
        draw_red.rectangle(self.__coords, self.__fill, self.__outline)

    def __drawBlack(self):
        draw_black.rectangle(self.__coords, self.__fill, self.__outline)



class Table(Rect):
    def __init__(self, \
                 upperLeftX = 0, \
                 upperLeftY = 0, \
                 lowerRightX = WIDTH - 1, \
                 lowerRightY = HEIGHT - 1, \
                 color = "black", \
                 fill = 0, \
                 outline = 0, \
                 dimX = 1, \
                 dimY = 1, \
                 textArray = []):
        self.__coords = (min(WIDTH - 2, max(0, upperLeftX)), \
                         min(HEIGHT - 2, max(0, upperLeftY)), \
                         max(1, min(WIDTH - 1, lowerRightX)), \
                         max(1, min(HEIGHT - 1, lowerRightY)))
        self.__color = color
        self.__fill = fill
        self.__outline = outline
        #Rect.__init__(upperLeftX, upperLeftY, lowerRightX, lowerRightY, color, fill, outline)
        self.__dimX = dimX
        self.__dimY = dimY
        self.__entries = []
        rectWidth = (self.__coords[2] - self.__coords[0]) // dimX
        rectHeight = (self.__coords[3] - self.__coords[1]) // dimY
        for i in range(0, self.__dimX):
            for j in range(0, self.__dimY):
                self.__entries.append(Rect(self.__coords[0] + i * rectWidth, \
                                         self.__coords[1] + j * rectHeight, \
                                         self.__coords[0] + (i+1) * rectWidth, \
                                         self.__coords[1] + (j+1) * rectHeight, \
                                         self.__color, \
                                         self.__fill, \
                                         self.__outline))
                                         #' ', (WIDTH // 2, HEIGHT // 2), "black", 0, 255))

    def getRect(self, pos):
        return self.__entries[pos]

    def setText(self, array):
        for i in range(0, len(array)):
            self.__entries[i].setText(textArray[i], self.__entries[i].getCenter(), "black", (HEIGHT-60) // 15, 0)



    def drawTable(self):
        for i in range(0, self.__dimX * self.__dimY):
            self.__entries[i].draw()


class Text:
    def __init__(self, text, center, color, height, fill):
        self.__height = height
        self.__font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', self.__height)
        self.__text = text
#        self.__width, self.__height = draw_red.textsize(text, font = self.__font)
        self.__upperLeftX = center[0] - draw_red.textsize(text, font = self.__font)[0] // 2
        self.__upperLeftY = center[1] - draw_red.textsize(text, font = self.__font)[1] // 2
        self.__color = color
        self.__fill = fill

    def setFill(self, fill):
        self.__fill = fill

    def getCoords(self):
        return self.__upperLeftX, self.__upperLeftY

    def setText(self, text, center, color, height, fill):
        self.__init__(text, center, color, height, fill)

    def setColor(self, color):
        self.__color = color

    def setFill(self, fill):
        self.__fill = fill

    def draw(self):
        if self.__color == "red":
            self.__drawRed()
        else:
            self.__drawBlack()

    def __drawRed(self):
        draw_red.text((self.__upperLeftX, self.__upperLeftY), self.__text, font = self.__font, fill = self.__fill)

    def __drawBlack(self):
        draw_black.text((self.__upperLeftX, self.__upperLeftY), self.__text, font = self.__font, fill = self.__fill)



class tableEntry(Text, Rect):
    def __init__(self, text, center, tColor, height, tFill, \
                 upperLeftX = 0, \
                 upperLeftY = 0, \
                 lowerRightX = WIDTH - 1, \
                 lowerRightY = HEIGHT - 1, \
                 color = "black", \
                 fill = 0, \
                 outline = 0):
        Rect.__init__(self, \
                 upperLeftX = 0, \
                 upperLeftY = 0, \
                 lowerRightX = WIDTH - 1, \
                 lowerRightY = HEIGHT - 1, \
                 color = "black", \
                 fill = 0, \
                 outline = 0)
        Text.__init__(self, text, center, tColor, height, tFill)

    def draw(self):
        Rect.draw()
        Text.draw()

