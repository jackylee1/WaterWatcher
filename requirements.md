
<head><link href="oft_spec.css" rel="stylesheet"></link></head>

System Requirement Specification for WatcherWatcher 

# Introduction
WaterWatcher is a self-made smarthome solution to prevent the smart house from becoming a flooded house due to an unnoticed broken pipe. 

## Goals
The goals are: 
  * Reliable & safe - You want it to protect your house, right?
  * Secure - No one else should know your water consumption or none-at-home times.
  * Effective - In case of a broken pipe an alarm-eMail won't do the job. It shall close the main water supply. 
  * Fun - Therefore this project will serve as my private software engineering learning dojo.

## Environment 
Part of this solution will run on a raspberry Pi connected to 
* a water clock with a reed sensor and 
* a valve, installed in the main water supply pipe. 
* The internet via WiFi 
The water clock and the valve are both real HW installed by a professional plumber - so you need to calculate ~300€ costs for this.  

## Terms and Abbreviations
The following list gives you an overview of terms and abbreviations commonly used in WW documents.
  * AWS: Amazon Web Services 
  * OFT - Open Fast Trace - A requirement tracing tool which professionally traces (in all documents of a project) if requirements are done. "aka covered". See more here:   
  * WW - WaterWatcher - This project 
  Because this project wants to try out the requirement tracing toolikt by the team of https://github.com/itsallcode/openfasttrace you we'll find engineering documents that follow the features requirements and tests of this solution throughout this repository - if I succeed in doing so. 
  
   

# Features

## Water Sensor 
`feat~requirement-sense~1`

WW shall note each litre of water being consumed at all times. 

Needs: req

## Consumption publication  
`feat~markdown-publish~1`

WW shall publish the water consumption to a cloud service for monitoring and alarming. 

Needs: req

## Cloud Dashbaord 
`feat~cloud~dashboard~1`

WW shall provide a convineint cloud dashbaord shing the consumption in various periods.  

Rationale:

See what is going on...

Needs: req

## Anomaly detection 
`feat~anomaly~detection~1`
WW shall notice anomalies in the water consumption. A sudden extreme increase in consumption based on a broken pipe and a small continous leak shall be detected at the very basic function. 

Needs: req

## Security 
'feat-security~1

WW shall be build with security and privacy in mind. 


## Draft
List of items to be worked in here: 
- Awareness of working modes
- Local HW watchdog
- Cloud based heartbeat 
- Backup 
- Valve self-test once a month with report 
- Calculate statistics values (consumption per month) 
- Integarte additrional sensors (someone in th house, ...) 
- Notification challes (local and clodu based) 
- Reliability configured system for 24/7 operation
- Automatically active after hard reboot and power outtake 
- 


