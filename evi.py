import frames
import shapes
import inputhandler
import datetime
from time import sleep
import requests
import click
import json

# Read input for text from file
textfile = open("sets.txt", "r")
setArray = textfile.read().split('\n')
textfile.close()
sets = []


class EVI():
    def __init__(self):
        self.frames = []
        self.__addStartFrame()
        self.__currentFrame = 0
        self.frames[0].display()

        # create owm API call
        owmkey = open("owmkey", "r")
        # weather for testing, use forecast for final
        self.__owmApiCall = ('http://api.openweathermap.org/data/2.5/weather?id=' \
                          + '524901' \
                          + '&APPID=' + owmkey.read()).split()[0]
        #self.__owmApiCall.rsplit('\n')
        owmkey.close()
        print(self.__owmApiCall)

        #self.currentWeather = {"temp" : 20, "wind" : "heavy", "clouds" : "cloudy"}

        #self.innerWeather = None
        #self.innerWeatherLastUpdate = None # necessary? use weatherlu?
        #self.weather = None
        self.weatherLastUpdate = datetime.datetime.now()

        #self.__addInnerWeatherFrame()
        #self.updateInnerWeather()
        self.__addWeatherFrame()
        #self.updateWeather()
        #self.__addTrainingFrame()
        self.__addPushupFrame()

        #self.frames[1].display()

        # inner "weather" frame
        #self.frames.append(innerWeather()) # TODO: sensor

        # outside weather frame
        #self.frames.append(weather())   # city as param?

        # training frame
        #self.frames.append(trainingFrame()) # table with data as param?

    def __addStartFrame(self):
        self.frames.append(frames.Frame("both"))

        frameBackground = shapes.Rect((0,0), (399,299), "black", 0, 0)
        whiteEllipse = shapes.Ellipse((-200, -300),(600,200), 30, 150, "black", 255, 255)
        name = shapes.Text("E-VI", (200, 75), "black", 35, 0)
        mainText = shapes.Text("E-Ink Visualizer of Information", (200, 120), "black", 18, 0)
        usage  = shapes.Text("Usage:      swipe left/right", (200, 230), "black", 16, 255)
        usage2 = shapes.Text("            swipe   up/down", (200,256), "black", 16, 255)
        circle = shapes.Ellipse((300, -100), (500, 100), 0, 180, "red", 0, 0)
        version = shapes.Text(frames.VERSION, (360, 35), "red", 20, 255)

        self.frames[0].addShapes([frameBackground, whiteEllipse, name, mainText, \
                                  usage, usage2, circle, version])

    def __addInnerWeatherFrame(self):
        self.frames.append(frames.Frame("both"))
        # setup graphics

    def updateInnerWeather(self):
        td = datetime.datetime.utcnow() - self.innerWeatherLastUpdate
        if td.seconds < 700:
            self.innerWeatherLastUpdate = datetime.datetime.utcnow()
        else:
            pass

    def __addWeatherFrame(self):
        self.frames.append(frames.Frame("both"))

        #titleHeight = 60
        
        # dictionary of shapes for labeling ?
        #self.frames[-1].addShapes([\
        titleRect = shapes.Rect((0, 0), (frames.WIDTH, frames.HEIGHT // 4), "black", 0, 0)
        sideTable = shapes.Table((0, frames.HEIGHT // 4), (frames.WIDTH // 3, frames.HEIGHT), \
                             "black", 255, 0, 2, 6)
        mainRect = shapes.Rect((frames.WIDTH // 3, frames.HEIGHT // 4), \
                            (frames.WIDTH, (3 * frames.HEIGHT) // 4), "black", 255, 0)
        bottomRect = shapes.Rect((frames.WIDTH // 3, (3 * frames.HEIGHT) // 4), \
                            (frames.WIDTH, frames.HEIGHT), "black", 255, 0)
        city = shapes.Text('City', (200, 25), "black", 25, 255)
        date = shapes.Text('Date: ', (200, 60), "black", 25, 255)
        temp = shapes.Text('Temperature: ', (200, 120), "black", 24, 0)
        #wind = shapes.Text('Wind: ', (130, 230), "black", 20, 0)
        clouds = shapes.Text('Clouds: ', (200, 190), "black", 20, 0)
        weather = shapes.Text('weatherDesc', (200, 160), "black", 20, 0)
        weatherMain = shapes.Picture((frames.WIDTH - 160, frames.HEIGHT // 4), \
                               (frames.WIDTH, frames.HEIGHT // 4 + 160 ), \
                               "black", 0, 0, "10d_black", "10d_red") 
        #                    ])

        sideTable.addShapes([shapes.Text('sunrise', (0,0), "black", 12, 0), \
                           shapes.Text('sunset ', (0,0), "black", 12, 0), \
                           shapes.Text('pressure', (0,0), "black", 12, 0), \
                           shapes.Text('humidity', (0,0), "black", 12, 0), \
                           shapes.Text('wind speed', (0,0), "black", 12, 0), \
                           shapes.Text('wind direction', (0,0), "black", 12, 0), \
                           shapes.Text('sunr', (0,0), "black", 12, 0), \
                           shapes.Text('suns', (0,0), "black", 12, 0), \
                           shapes.Text('press', (0,0), "black", 12, 0), \
                           shapes.Text('humid', (0,0), "black", 12, 0), \
                           shapes.Text('win', (0,0), "black", 12, 0), \
                           shapes.Text('windir', (0,0), "black", 12, 0)])

        sideTable.addBackground("black", 255, 0)

        self.frames[-1].addShapes([titleRect, sideTable, mainRect, bottomRect, city, date, \
                                   temp, clouds, weather, weatherMain])
            
        self.updateWeather()

    def updateWeather(self):
            td = datetime.datetime.utcnow() - self.weatherLastUpdate
        #if td.seconds < 700:
            self.__currentWeather = requests.get(self.__owmApiCall).json()
            print(self.__currentWeather)
            #data = open('data.json', 'r')
            #self.__currentWeather = json.loads(data.read())
            #data.close()

            self.frames[1].getShape(4).setText(self.__currentWeather["name"])
            self.frames[1].getShape(5).setText(datetime.datetime.now().strftime("%d.%m.%Y  week %W"))
            self.frames[1].getShape(6).setText(str(round(\
                    self.__currentWeather["main"]["temp"] - 271.15, 2)) + "oC")
#            self.frames[1].getShape(7).setText(str(self.__currentWeather["wind"]["speed"]))
            self.frames[1].getShape(7).setText('clouds: ' + \
                            str(self.__currentWeather["clouds"]["all"]) + '%')
            self.frames[1].getShape(8).setText(str(self.__currentWeather["weather"][0]["description"]))
            self.frames[1].getShape(9).setImgNames(self.__currentWeather["weather"][0]["icon"]\
                                                    + "_black", \
                                                    self.__currentWeather["weather"][0]["icon"]\
                                                    + "_red")
            #self.frames[1].draw()
            self.frames[1].getShape(1).getEntry(6).setText( \
                    datetime.datetime.utcfromtimestamp(\
                            self.__currentWeather["sys"]["sunrise"]).strftime("%H:%M"))
            self.frames[1].getShape(1).getEntry(7).setText( \
                    datetime.datetime.utcfromtimestamp(\
                            self.__currentWeather["sys"]["sunset"]).strftime("%H:%M"))
            self.frames[1].getShape(1).getEntry(8).setText( \
                    str(self.__currentWeather["main"]["pressure"]))           
            self.frames[1].getShape(1).getEntry(9).setText( \
                    str(self.__currentWeather["main"]["humidity"]))
            self.frames[1].getShape(1).getEntry(10).setText( \
                    str(self.__currentWeather["wind"]["speed"]))
            self.frames[1].getShape(1).getEntry(11).setText( \
                    str(self.__currentWeather["wind"]["deg"]))           
             

            
            self.weatherLastUpdate = datetime.datetime.utcnow()

            if self.__currentFrame == 1:
                self.__refresh()
        #else:
        #    pass

    def __addTrainingFrame(self):
        self.frames.append(frames.Frame("both"))

    def __addPushupFrame(self):
        self.frames.append(frames.Frame("both"))

        titleHeight = 60
        table = shapes.Table((0, titleHeight+1), (frames.WIDTH - 1, frames.HEIGHT - 1), \
                              "black", 255, 0, 3, 10) 

        titleRect = shapes.Rect((0, 0), (frames.WIDTH, titleHeight), "red", 0, 0)
        title = shapes.Text('Liegestuetz', titleRect.getCenter(), "red", \
                            titleHeight // 3 * 2, 255)
        for i in range(0, len(setArray)-1):
            sets.append(shapes.Text(setArray[i], (0,0), "black", \
                                    (frames.HEIGHT - titleHeight) // 15, 0))
            table.addShape(sets[i])

        table.addBackground("black", 255, 0)

        table.invertCells(range(0, 6))
        table.swapCells([5])

    # add shapes to training frame
        self.frames[-1].addShape(titleRect)
        self.frames[-1].addShape(title)
        self.frames[-1].addShape(table)

    def __refresh(self):
        self.frames[self.__currentFrame].display()
        #print("before sleep")
        #sleep(15) # wait until refresh, so display()s won't stack up
        #print("after sleep") # apparently display() blocks already

    def addFrame(self, frame):   # for custom frames
        self.frames.append(frame)

    def start(self):

        loop = True

        #_left = 0
        #_right = 0

        while loop:
            char = click.getchar()
            if char == 'a': #and _left == 0:
                self.__currentFrame = (self.__currentFrame - 1) % len(self.frames)
                self.__refresh()
                #_left = 1
                #_right = 0
            if char == 'd': # and _right == 0:
                self.__currentFrame = (self.__currentFrame + 1) % len(self.frames)
                self.__refresh()
                #_left = 0
                #_right = 1
            if char == 'q':
                loop = False


