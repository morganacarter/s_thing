"""Working alarm clock python script.  To test this on the first run, I suggest setting alarm_HH and alarm_MM to whatever your computer clock is displaying at time of run - that way, the alarm will automatically go off. For the second run, set the alarm to go off one minute from computer display. """

import time
import os
#from non import nonBlockingRawInput

name = raw_input("Enter your name.")

print("Hello, " + name)

alarm_HH = raw_input("Enter the hour you want to wake up at") #military time. enter number 0-23
alarm_MM = raw_input("Enter the minute you want to wake up at") #military time. enter number 0-60. 
#will combine alarm_HH with alarm_MM. For example: 21:05

print("You want to wake up at " + alarm_HH + ":" + alarm_MM)

while True:
    now = time.localtime()
    print now
    if now.tm_hour == int(alarm_HH) and now.tm_min == int(alarm_MM):
        print("ALARM NOW!")
        os.popen("samplesong.mp3") #place an mp3 file into your python directory. Rename the file samplesong in order for this to open as your alarm
        break

    else:
        print("no alarm")
    timeout = 60 - now.tm_sec
    
