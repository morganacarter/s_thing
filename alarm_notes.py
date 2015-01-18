import time
import os
#from non import nonBlockingRawInput

name = raw_input("Enter your name.")

print("Hello, " + name)

alarm_HH = raw_input("Enter the hour you want to wake up at")
alarm_MM = raw_input("Enter the minute you want to wake up at")

print("You want to wake up at " + alarm_HH + ":" + alarm_MM)

while True:
    now = time.localtime()
    print now
    if now.tm_hour == int(alarm_HH) and now.tm_min == int(alarm_MM):
        print("ALARM NOW!")
        os.popen("samplesong.mp3")
        break

    else:
        print("no alarm")
    timeout = 60 - now.tm_sec
    
