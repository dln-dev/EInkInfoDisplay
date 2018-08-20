# Helper classes for common objects ("model")
# This creates shapes, text etc. for the frames

import epd4in2b
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw


WIDTH = epd4in2b.EPD_WIDTH
HEIGHT = epd4in2b.EPD_HEIGHT


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
        if fill == 0:
            self.__outline = 255

    def draw(self, blackImg, redImg):
        if self.__color == "red":
            #self.__drawRed()
            redImg.rectangle(self.__coords, self.__fill, self.__outline)
        else:
            #self.__drawBlack()
            blackImg.rectangle(self.__coords, self.__fill, self.__outline)

    #def __drawRed(self):
    #    redImg.rectangle(self.__coords, self.__fill, self.__outline)

    #def __drawBlack(self):
    #    blackImg.rectangle(self.__coords, self.__fill, self.__outline)



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



    def draw(self, blackImg, redImg):  ### formerly drawTable(self)
        for i in range(0, self.__dimX * self.__dimY):
            self.__entries[i].draw(blackImg, redImg)


class Text:
    def __init__(self, text, center, color, height, fill):
        self.__height = height
        self.__font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', self.__height)
        self.__text = text
#        self.__width, self.__height = redImg.textsize(text, font = self.__font)
        self.__upperLeftX = center[0]# - ImageDraw.ImageDraw.textsize(self.__text, font = self.__font)[0] // 2  BROKEN WTF ---> Use "adjustFont() from frame object with images
        self.__upperLeftY = center[1]# - ImageDraw.ImageDraw.textsize(self.__text, font = self.__font)[1] // 2
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

    def setCenter(self, Img):
        self.__upperLeftX -= Img.textsize(self.__text, font = self.__font)[0] // 2 
        self.__upperLeftY -= Img.textsize(self.__text, font = self.__font)[1] // 2


    def draw(self, blackImg, redImg):
        if self.__color == "red":
            #self.__drawRed()
            redImg.text((self.__upperLeftX, self.__upperLeftY), self.__text, font = self.__font, fill = self.__fill)
        else:
            #self.__drawBlack()
            blackImg.text((self.__upperLeftX, self.__upperLeftY), self.__text, font = self.__font, fill = self.__fill)


    #def __drawRed(self):
    #    redImg.text((self.__upperLeftX, self.__upperLeftY), self.__text, font = self.__font, fill = self.__fill)

    #def __drawBlack(self):
    #    blackImg.text((self.__upperLeftX, self.__upperLeftY), self.__text, font = self.__font, fill = self.__fill)



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

