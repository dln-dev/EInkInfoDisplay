# Helper classes for common objects ("model")
# This creates shapes, text etc. for the frames

from abc import ABCMeta, abstractmethod
#import epd4in2b
#from PIL import Image
from PIL import ImageFont
#from PIL import ImageDraw


#WIDTH = epd4in2b.EPD_WIDTH
#HEIGHT = epd4in2b.EPD_HEIGHT
COLORS = {"black", "red"}
FILLS = {0, 255}

# Base class for all shapes
class Shape(metaclass = ABCMeta):
    @abstractmethod
    def __init__(self, baseCoords, color, fill):   # "black" as default?

        self.baseCoords = baseCoords

        if color in COLORS:
            self.color = color
        else:
            raise ValueError("unrecognized color '%s'", color)

        if fill in FILLS:
            self.fill = fill
        else:
            raise ValueError("incorrect fill '%d'", fill)
    
    def setBaseCoords(self, coords):
        self.baseCoords = coords

    @abstractmethod
    def setCenter(self, center):
        pass

    def setColor(self, color):
        if color in COLORS:
            self.color = color
        else:
            raise ValueError("unrecognized color '%s'", color)


    def setFill(self, fill):
        if fill in FILLS:
            self.fill = fill
        else:
            raise ValueError("unrecognized fill '%d'", fill)


    def getBaseCoords(self):
        return self.baseCoords


    @abstractmethod
    def getCenter(self):
        pass


    def swap(self):
        if self.color == "black":
            self.color == "red"
        else:
            self.color == "black"

    def invert(self):
        if self.fill == 0:
            self.fill = 255
        else:
            self.fill = 0

    # both ImageDraw objects are given, so that frame can simply call "draw()"
    # there might be a better way, perhaps frame having two arrays of shapes
    # but then switching color is awkward
    @abstractmethod
    def draw(self, blackDraw, redDraw):
        pass



