# Helper classes for common objects ("model")
# This creates shapes, text etc. for the frames

from abc import ABCMeta, abstractmethod
#import epd4in2b
from PIL import Image
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
            self.color = "red"
        else:
            self.color = "black"

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


class Ellipse(Rect):
    def __init__(self, \
                 upperLeftCoords, \
                 lowerRightCoords, \
                 startAngle, \
                 endAngle, \
                 color, \
                 fill, \
                 outline):    # defaults?

        self.startAngle = startAngle
        self.endAngle   = endAngle
        self.coords     = (upperLeftCoords[0],  upperLeftCoords[1], \
                           lowerRightCoords[0], lowerRightCoords[1]) 
        Rect.__init__(self, upperLeftCoords, lowerRightCoords, color, fill, outline) 
        
        if outline in FILLS: # use function call instead?
            self.outline = outline
        elif outline is None: # None: use pieslice, otherwise arc
            self.outline = None
        else:
            raise ValueError("unrecognized outline: '%s'", outline)

    def setOutline(self, outline):
        if outline in FILLS:
            self.outline = outline
        elif outline is None:
            self.outline = None
        else:
            raise ValueError("unrecognized outline: '%s'", outline)

    def draw(self, blackImg, redImg):
        if self.color == "red":
            if self.outline is None:
                redImg.arc([*self.coords], self.startAngle, self.endAngle, self.fill)
            else:
                redImg.pieslice([*self.coords], self.startAngle, self.endAngle, self.fill, self.outline)
        else:
            if self.outline is None:
                blackImg.arc([*self.coords], self.startAngle, self.endAngle, self.fill)
            else:
                blackImg.pieslice([*self.coords], self.startAngle, self.endAngle, self.fill, self.outline)




class Text(Shape):
    def __init__(self, text, center, color, fontsize, fill):
        Shape.__init__(self, center, color, fill)
        self.fontsize = fontsize
        self.font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', self.fontsize)
        self.text = text
        self.upperLeftCoords = (-1, -1) # unfortunately, this can really onl be set in draw()

    def setCenter(self, center):
        self.setBaseCoords(center)

    def setUpperLeftCoords(self, coords):
        self.upperLeftCoords = coords

    def setText(self, text):
        self.text = text

    def getCenter(self):
        return self.baseCoords

    def draw(self, blackImg, redImg):
        if self.upperLeftCoords != (-1, -1): # apply shift if upperLeftCoords is set
            self.setCenter(\
                    (self.upperLeftCoords[0] + redImg.textsize(self.text, font = self.font)[0] // 2, \
                     self.upperLeftCoords[1] + redImg.textsize(self.text, font = self.font)[1] // 2))
        if self.color == "red":
            redImg.text((self.baseCoords[0] - redImg.textsize(self.text, font = self.font)[0] // 2, \
                         self.baseCoords[1] - redImg.textsize(self.text, font = self.font)[1] // 2), \
                         self.text, font = self.font, fill = self.fill)
        else:
            blackImg.text((self.baseCoords[0] - blackImg.textsize(self.text, font = self.font)[0] // 2, \
                           self.baseCoords[1] - blackImg.textsize(self.text, font = self.font)[1] // 2), \
                           self.text, font = self.font, fill = self.fill)


class Picture(Rect):
    def __init__(self, \
                 upperLeftCoords, \
                 lowerRightCoords, \
                 color, \
                 fill, \
                 outline, \
                 blackImg, \
                 redImg):
        Rect.__init__(self, upperLeftCoords, lowerRightCoords, color, fill, outline)
        # bmps must be inverted and monochrome (convert -monochrome)
        self.blackImg = Image.open('Images/'+blackImg+'.bmp').convert('1')
        self.redImg   = Image.open('Images/'+ redImg +'.bmp').convert('1')

#frame_black = epd.get_frame_buffer(Image.open('black.bmp'))
    #frame_red = epd.get_frame_buffer(Image.open('red.bmp'))
    #epd.display_frame(frame_black, frame_red)

    def setImgNames(self, blackImg, redImg):
        self.blackImg = Image.open('Images/'+blackImg+'.bmp').convert('1')
        self.redImg = Image.open('Images/'+redImg+'.bmp').convert('1')

    def invert(self, color):
        if color == "black":
            pass
        elif color == "red":
            pass
        elif color == "both":
            pass
        else:
            raise(ValueError("Unrecognized color %s", color))

    def switch(self):
        tmp = self.blackImg
        self.blackImg = self.redImg
        self.redImg = tmp

    def draw(self, blackImg, redImg):
        redImg.bitmap(  (self.coords[0],self.coords[1]), self.redImg, 0)
        blackImg.bitmap((self.coords[0],self.coords[1]), self.blackImg, 0)


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
 
    def __newCenter(self):
        if len(self.entries) == 0:
            return self.rectWidth  // 2 + self.coords[0], \
                   self.rectHeight // 2 + self.coords[1]
        else: # this must be easier...
            return ((self.entries[0].getCenter()[0] + self.rectWidth * \
                    (len(self.entries) // self.dimY) - self.coords[0]) \
                    % (self.dimX * self.rectWidth)   + self.coords[0], \
                    (self.entries[-1].getCenter()[1] + self.rectHeight - self.coords[1]) \
                    % (self.dimY * self.rectHeight)  + self.coords[1])

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

    def addShapes(self, shapes):
        for shape in shapes:
            self.addShape(shape)

    def addBackground(self, color, fill, outline):
        self.background = Table((self.coords[0], self.coords[1]), \
                                (self.coords[2], self.coords[3]), \
                                 color, fill, outline, self.dimX, self.dimY)
        self.background.__fillRects(fill, outline)

    def removeBackground(self):
        self.background = None

    def invert(self, places = None):
        if places is None:
            places = range(0, self.dimX * self.dimY)
        for place in places:
            self.entries[place].invert()

    def invertBackgrounds(self, places = None):
        if places is None:
            places = range(0, self.dimX * self.dimY)
        for place in places:
            self.background.getEntry(place).invert()

    def invertCells(self, places = None):
        if places is None:
            places = range(0, self.dimX * self.dimY)
        self.invert(places)
        self.invertBackgrounds(places)

    def swap(self, places):
        if places is None:
            places = range(0, self.dimX * self.dimY)
        for place in places:
            self.entries[place].swap()

    def swapBackgrounds(self, places = None):
        if places is None:
            places = range(0, self.dimX * self.dimY)
        for place in places:
            self.background.getEntry(place).swap()

    def swapCells(self, places):
        if places is None:
            places = range(0, self.dimX * self.dimY)
        self.swap(places)
        self.swapBackgrounds(places)

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


