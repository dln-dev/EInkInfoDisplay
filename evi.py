import frames
import shapes
#import inputhandler
import datetime
#from time import sleep
import requests
import click
import json # only for testing


class EVI():
    def __init__(self):
        self.frames = []
        self.addFrame("start", ["both"])
        self.__currentFrame = 0
        self.frames[0].display()


    def addFrame(self, frameType, params):
        if frameType in ["start", "Start"]:
            self.frames.append(StartFrame(*params))
        elif frameType in ["weather", "Weather"]:
            self.frames.append(WeatherFrame(*params))
        elif frameType in ["training", "Training"]:
            self.frames.append(TrainingFrame(*params))
        elif frameType in ["pushup", "pushups", "Pushup", "Pushups"]:
            self.frames.append(PushupFrame(*params))
        else:
            raise(ValueError("unrecognized frame type %s", frameType))


    def __refresh(self):
        self.frames[self.__currentFrame].display()


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


class StartFrame(frames.Frame):
    def __init__(self, colors):
        frames.Frame.__init__(self, colors)

        frameBackground = shapes.Rect((0,0), (399,299), "black", 0, 0)
        whiteEllipse = shapes.Ellipse((-200, -300),(600,200), 30, 150, "black", 255, 255)
        name = shapes.Text("E-VI", (200, 75), "black", 35, 0)
        mainText = shapes.Text("E-Ink Visualizer of Information", (200, 120), "black", 18, 0)
        usage  = shapes.Text("Usage:      swipe left/right", (200, 230), "black", 16, 255)
        usage2 = shapes.Text("            swipe   up/down", (200,256), "black", 16, 255)
        circle = shapes.Ellipse((300, -100), (500, 100), 0, 180, "red", 0, 0)
        version = shapes.Text(frames.VERSION, (360, 35), "red", 20, 255)

        self.addShapes([frameBackground, whiteEllipse, name, mainText, \
                                  usage, usage2, circle, version])



