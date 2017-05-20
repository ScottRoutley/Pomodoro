import time

from Adafruit_LED_Backpack import SevenSegment
import RPi.GPIO as GPIO  

# Create display instance on default I2C address (0x70) and bus number.
display = SevenSegment.SevenSegment()

# Alternatively, create a display with a specific I2C address and/or bus.
# display = SevenSegment.SevenSegment(address=0x74, busnum=1)

# Initialize the display. Must be called once before using the display.
display.begin()

# Keep track of the colon being turned on or off.
colon = True

pomodoroMode = True
timerRunning = False
threeSecondCheck = 0
twentyFiveMinutes = 0
GPIO.setmode(GPIO.BCM)
GPIO.setup(17,GPIO.IN,pull_up_down=GPIO.PUD_UP)

# # Yellow lights
# GPIO.setup(16,GPIO.OUT)

# # Buzzer buzzer
# GPIO.setup(26,GPIO.OUT)


def setup():
    print("in setup")
    global twentyFiveMinutes
    # twentyFiveMinutes = 1500
    twentyFiveMinutes = 10

def checkForButton():
    if (GPIO.input(17) == False):
        return True

def sleepAndLookForClick():
    clickCount = 0

    for i in range(0,10):
        if (checkForButton()):
            clickCount += 1
            print ('button pushed ' + str(clickCount))
        # else:
        #     count = 0
        time.sleep(.1)
        print('sleep' + str(i))
 
    return clickCount


def finishedPomodoro():

    pomodoroMode = False

    for i in range(0,5):
        GPIO.output(26, GPIO.HIGH)
        GPIO.output(16, GPIO.HIGH)
        display.clear()
        display.write_display()

        time.sleep(.4)
        GPIO.output(26, GPIO.LOW)
        GPIO.output(16, GPIO.LOW)
        display.print_float(8888)
        display.write_display()
        time.sleep(.4)

    global twentyFiveMinutes

    twentyFiveMinutes = 180

# Run through different number printing examples.
print('Press Ctrl-C to quit.')

setup()

buttonWasPressed = False

while True:
    m, s = divmod(twentyFiveMinutes, 60)

    currentTime = float(m) + (s / 100.00)
    # Clear the display buffer.
    display.clear()
    # Print a floating point number to the display.
    display.print_float(currentTime)
    # Set the colon on or off (True/False).
    display.set_colon(colon)
    # Write the display buffer to the hardware.  This must be called to
    # update the actual display LEDs.
    display.write_display()
    # Delay for a second.
    # time.sleep(1)
    resultOfClick = sleepAndLookForClick()

    if (resultOfClick > 0):
        if (buttonWasPressed == False):
            timerRunning = not timerRunning
        buttonWasPressed = True
    else:
        threeSecondCheck = 0
        buttonWasPressed = False

    if (resultOfClick > 0):
        threeSecondCheck += resultOfClick

        print ("addtion of " + str(threeSecondCheck))

        if (threeSecondCheck > 30):
            print("reset the timer")
            timerRunning = False
            setup()
    

    if timerRunning:
        twentyFiveMinutes -=1
        if (pomodoroMode):
             GPIO.output(16,GPIO.HIGH)
    else:
        GPIO.output(16,GPIO.LOW)


    if (twentyFiveMinutes == 0) and (timerRunning) and (pomodoroMode):
        finishedPomodoro()
    elif (twentyFiveMinutes == 0) and (pomodoroMode == False) and (timerRunning):
        setup()
        timerRunning = False


    # Print the same numbers with 1 digit precision.

GPIO.cleanup()   
