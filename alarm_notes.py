import time
import os
import requests
from datetime import datetime, timedelta

#Sets up alarm using user inputs
name = raw_input("Enter your name.")

print("Hello, " + name)

alarm_HH = raw_input("Enter the hour you want to wake up at")
alarm_MM = raw_input("Enter the minute you want to wake up at")
alarm_time = "{0}:{1}".format(alarm_HH, alarm_MM)

#converts raw input into datetime format
time_obj = datetime.strptime(alarm_time, '%H:%M')
print time_obj

#JSON requests for WMATA, OPM and Weather. WMATA uses guest api key.

sample_metro_delays = requests.get("https://api.wmata.com/Incidents.svc/json/Incidents?api_key=kfgpmgvfgacx98de9q3xazww").json()

sample_opm_delays=requests.get("http://www.opm.gov/json/operatingstatus.json").json()

sample_weather_delays=requests.get("http://api.openweathermap.org/data/2.5/weather?q=Washington,DC&units=imperial&cnt=7").json()

#establishes how much we'll adjust the time if there is a delay. In our final script, this will be in the 'if there is a delay'...
"""return the value of dictionary dic given the key"""
def find_value(dic, key):
    return dic[key]

delay_minutes =0
for Incidents in sample_metro_delays:
    for IncidentType in sample_metro_delays["Incidents"]:
        if find_value(IncidentType, "IncidentType") == "Delay" and find_value(IncidentType, "LinesAffected").find("SV"):
            delay_minutes +=1
if find_value(sample_opm_delays,"StatusSummary").find("Delayed Arrival"):
    delay_minutes -=4
if sample_weather_delays['weather'][0]['main'] == "Snow":
    delay_minutes +=5
   
            
change_in_time = timedelta(minutes=delay_minutes)

#creates the new time the person wants to wake up
new_time = time_obj - change_in_time


print "You want to wake up at {0}".format(new_time.time())

while True:
    now = time.localtime()
    if now.tm_hour == int(new_time.hour) and now.tm_min == int(new_time.minute):
        print("ALARM NOW!")
        os.popen("samplesong.mp3")
        break

    # else:
    #     print("no alarm")
    timeout = 300 - now.tm_sec
    
