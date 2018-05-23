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

## DatalogLoader
An abstract class DatalogLoader provides a .get() method that will return one line of telemetry.  DatalogFileLoader will be implemented to solve the problem, and DatalogMemoryLoader will be used for testing.

This architecture lets us handle telemetry streams that are possibly too big to fit in memory, or that are streaming, i.e. streamed one measurement at a time over a connection of some sort.

![DatalogLoader](doc/DataLogClasses.png)

* get():
Returns one line of telemetry as a string.  If this won't be possible, i.e. there are no more lines in an input file or a socket is closed, return None.

## DataProcessor

* run():
Calls the callback that gets a line of telemetry and processes it in an output line, which is then sent to the write function callback.  Continues until get() has a problem.

# Running

```shell
python Process_Powerline_File.py inputdata.dat outputfile.dat
```

# Testing

From the project directory, run:
```
python -m unittest discover pyPowerLine/test
```

The dataloader will be tested to 

## PowerlineDataProcessor

The PowerlineDataProcessor will use object mocking to make sure it calls an input function and an output function.

Parsing will be tested with unittests