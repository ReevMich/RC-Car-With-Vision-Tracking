#MANIFEST
-------

Contains a list of each file and its purpose

*   **.gitignore**: 
      extensions of files that are not including in staging or commits
*   ***/Arduino/***: 
      contains all the adruino programs
	* **License Plate.ino**: 
	    The license plate random generator for the 16x2 LCD Display  
* 	***/RaspberryPi/***: 
      contains all the raspberry-pi programs
	* **BallTracker.py**: 
	  ???
	* **BallTrackerHue.py**: 
	  ???
	* **DS4_Controller.py**: 
    PS4 Controller thread that controls the motors and sends messages through pipes in python
	* **Distance_Sensor.py**: 
	  Distance Sensor Module that detects how far the car is from an object the sensor detects
	* **Wheel_Control.py**: 
	  ???
	* **cfirmata.c**:
	  ???
	* ***/DS4Controller/***:
	  Contains all the DS4 module files, thats used in "C" wrapping
	  * **__init__.py**
	  * ***/src/***:
	    All the DS4 Controller source files.
      * **DS4.c**
      * **DS4.h**
      * **DS4.i**
      * **controller.py**
      * **init.sh**
      * **setup.py**
      * **test.py**
