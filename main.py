##
 #  @filename   :   main.cpp
 #  @brief      :   4.2inch e-paper display (B) demo
 #  @author     :   Yehui from Waveshare
 #
 #  Copyright (C) Waveshare     August 15 2017
 #
 # Permission is hereby granted, free of charge, to any person obtaining a copy
 # of this software and associated documnetation files (the "Software"), to deal
 # in the Software without restriction, including without limitation the rights
 # to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 # copies of the Software, and to permit persons to  whom the Software is
 # furished to do so, subject to the following conditions:
 #
 # The above copyright notice and this permission notice shall be included in
 # all copies or substantial portions of the Software.
 #
 # THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 # IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 # FITNESS OR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 # AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 # LIABILITY WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 # OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 # THE SOFTWARE.
 ##

import epd4in2b
import models
#from PIL import Image
#from PIL import ImageFont
#from PIL import ImageDraw

COLORED = 1
UNCOLORED = 0
# Display is 400x300px
WIDTH = epd4in2b.EPD_WIDTH
HEIGHT = epd4in2b.EPD_HEIGHT

def main():
    epd = epd4in2b.EPD()
    epd.init()

    textfile = open("sets.txt", "r")
    setArray = textfile.read().split('\n')
    sets = []

    # SETUP FRAMES
    titleHeight = 60
    titleRect = models.Rect(0, 0, 400, titleHeight, "red", 0, 0)
    table = models.Table(0, titleHeight + 1, WIDTH - 1, HEIGHT - 1, "black", 255, 0, 3, 10)
    title = models.Text('Liegestuetz', titleRect.getCenter(), "red", titleHeight // 3 * 2, 255)
    for i in range(0, len(setArray)-1):
        sets.append(models.Text(setArray[i], table.getRect(i).getCenter(), "black", (HEIGHT-titleHeight) // 15, 0))

    titleRect.draw()
    title.draw()
    table.drawTable()
    for i in range(0, len(sets)):
        sets[i].draw()

#    width, height = draw_red.textsize('Liegestuetz', font = font)
#    draw_red.text((200 - width // 2, 27 - height // 2 + 6), 'Liegestuetz', font= font, fill = 255)
#    draw_black.rectangle((0, 61, 399, 299), fill = 255, outline = 0)

    # display the frames
    epd.display_frame(epd.get_frame_buffer(models.image_black), epd.get_frame_buffer(models.image_red))

    # display images
    #frame_black = epd.get_frame_buffer(Image.open('black.bmp'))
    #frame_red = epd.get_frame_buffer(Image.open('red.bmp'))
    #epd.display_frame(frame_black, frame_red)

if __name__ == '__main__':
    main()
