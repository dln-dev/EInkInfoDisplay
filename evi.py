import frames
import shapes
import inputhandler
import datetime
import requests

# Read input for text from file
textfile = open("sets.txt", "r")
setArray = textfile.read().split('\n')
textfile.close()
sets = []


class EVI():
    def __init__(self):
        self.frames = []
        self.__addStartFrame()
        self.currentFrame = 0
        self.frames[0].display()

        # create owm API call
        owmkey = open("owmkey", "r")
        self.owmApiCall = 'http://api.openweathermap.org/data/2.5/forecast?id=' \
                          + "524901"\
                          + '&APPID=' + owmkey.read()
        owmkey.close()

        self.currentWeather = {"temp" : 20, "wind" : "heavy", "clouds" : "cloudy"}

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
        self.updateWeather()

        titleHeight = 60

        self.frames[-1].addShapes([\
                shapes.Rect((0, 0), (frames.WIDTH, titleHeight), "black", 0, 0), \
                shapes.Text('Weather', (200, 30), "black", \
                            titleHeight // 3 * 2, 255), \
                shapes.Text('Temperature: ' + str(self.currentWeather["temp"]) + 'OC', \
                            (130, 190), "black", 20, 0), \
                shapes.Text('Wind: ' + self.currentWeather["wind"], \
                            (130, 230), "black", 20, 0), \
                shapes.Text('Clouds: ' + self.currentWeather["clouds"], \
                            (130, 270), "black", 20, 0) \
                            ])


    def updateWeather(self):
        td = datetime.datetime.utcnow() - self.weatherLastUpdate
        if td.seconds < 700:
            # self.weather = requests.get(owmApiCall)
            self.weatherLastUpdate = datetime.datetime.utcnow()
        else:
            pass

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

    def addFrame(self, frame):   # for custom frames
        self.frames.append(frame)

    def start(self):
        pass
        #inputhandler.start()


