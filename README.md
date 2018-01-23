# WaterWatcher
Water monitoring for Raspbery PI 

This project aims to create a smart home water monitoring solution running on a raspbery PI.

The overall system consists of a 
1) the RasPi for monitoring and learning the water consumption. 
2) Monitoring software running of the RasPI to store the consumption locally 
3) A reed contact water clock for getting the current consumption (impulse per litre) 
4) A valve to turn off the water if the monitoring senses unusual conditions
5) Optional a direct water sensor to install in the basement to immediately close the valve in case of flooding 
6) Optional movement sensor to detect if someone was present at home to correlate the water consumption with e.g. holiday times.


An MQTT connection to Amazon AWS IoT Service shall to publish the consumptions values for storage and analytics in an InfulxDB.

