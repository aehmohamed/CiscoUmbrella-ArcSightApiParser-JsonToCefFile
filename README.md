# CiscoUmbrella-ApiParser-JsonToCefFile
 Sample Parser for Cisco Umbrella Cloud Logs - JSON to CEF File - Usable with ArcSight CEF File/Folder Follower Smart Connectors

## _A)Description_

1- Sample Parser for Cisco Umbrella Cloud API Logs - JSON to CEF File - Usable with ArcSight CEF Folder Follower Smart Connectors

2- Intended as an alternative for using Amazon AWS standard connector because of one customer policy, it was built as PoC prone to improvements and was deployed to production successfully after testing, so test before you deploy.


## _B) Requirements_

1- In order to use the script you will need to get some details from Cisco Support (Organization Id, enable and keep both Reports Api Key and Reports Api Secret) and insert your preferred folder location and/or file name format.


## _C) Notes_
 
 1- The script is built to parse Cisco Umbrella logs from the web cloud and map the output JSON into CEF format then deliver it to ArcSight as a CEF file (Not CEF Syslog for this version)
 
 2- The script takes several values, and constrcuts an API call to fetch all logs between the current moment and the last 15 mins, with a limit of 500 logs per call, so this script should be scheduled using Unix Cron or Windows Task Scheduler every 15 mins.
 
 3- Cisco API displays only the "Blocked" logs, if you need the "Allowed" logs then you will have to use the default supported ArcSight AWS Cloud Connector and fill in the region and AWS connection details.
 
 4- CEF logs resultant from this script will accumulate, so you will need to configure ArcSight Folder Follower Post-Processing option to "DeleteFile" in case you need to 


## _D) Known Limitations/Issues_


1- Cisco API result events have no unique ID, so there is a slight chance of duplicating few logs if they have the same exact timestamp to the second (there are no milliseconds in the timestamp either).

2- No Error Handling in case of non-successful JSON responses, the exception handler will be invoked in case of non-JSON (HTML) responses.

3- One Empty log may appear due to the usage of "/n" as a line terminator, depending on the behavior of ArcSight SmartConnectors.

4- The built-in limit for the replies specified by Cisco are 500 events per call, so there is a chance of some missing events.

5- Some python libraries are imported but not used in this published version like "sys".

6- CEF Mapping is done based on a specific use case, you may need to change the CEF mapping per your corporate correlation rules design and flow.
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

7- There is an ArcSight integration command version based on this parser but I did not publish it yet.

8- The API Key and Secret are one-time generated from Cisco Umbrella UI, so they will be visible on the file, while you cannot use them to login but this is a clear audit violation for almost any standard, alternatively you can convert the script to an executable and use encryption via keyrings libraries or at least obfuscation via encoding libraries plus your existing enterprise DLP/File Control Policies.

9- Categories values can be parsed into a list and passed to ArcSight as a CSV without the brackets strings to align it with ArcSight List-type variables and functions.

## _E) References_

1- https://community.microfocus.com/t5/ArcSight-Connectors/ArcSight-Common-Event-Format-CEF-Implementation-Standard/ta-p/1645557?attachment-id=68077

2- https://docs.umbrella.com/umbrella-api/docs/about-the-umbrella-api
