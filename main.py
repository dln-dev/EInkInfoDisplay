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

import shapes
import frames
import evi 
import click

def main():
    # Read input for text from file
    textfile = open("sets.txt", "r")
    setArray = textfile.read().split('\n')
    textfile.close()
    sets = []

    titleHeight = 60

    # Setup frames
#    training = frames.Frame("both")
#    crazyTable = frames.Frame("both")

    # Setup some shapes for training frame
#    table = shapes.Table((0, titleHeight+1), (frames.WIDTH - 1, frames.HEIGHT - 1), \
#                          "black", 255, 0, 3, 10) 
#    titleRect = shapes.Rect((0, 0), (frames.WIDTH, titleHeight), "red", 0, 0)
#    title = shapes.Text('Liegestuetz', titleRect.getCenter(), "red", titleHeight // 3 * 2, 255)
#    for i in range(0, len(setArray)-1):
#        sets.append(shapes.Text(setArray[i], (0,0), "black", (frames.HEIGHT - titleHeight) // 15, 0))
#        table.addShape(sets[i])

#    table.addBackground("black", 255, 0)

#    table.invertCells(range(0, 6))
#    table.swapCells([5])


    # add shapes to training frame
#    training.addShape(titleRect)
#    training.addShape(title)
#    training.addShape(table)

    # Setup some shapes for the second frame
#    cTable = shapes.Table((0,0), (frames.WIDTH-1, frames.HEIGHT-1), "black", 255, 0, 2, 2)
#    cTable.addBackground("black", 255, 0)
#    innerTable = shapes.Table((0,0), (frames.WIDTH/2, frames.HEIGHT/2), "black", 255, 0, 4, 4)
#    innerTable.addBackground("red", 255, 0)
#    cTable.addShape(innerTable)

#    crazyTable.addShape(cTable)
#    #crazyTable.addShape(innerTable)
#    #crazyTable.addShape(cTable)

# transmit frame to display
#    loop = True

#    _left = 0
#    _right = 0

#    while loop:
#        char = click.getchar()
#        if char == 'a' and _left == 0:
#            training.display()
#            _left = 1
#            _right = 0
#        if char == 'd' and _right == 0:
#            crazyTable.display()
#            _left = 0
#            _right = 1
#        if char == 'q':
#            loop = False

    program = evi.EVI()
    

    #training.display()
    #crazyTable.display()

if __name__ == '__main__':
    main()
