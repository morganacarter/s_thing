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

#Fake WMATA JSON info for demo purposes

sample_metro_delays = {
"Incidents": [
{
"DateUpdated": "2010-07-29T14:21:28",
"DelaySeverity": "null",
"Description": "Red Line: Expect residual delays to Glenmont due to an earlier signal problem outside Forest Glen.",
"EmergencyText": "null",
"EndLocationFullName": "null",
"IncidentID": "3754F8B2-A0A6-494E-A4B5-82C9E72DFA74",
"IncidentType": "Delay",
"LinesAffected": "RD;",
"PassengerDelay": "0",
"StartLocationFullName": "null"
},
{
"DateUpdated": "2010-07-29T14:21:28",
"DelaySeverity": "null",
"Description": "Train Door Malfunction",
"EmergencyText": "null",
"EndLocationFullName": "null",
"IncidentID": "3754F8B2-A0A6-494E-A4B5-82C9E72DFA74",
"IncidentType": "Delay",
"LinesAffected": "SV;RD;",
"PassengerDelay": "0",
"StartLocationFullName": "null"
}
]
}

sample_opm_delays={"Id":642,"Title":"Federal Government Operating Status in the Washington, DC, Area","Location":"Washington, DC area","StatusSummary":"Open - 2 hours Delayed Arrival - With Option for Unscheduled Leave or Unscheduled Telework","StatusWebPage":"http://www.opm.gov/policy-data-oversight/snow-dismissal-procedures/current-status/","ShortStatusMessage":"Federal agencies in the Washington, DC area are OPEN under 2 hours DELAYED ARRIVAL and employees have the OPTION FOR UNSCHEDULED LEAVE OR UNSCHEDULED TELEWORK. Employees should plan to arrive for work no more than 2 hours later than they would be expected to arrive.","LongStatusMessage":"Federal agencies in the Washington, DC area are OPEN under 2 hours DELAYED ARRIVAL and employees have the OPTION FOR UNSCHEDULED LEAVE OR UNSCHEDULED TELEWORK. Employees should plan to arrive for work no more than 2 hours later than they would be expected to arrive.\r\n \r\nNon-Emergency Employees who report to the office will be granted excused absence (administrative leave) for up to 2 hours past their expected arrival time. In accordance with their agency\u0027s policies and procedures, subject to any applicable collective bargaining requirements (as consistent with law), non-emergency employees may notify their supervisor of their intent to use:\r\n\r\nearned annual leave, compensatory time off, credit hours, or sick leave, as appropriate;\r\nleave without pay;\r\ntheir alternative work schedule (AWS) day off or rearrange their work hours under flexible work schedules; or\r\nunscheduled telework (if telework-ready).\r\n\r\n\r\n(Employees who request unscheduled leave should be charged leave for the entire workday.)\r\n\r\nTelework-Ready Employees who are regularly scheduled to perform telework or who notify their supervisor of their intention to perform unscheduled telework must be prepared to telework for the entire workday, or take unscheduled leave, or a combination of both, for the entire workday in accordance with their agency\u0027s policies and procedures, subject to any applicable collective bargaining requirements (as consistent with law).\r\n\r\nPre-approved Leave. Employees on pre-approved leave for the entire workday or employees who requested unscheduled leave for the entire workday should be charged leave for the entire day.\r\n\r\nEmergency Employees are expected to report to their worksite on time unless otherwise directed by their agencies.","ExtendedInformation":" \r\nNon-Emergency Employees who report to the office will be granted excused absence (administrative leave) for up to 2 hours past their expected arrival time. In accordance with their agency\u0027s policies and procedures, subject to any applicable collective bargaining requirements (as consistent with law), non-emergency employees may notify their supervisor of their intent to use:\r\n\r\nearned annual leave, compensatory time off, credit hours, or sick leave, as appropriate;\r\nleave without pay;\r\ntheir alternative work schedule (AWS) day off or rearrange their work hours under flexible work schedules; or\r\nunscheduled telework (if telework-ready).\r\n\r\n\r\n(Employees who request unscheduled leave should be charged leave for the entire workday.)\r\n\r\nTelework-Ready Employees who are regularly scheduled to perform telework or who notify their supervisor of their intention to perform unscheduled telework must be prepared to telework for the entire workday, or take unscheduled leave, or a combination of both, for the entire workday in accordance with their agency\u0027s policies and procedures, subject to any applicable collective bargaining requirements (as consistent with law).\r\n\r\nPre-approved Leave. Employees on pre-approved leave for the entire workday or employees who requested unscheduled leave for the entire workday should be charged leave for the entire day.\r\n\r\nEmergency Employees are expected to report to their worksite on time unless otherwise directed by their agencies.","DateStatusPosted":"\/Date(1422347400000)\/","CurrentDate":"\/Date(1422347838546)\/","DateStatusComplete":"null","AppliesTo":"January 27, 2015","Icon":"Alert","StatusType":"Open - X hour(s) Delayed Arrival - With Option for Unscheduled Leave or Unscheduled Telework","StatusTypeGuid":"86cc1e55-aa95-4599-b3bb-1a001b58f861","Url":"http://www.opm.gov/policy-data-oversight/snow-dismissal-procedures/current-status/"}

sample_weather_delays={u'clouds': {u'all': 88}, u'name': u'Washington', u'snow': {u'3h': 0}, u'coord': {u'lat': 38.89, u'lon': -77.03}, u'sys': {u'country': u'United States of America', u'sunset': 1422483905, u'message': 0.1009, u'type': 3, u'id': 129340, u'sunrise': 1422447432}, u'weather': [{u'main': u'Clouds', u'id': 804, u'icon': u'04n', u'description': u'overcast clouds'}], u'cod': 200, u'base': u'cmc stations', u'dt': 1422403655, u'main': {u'pressure': 1013.8, u'temp_min': 29.84, u'temp_max': 31.1, u'temp': 30.43, u'humidity': 75}, u'id': 4140963, u'wind': {u'speed': 10.39, u'deg': 328.002}}

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
