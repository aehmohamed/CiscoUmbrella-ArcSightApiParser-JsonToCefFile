import os
import sys
import json
import time
import datetime
import requests
from requests.auth import HTTPBasicAuth
##########################################

#API Call
url="https://reports.api.umbrella.com/v1/organizations/YYYY/security-activity"      #Replace YYYY with your Cisco Umbrella unique Organization ID, you can get it from Cisco Support.
requests.packages.urllib3.disable_warnings()                                        #To disable SSL Warnings, otherwise you will need to have the certificate trusted.


time_tuple1 = time.strptime(str(datetime.datetime.now()), '%Y-%m-%d %H:%M:%S.%f')   #Define current time as tuple
time_epoch1 = int(time.mktime(time_tuple1))-900                                     #Define current time - 15 minutes as integer epoch time_epoch1
time_epoch2 = int(time.mktime(time_tuple1))                                         #Define current time as integer time_epoch2
time_epoch1Str = str(time_epoch1)                                                   #Convert time_epoch1 to string to pass the string as an argument to the API call
time_epoch2Str = str(time_epoch2)                                                   #Convert time_epoch2 to string to pass the string as an argument to the API call


print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time_epoch1)))              #Print time_epoch1 in a readable format, just for verification
print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time_epoch2)))              #Print time_epoch2 in a readable format, just for verification

parameters={'start':time_epoch1Str,'stop':time_epoch2Str
    ,'limit':'500'
         }                                                                          #API Call parameters : Get all logs from the last 15 mins with a max. of 500 logs, Cisco Umbrella API will show only the blocked logs



response = requests.request(url=url,
                            method='GET'
                            ,auth=HTTPBasicAuth('ApiKey','ApiSecret')               #Replace ApiKey and ApiSecret with the un-encoded Cisco Umbrella API Key and Secret generated from the Web UI for Umbrella reporting), in case of encoding then use header='"Authorization":"Basic ZZZZ"' where ZZZZ is encBase64(key:secret)
                            ,params=parameters                                      #Pass the parameters list (time, time-15 mins, max row results=500)
                            ,verify=False                                           #Disable SSL Verification (you can enable it if you want to)
                            ,timeout=120)                                           #Timeout for the API call to be 120 seconds, just in case it took too long

#API Response
print("Request URL=",response.status_code)                                          #Display the HTTP Reply Code received as a response, just for verification, it should be 2xx
print("Response Code=",response.url)                                                #Display the API Call Response, For verification.


#Parser
cef=[]                                                                              #Define a list for all logs rows, each entry in the list corresponds to a log row

## Mapping JSON Response to CEF
'''
CEF Version                     =   0
Device Vendor                   =   'CISCO'
Device Product                  =   'Umbrella'
Device Version                  =   1
Device Event Class Id           =   originId
Name                            =   actionTaken
Severity                        =   3
Device Host                     =   'umbrella.com'
Destination Host                =   destination
Source Address                  =   internalIp
Source Translated Address       =   externalIp
Device Custom String 1 Label    =   'Categories'
Device Custom String 1          =   categories
Device Custom String 2 Label    =   'Tags'
Device Custom String 2          =   Tags
Device Action                   =   actionTaken
End Time                        =   datetime
'''

try:
    response.json().get('requests')                                                 #When the server replies with JSON Logs, execute the below code
    for log in response.json().get('requests'):                                     #For each JSON log row, map its fields to a corresponding CEF field
        cef.append('CEF:0|CISCO|Umbrella|1|'+str(log.get("originId"))+'|'+log.get("actionTaken")+'|'+'3| '+'dvchost='+'umbrella.com'
                   +' dhost='+log.get("destination")
                   +' src='+log.get("internalIp")
                   +' sourceTranslatedAddress='+log.get("externalIp")
                   +' cs1Label='+'Categories'
                   +' cs1=' + str(log.get("categories"))
                   +' cs2Label=' + 'Tags'
                   +' cs2=' + str(log.get("Tags"))
                   +' act=' +  log.get("actionTaken")
                   +' end=' +  str(1000*int(time.mktime(time.strptime(log.get("datetime"), '%Y-%m-%dT%H:%M:%S.%fZ'))))
                   )

    print("Length=",len(cef))                                                       #Print the number of logs received, for verification.
    print("Sample Log Entry=",cef[0])                                               #Print the first log received as CEF, for verification.

#Write CEF logs to a CEF file name "ciscoUmbrella<timestamp>.cef"

    filename='ciscoUmbrella'+time.strftime("%Y%m%d-%H%M%S")+'.cef'              #Define File names formats, these files can be deleted after processing by this same script Or ArcSight Smart Connector File Processing Options, but I left them in this version for reference.
    filepath='C:\\ArcSight_Connectors\\CiscoUmbrella\\logs\\'+filename          #Define File Path

    fileURLsProcessed_write = open(filepath, "a+", encoding="utf-8")
    for entry in cef:
        fileURLsProcessed_write.write(entry + "\n")                             #For each log row, write it to the file and then add new line to switch to next line.
    fileURLsProcessed_write.close()

except TypeError:                                                               #In case the API returns HTTP code (meaning wrong API call), print "No Logs" and exit
    print("No Logs")