import evi 

def main():

    program = evi.EVI()

    program.addFrame("innerclimate", ["both"])
    program.addFrame("weather", ["both", "524901"] )
    program.addFrame("training", ["both", "Big 6"])
    program.addFrame("pushup", ["both"])

    program.start() # start display loop


if __name__ == '__main__':
    main()