class Rect(Shape):
    def __init__(self, \
                 upperLeftCoords, \
                 lowerRightCoords, \
                 color, \
                 fill, \
                 outline):    # defaults?

        #Shape.__init__(self, self.getCenter(), color, fill)
        self.coords = (upperLeftCoords[0], upperLeftCoords[1], \
                         lowerRightCoords[0], lowerRightCoords[1]) 
        Shape.__init__(self, self.getCenter(), color, fill) # -> baseCoords = center
        #self.color = color
        #self.fill = fill
        if outline in FILLS: # use function call instead?
            self.outline = outline
        else:
            raise ValueError("unrecognized outline: '%s'", outline)

    def setCenter(self, center):
        halfWidth  = (self.coords[2] - self.coords[0]) // 2
        halfHeight = (self.coords[3] - self.coords[1]) // 2
        self.coords = (center[0] - halfWidth, center[1] - halfHeight, \
                       center[0] + halfWidth, center[1] + halfHeight)
                        # center[2] - halfWidth, center[3] - halfHeight)
        self.setBaseCoords((self.coords[0], self.coords[1]))

    def setOutline(self, outline):
        if outline in FILLS:
            self.outline = outline
        else:
            raise ValueError("unrecognized outline: '%s'", outline)


    def getCoords(self):
        return self.coords


    def getCenter(self):
        return (self.coords[0] + (self.coords[2] - self.coords[0]) // 2, \
                self.coords[1] + (self.coords[3] - self.coords[1]) // 2)


    def draw(self, blackImg, redImg):
        if self.color == "red":
            redImg.rectangle(self.coords, self.fill, self.outline)
        else:
            blackImg.rectangle(self.coords, self.fill, self.outline)


class Text(Shape):
    def __init__(self, text, center, color, fontsize, fill):
        Shape.__init__(self, center, color, fill)
        self.fontsize = fontsize
        self.font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', self.fontsize)
        self.text = text

    def setCenter(self, center):
        self.setBaseCoords(center)

    def setText(self, text):
        self.text = text

    def getCenter(self):
        return self.baseCoords

    def draw(self, blackImg, redImg):
        if self.color == "red":
            redImg.text((self.baseCoords[0] - redImg.textsize(self.text, font = self.font)[0] // 2, \
                         self.baseCoords[1] - redImg.textsize(self.text, font = self.font)[1] // 2), \
                         self.text, font = self.font, fill = self.fill)
        else:
            blackImg.text((self.baseCoords[0] - blackImg.textsize(self.text, font = self.font)[0] // 2, \
                           self.baseCoords[1] - blackImg.textsize(self.text, font = self.font)[1] // 2), \
                           self.text, font = self.font, fill = self.fill)


class Table(Rect):
    def __init__(self, \
                 upperLeftCoords, \
                 lowerRightCoords, \
                 color, \
                 fill, \
                 outline, \
                 dimX, \
                 dimY): # dim = number of entries in table

        Rect.__init__(self, upperLeftCoords, lowerRightCoords, color, fill, outline)
        self.dimX = dimX
        self.dimY = dimY
        self.entries = []
        self.background = None
        self.rectWidth  = round((self.coords[2] - self.coords[0]) / dimX)
        self.rectHeight = round((self.coords[3] - self.coords[1]) / dimY) # rounding errors?
        print("upperLeftCoords: ", upperLeftCoords, "\nlowerRightCoords: ", lowerRightCoords)
        print("rectWidth: ", self.rectWidth, "\nrectHeight: ", self.rectHeight)
 
    def __newCenter(self):
        if len(self.entries) == 0:
            return self.rectWidth  // 2 + self.coords[0], \
                   self.rectHeight // 2 + self.coords[1]
        else:
            return ((self.entries[-1].getCenter()[0] + self.rectWidth - self.coords[0]) \
                    % (self.dimX * self.rectWidth) + self.coords[0], \
                    (self.entries[-1].getCenter()[1] + self.rectHeight - self.coords[1]) \
                    % (self.dimY * self.rectHeight) + self.coords[1])

    def __getRectCoords(self, center):
        return [(center[0] - self.rectWidth  // 2,  \
                 center[1] - self.rectHeight // 2), \
                (center[0] + self.rectWidth  // 2,
                 center[1] + self.rectHeight // 2)]


    def __fillRects(self, fill, outline):
        for i in range(0, self.dimX):
            for j in range(0, self.dimY):
                self.entries.append(Rect((self.coords[0] +     i * self.rectWidth, \
                                          self.coords[1] +     j * self.rectHeight), \
                                         (self.coords[0] + (i+1) * self.rectWidth, \
                                          self.coords[1] + (j+1) * self.rectHeight), \
                                          self.color, fill, outline))
        #for i in range(0, self.dimX * self.dimY):
        #    self.entries.append(Rect(*self.__getRectCoords(self.__newCenter()), \
        #                        self.color, fill, outline))

    def addShape(self, shape):
        if len(self.entries) < self.dimX * self.dimY:
            shape.setCenter(self.__newCenter())
            self.entries.append(shape)
        else:
            print("Table full")

    def addBackground(self, color, fill, outline):
        self.background = Table((self.coords[0], self.coords[1]), \
                                (self.coords[2], self.coords[3]), \
                                 color, fill, outline, self.dimX, self.dimY)
        self.background.__fillRects(fill, outline)

    def removeBackground(self):
        self.background = None

    def invertBackground(self, places = None):
        if places is None:
            places = range(0, self.dimX, self.dimY)
        for place in places:
            self.background.getEntry(place).invert()

    def getEntry(self, place):
        return self.entries[place]

    def __drawOutline(self, blackImg, redImg):
        if self.rectHeight * self.dimY > self.coords[3] - self.coords[1]:
            if self.color == "red":
                redImg.line([(self.coords[0], self.coords[3]), \
                             (self.coords[2], self.coords[3])], 0, 1)
            else:
                blackImg.line([(self.coords[0], self.coords[3]), \
                             (self.coords[2], self.coords[3])], 0, 1)
        if self.rectWidth * self.dimX > self.coords[2] - self.coords[0]:
            if self.color == "red":
                redImg.line(self.coords, 0, 1)
            else:
                blackImg.line(self.coords, 0, 1)

    def draw(self, blackImg, redImg):  
        if self.color == "red":
            redImg.rectangle(self.coords, self.fill, self.outline)
        else:
            blackImg.rectangle(self.coords, self.fill, self.outline)
        if self.background: 
            self.background.draw(blackImg, redImg)
        for entry in self.entries:
            entry.draw(blackImg, redImg)
        self.__drawOutline(blackImg, redImg) # if rounding errors, draw outline manually (prob wonky)



#class Table(Rect):
#    def __init__(self, \
#                 upperLeftCoords, \
#                 lowerRightCoords, \
#                 color, \
#                 fill, \
#                 outline, \
#                 dimX, \
#                 dimY):
#
#        Rect.__init__(self, upperLeftCoords, lowerRightCoords, color, fill, outline)
#        self.dimX = dimX
#        self.dimY = dimY
#        self.rects = [] # max dimX * 
#        self.texts = [] # dimY entries
#
#    def fillRects(self, color = self.color, fill = self.fill, outline = self.outline):
#        rectWidth = (self.coords[2] - self.coords[0]) // dimX
#        rectHeight = (self.coords[3] - self.coords[1]) // dimY
#        for i in range(0, self.dimX):
#            for j in range(0, self.dimY):
#                self.rects.append(Rect((self.coords[0] + i * rectWidth, \
#                                         self.coords[1] + j * rectHeight), \
#                                        (self.coords[0] + (i+1) * rectWidth, \
#                                         self.coords[1] + (j+1) * rectHeight), \
#                                         color, \
#                                         fill, \
#                                         outline))
#
#    def fillTexts(self, texts, color = self.color, fill = self.fill):
#        rectWidth = (self.coords[2] - self.coords[0]) // dimX
#        rectHeight = (self.coords[3] - self.coords[1]) // dimY
#        fontsize = 2 * rectHeight // 3
#        for i in range(0, self.dimX):
#            for j in range(0, self.dimY):
#                self.texts.append(Text(texts[i*dimY + j], \
#                                         (self.coords[0] + (i + 0.5) * rectWidth, \
#                                          self.coords[1] + (j + 0.5) * rectHeight), \
#                                          color, fontsize, fill))
#
#    def getRect(self, pos):
#        return self.Rects[pos]
#
#    def getText(self, pos):
#        return self.texts[pos]
#
#
#    def draw(self, blackImg, redImg):  ### formerly drawTable(self)
#        for i in range(0, self.dimX * self.dimY):
#            self.entries[i].draw(blackImg, redImg)
#        if self.color == "red":
#            redImg.rectangle(self.coords, self.fill, self.outline)
#        else:
#            blackImg.rectangle(self.coords, self.fill, self.outline)
#