class WeatherFrame(frames.Frame):
    def __init__(self, colors, city):
        frames.Frame.__init__(self, colors)

        owmkey = open("owmkey", "r")
        self.__owmApiCall = ('http://api.openweathermap.org/data/2.5/weather?id=' \
                              + city + '&APPID=' + owmkey.read()).split()[0]
        owmkey.close()

        self.weatherLastUpdate = datetime.datetime.now()
       
        titleRect = shapes.Rect((0, 0), (frames.WIDTH, frames.HEIGHT // 4), "black", 0, 0)
        sideTable = shapes.Table((0, frames.HEIGHT // 4), (frames.WIDTH // 3, frames.HEIGHT), \
                             "black", 255, 0, 2, 6)
        mainRect = shapes.Rect((frames.WIDTH // 3, frames.HEIGHT // 4), \
                            (frames.WIDTH, (3 * frames.HEIGHT) // 4), "black", 255, 0)
        bottomRect = shapes.Rect((frames.WIDTH // 3, (3 * frames.HEIGHT) // 4), \
                            (frames.WIDTH, frames.HEIGHT), "black", 255, 0)
        city = shapes.Text('City', (frames.WIDTH // 2, 23), "black", 25, 255)
        date = shapes.Text('Date: ', (frames.WIDTH // 2, 55), "black", 25, 255)
        temp = shapes.Text('Temperature: ', (225, frames.HEIGHT // 4 + 30), "black", 24, 0)
        clouds = shapes.Text('Clouds: ', (200, 200), "black", 20, 0)
        weather = shapes.Text('weatherDesc', (335, 200), "black", 20, 0)
        weatherMain = shapes.Picture((frames.WIDTH - 160, frames.HEIGHT // 4 - 20), \
                               (frames.WIDTH, frames.HEIGHT // 4 + 160 - 20), \
                               "black", 0, 0, "OWM/10d_black", "OWM/10d_red")
        tempSym = shapes.Picture((frames.WIDTH // 3, frames.HEIGHT // 4 + 10), \
                                 (frames.WIDTH // 3 + 50, frames.HEIGHT // 4 + 50 + 10), \
                                 "black", 0, 0, "Icons/temp_black", "Icons/temp_red")
 
        # setup texts, last 6 are placeholders
        sideTable.addShapes([shapes.Picture((0,0), (50,50), "black", 0, 0, \
                             "Icons/sunrise_black", "Icons/sunrise_red"), \
                           shapes.Picture((0, 0), (50, 50), "black", 0, 0, \
                             "Icons/sunset_black", "Icons/sunset_red"), \
                           shapes.Picture((0, 0), (50, 50), "black", 0, 0, \
                             "Icons/pressure_black", "Icons/pressure_red"), \
                           shapes.Picture((0, 0), (50, 50), "black", 0, 0, \
                             "Icons/humidity_black", "Icons/humidity_red"), \
                           shapes.Picture((0, 0), (50, 50), "black", 0, 0, \
                             "Icons/windspeed_black", "Icons/windspeed_red"), \
                           shapes.Picture((0, 0), (50, 50), "black", 0, 0, \
                             "Icons/winddir_black", "Icons/winddir_red"), \
                           shapes.Text('sunr', (0,0), "black", 16, 0), \
                           shapes.Text('suns', (0,0), "black", 16, 0), \
                           shapes.Text('press', (0,0), "black", 16, 0), \
                           shapes.Text('humid', (0,0), "black", 16, 0), \
                           shapes.Text('win', (0,0), "black", 16, 0), \
                           shapes.Text('n/a', (0,0), "black", 16, 0)])

        sideTable.addBackground("black", 255, 255)

        self.addShapes([titleRect, sideTable, mainRect, bottomRect, city, date, \
                                   temp, clouds, weather, weatherMain, tempSym])
            
        self.updateWeather()


    def updateWeather(self):
        td = datetime.datetime.utcnow() - self.weatherLastUpdate

        #if td.seconds < 700:
        #self.__currentWeather = requests.get(self.__owmApiCall).json()
        data = open('data.json', 'r')
        self.__currentWeather = json.loads(data.read())
        data.close()

        self.getShape(4).setText(self.__currentWeather["name"])
        self.getShape(5).setText(datetime.datetime.now().strftime("%d.%m.%Y  week %W"))
        self.getShape(6).setText(str(round(\
                self.__currentWeather["main"]["temp"] - 271.15, 2)) + "oC")
#        self.frames[1].getShape(7).setText(str(self.__currentWeather["wind"]["speed"]))
        self.getShape(7).setText('clouds: ' + \
                        str(self.__currentWeather["clouds"]["all"]) + '%')
        self.getShape(8).setText(str(self.__currentWeather["weather"][0]["description"]))
        self.getShape(9).setImgNames("OWM/" + self.__currentWeather["weather"][0]["icon"]\
                                        + "_black", \
                                     "OWM/" + self.__currentWeather["weather"][0]["icon"]\
                                        + "_red")
        
        self.getShape(1).getEntry(6).setText( \
                datetime.datetime.utcfromtimestamp(\
                self.__currentWeather["sys"]["sunrise"]).strftime("%H:%M"))
        self.getShape(1).getEntry(7).setText( \
                datetime.datetime.utcfromtimestamp(\
                        self.__currentWeather["sys"]["sunset"]).strftime("%H:%M"))
        self.getShape(1).getEntry(8).setText( \
                str(self.__currentWeather["main"]["pressure"]))           
        self.getShape(1).getEntry(9).setText( \
                str(self.__currentWeather["main"]["humidity"]))
        self.getShape(1).getEntry(10).setText( \
                str(self.__currentWeather["wind"]["speed"]))
        #self.frames[1].getShape(1).getEntry(11).setText( \
        #        str(self.__currentWeather["wind"]["deg"]))  # no "deg" in hometown         
             

            
        self.weatherLastUpdate = datetime.datetime.utcnow()

#        if self.__currentFrame == 1:
#        self.__refresh()
        #else:
        #    pass


class InsideClimateFrame(frames.Frame):
    def __init__(self, colors):
        frames.Frame.__init__(self, colors)

        self.addShape(shapes.Text("TBD", (200, 150), "black", 0, 0))


class TrainingFrame(frames.Frame):
    def __init__(self, colors, programName):
        frames.Frame.__init__(self, colors)
        # plan: sqlite db with marking of last performed exercise, then fill 
        # with current tbd exercises for the week, swipe down for done
        self.__programName = programName

        titleRect = shapes.Rect((0, 0), (frames.WIDTH, frames.HEIGHT // 6), "red", 0, 0)
        titleText = shapes.Text("Big 6", titleRect.getCenter(), "red", 24, 255)
        table = shapes.Table((0, frames.HEIGHT // 6), (frames.WIDTH - 1, frames.HEIGHT - 1), \
                             "black", 255, 0, 5, 6)

        table.addShapes([shapes.Picture((0, 0), (50, 50), "black", 0, 0, \
                         "Training/squats_black", "Training/squats_red"), \
                         shapes.Picture((0, 0), (50, 50), "black", 0, 0, \
                         "Training/handstand_black", "Training/handstand_red"), \
                         shapes.Picture((0, 0), (50, 50), "black", 0, 0, \
                         "Training/legraise_black", "Training/legraise_red"), \
                         shapes.Picture((0, 0), (50, 50), "black", 0, 0, \
                         "Training/bridge_black", "Training/bridge_red"), \
                         shapes.Picture((0, 0), (50, 50), "black", 0, 0, \
                         "Training/pushups_black", "Training/pushups_red"), \
                         shapes.Picture((0, 0), (50, 50), "black", 0, 0, \
                         "Training/pullup_black", "Training/pullup_red") \
                        ])

        self.addShapes([titleRect, titleText, table])


class PushupFrame(frames.Frame):
    def __init__(self, colors):
        frames.Frame.__init__(self, colors)

        textfile = open("sets.txt", "r")   # later use sqlite db
        setArray = textfile.read().split('\n')
        textfile.close()
        sets = []

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
        self.addShape(titleRect)
        self.addShape(title)
        self.addShape(table)


