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

import newShapes
import frames

def main():
    # Read input for text from file
    textfile = open("sets.txt", "r")
    setArray = textfile.read().split('\n')
    textfile.close()
    sets = []

    titleHeight = 60

    # Setup frames
    training = frames.Frame("both")
    table = newShapes.Table((0, titleHeight), (399, 299), "black", 255, 0, 3, 10)
    rectTable = newShapes.Table((0, titleHeight), (399, 299), "black", 255, 0, 3, 10)

    rectTable.fillRects(255,0)

    # Setup some shapes
    titleRect = newShapes.Rect((0, 0), (400, titleHeight), "red", 0, 0)
    #table = shapes.Table(0, titleHeight + 1, frames.WIDTH - 1, frames.HEIGHT - 1, "black", 255, 0, 3, 10)
    title = newShapes.Text('Liegestuetz', titleRect.getCenter(), "red", titleHeight // 3 * 2, 255)
    for i in range(0, len(setArray)-1):
        #sets.append(newShapes.Text(setArray[i], table.getRect(i).getCenter(), "black", (frames.HEIGHT-titleHeight) // 15, 0))
        sets.append(newShapes.Text(setArray[i], (0,0), "black", (frames.HEIGHT - titleHeight) // 15, 0))
        table.addShape(sets[i])
#        training.addShape(shapes.Text(setArray[i], table.getRect(i).getCenter(), "black", (frames.HEIGHT-titleHeight) // 15, 0))


    #for i in range(0,5):
    #    table.getRect(i).setFill(0)
    #    sets[i].setFill(255)

    #table.getRect(5).setColor("red")
    #table.getRect(5).setFill(0)
    #sets[5].setColor("red")
    #sets[5].setFill(255)

    # add shapes to training frame
    training.addShape(titleRect)
    training.addShape(title)
    training.addShape(rectTable)
    training.addShape(table)
    # transmit frame to display
    training.display()

if __name__ == '__main__':
    main()
