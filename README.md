# Powerline Datalog Pre-processor

This is an exerise in object oriented design using Python.  

Lines from a datalog of timestamps and electrical powerline measurements will be read and put through a moving average filter, and output to a different file.  

Input lines appear as:
  ```
  T, kW, V, I
  ```
Timestamp T is an ISO 8601 formatted timestamp


  ```
2018-01-08 14:54:42.630, 441.781, 477.470, 925.254, , ,
2018-01-08 14:54:43.784, 320.249, 475.942, 672.873, , ,
2018-01-08 14:54:44.900, 435.929, 482.613, 903.268, , ,
2018-01-08 14:54:46.010, 357.977, 475.937, 752.151, , ,
2018-01-08 14:54:47.189, 461.782, 483.066, 955.939, 403.544, <remaining values>
...
<time>, <kW>, <V>, <I>, <kW-avg>, <V-avg>, <I-avg>
* Anomaly - time gap detected
<time>, <kW>, <V>, <I>, , ,
  ```

# Requirements
* Python 3.6+

# Design
An abstract class DatalogLoader provides a .get() method that will return one line of telemetry.  DatalogFileLoader will be implemented to solve the problem, and DatalogMemoryLoader will be used for testing.
![DatalogLoader](doc/DataLogClasses.png)



# Running

# Testing