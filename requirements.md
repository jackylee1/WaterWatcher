
<head><link href="oft_spec.css" rel="stylesheet"></link></head>

System Requirement Specification Watcher Watcher 

# Introduction

Watcehr Watcher is a slef-made smarthome sokution to prevent the smart house from being flooded and trasformed into a wet house. 

## Goals

The goals are 

  * Reliable & safe - You want it to protect your house, right?
  * Secure - No one else should know your water consumption of no-at-hoem times.
  * Effective - In case of a broken pipe an alarm-eMail won't do the job. 
  * Fun - Therefore this project will serve as my private software engineering learning dojo.  

## Terms and Abbreviations

The following list gives you an overview of terms and abbreviations commonly used in OFT documents.

  * AWS: Amazon Web Services 
  * OFT - Open Fast Trace - A requirement tracing tool which professionally traces (in all documents of a project) if requirements are done. "aka covered". Se more here:   
  * WW - WaterWatcher - This project 
  Because this project wants to try out the requirement tracing toolikt by the team of https://github.com/itsallcode/openfasttrace you we'll find engineering documents that follow the features requirements and tests of this solution throughout this repository. If I succeed in doing so. 
  
  
  

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

## Anmaly detection 
`feat~anomalyt~detection~1

WW shall notice anomalies in the water consumption. At the very latest a sudden raise in consumption based on a broken pipe and a small continous leak shall be detected.

Rationale:
Manual setting bounaries may work but a system that can learn from the normal consumption and then derive intelligence for a deviation should prove more user friendly. 

Needs: req

## Security 
'feat-security~1

WW shall be build with security and privacy in mind. 


LÖist to be worked in here: 
- Awareness of working modes
- Local Watchdog
- CLoud based heartbeat 
- Backup 
- Valve self-test once a month with report 
- Calculate statistics values (consumption per month) 
- Integarte additrional sensors (someone in th house, ...) 
- Notification challes (local and clodu based) 
- Reliability configured system 
