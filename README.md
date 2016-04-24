
#RC Car with Vision Tracking [![Awesome](https://cdn.rawgit.com/sindresorhus/awesome/d7305f38d29fed78fa85652e3a63e154dd8e8829/media/badge.svg)](https://github.com/sindresorhus/awesome)
----
The RC Car with Vision Tracking is a custom built RC Car with a raspberry pi as the main computer.
This car uses an arduino and H-drive to control the motor and what speed they run at.
The way the RC car with Vision Tracking moves is by utilizing  a camera to track a ball of a predetermined color.
As a secondary control system we have a bluetooth Playstation 4 control for manual control.

* GitHub: https://github.com/du-linux/Team1/

##Features
========

- Control Remote Control Car with Playstation 4 Controller -- Wired/Wirelessly **Bluetooth** 
- Remote Control Car tracks and follows a colored ball
- Randomized License Plate -- (**using Arduino**)
- Reverse Support with the Playstation 4 Controller.
- Object avoidance, (**using Ultra Sonic Sensors**), with automatic reverse
- Features a (**Dual H-Bridge Stepper Motor**) that controls all four motors/wheels
- Controlling all 4-wheels with python dirrectly to GPIO


========
</br>

###Dependencies



####Vision Tracking
==================
Install SimpleCV. This was the method we used even though there are many ways to install SimpleCV:

    sudo apt-get install ipython python-opencv python-scipy python-numpy python-setuptools python-pip
    sudo pip install svgwrite
    sudo pip install https://github.com/sightmachine/SimpleCV/zipball/master

More documentation on SimpleCV at (http://simplecv.org)

- Simple CV uses Python so you can run it either on iPython to test out the camera or run a .py file
- Importing SimpleCV allows you to grab the Image from the Camera
- This allows to have the image to keep refreshing

``` python
    import SimpleCV
    
    cam = SimpleCV.Camera()
    while True:
        img = cam.getImage()
```

Using colorDistance to dilate the image allows it to search for one color. We used ORANGE to find our blue ball. 
Segmenting the image makes it easier to only see the colored object to be able to find the "blobs"

``` python
    dist = img.colorDistance(SimpleCV.Color.ORANGE).dilate(2)
    segmented = dist.stretch(200,255)
    blobs = segmented.findBlobs()
```

The filter function for the blobs creates the circle around the ball. With the circle object, we can grab the x and y coordinates which we use for our wheel power logic.

    

####DS4DRV
==========
- [Python](http://python.org/)_ 2.7 or 3.3+ (for Debian/Ubuntu you need to
  install the *python2.7-dev* or *python3.3-dev* package)
- [python-setuptools](https://pythonhosted.org/setuptools/)
- hcitool (usually available in the *bluez-utils* or equivalent package)

These packages will normally be installed automatically by the setup script,
but you may want to use your distro's packages if available:

- [pyudev](http://pyudev.readthedocs.org/) 0.16 or higher
- [python-evdev](http://pythonhosted.org/evdev/) 0.3.0 or higher
<br/>

Installing the latest release is simple by using [pip](http://www.pip-installer.org/):

    sudo pip install ds4drv
    sudo pip install evdev==0.5.0

Installing a recent version of bluez **Required for Bluetooth**    

    cd ~
    wget http://www.kernel.org/pub/linux/bluetooth/bluez-5.37.tar.xz
    tar xvf bluez-5.37.tar.xz

Installing SWIG - The C code Wrapper to Python ***Required to wrapping C code to Python***
  
    sudo apt-get install swig

#####Distance Sensor
- Importing RPi.GPIO allows for use of the gpio pins on the Raspberry Pi
- Importing time allows for calculating time between triger and echo.

``` python
    import RPi.GPIO as GPIO
    import time
```

#####Using DS4
---------

Unless your system is using BlueZ 5.14 (which was released recently) or higher
it is not possible to pair with the DS4. Therefore this workaround exists,
which connects directly to the DS4 when it has been started in pairing mode
(by holding **Share + the PS button** until the LED starts blinking rapidly), then
run any of the following commands to get the controller synced with your system.

This is the default mode as root when running without any options:

    sudo ds4drv
    
However we run ds4drv as root as a background process:

    sudo dsr4dv --daemon


See ``ds4drv --help`` for a list of all the options.


#####DS4 How to use in (Python)
=========
- Navigate to the **DS4Controller/src** folder and run the **run.sh** script. **MAKE SURE SWIG AND ALL THE DEPENDENCIES ABOVE ARE INSTALLED**
    - DO NOT CHANGE THE FILE UNLESS YOU KNOW WHAT YOURE DOING.

- In order to implement the DS4 controller module into a python project, you have to 'import controller'.
- Below is an example of a file that uses this module.

``` python
    # file: test.py
    # This is an example of how this module is used in a python script.
    # For further understanding please visit the documentation.
    from DS4Controller.src import controller
    
     # creates a new controller object.
    ds4 = controller.newController()
    
    # checks if the controller is still active.
    while(ds4.active):
        if(controller.getAxisDown(controller.AXIS_R2)):
            print("R2=%d" % controller.getAxisValue(controller.AXIS_R2))

        if(controller.getAxisDown(controller.AXIS_L2)):
            print("L2=%d" % controller.getAxisValue(controller.AXIS_L2))

        if(controller.getAxisDown(controller.AXIS_LEFT_STICK_X)):
            print("LS_X=%d" % controller.getAxisValue(controller.AXIS_LEFT_STICK_X))

        if(controller.getAxisDown(controller.AXIS_LEFT_STICK_Y)):
            print("LS_Y=%d" % controller.getAxisValue(controller.AXIS_LEFT_STICK_Y))

        if(controller.getAxisDown(controller.AXIS_RIGHT_STICK_X)):
            print("RS_X=%d" % controller.getAxisValue(controller.AXIS_RIGHT_STICK_X))

        if(controller.getAxisDown(controller.AXIS_RIGHT_STICK_Y)):
            print("RS_Y=%d" % controller.getAxisValue(controller.AXIS_RIGHT_STICK_Y))
```

######Controller Constants/Definitions

``` python
    /* DO NOT CHANGE ANY OF THESE HARDCODED ENUM VALUES IN THE SOURCE CODE */
    BTN_SQUARE = 0,
    BTN_CROSS = 1,
    BTN_CIRCLE = 2,
    BTN_TRIANGLE = 3,
    BTN_L1 = 4,
    BTN_R1 = 5,
    BTN_L2 = 6,
    BTN_R2 = 7,
    BTN_SHARE = 8,
    BTN_OPTIONS = 9,
    BTN_LEFT_STICK = 10,
    BTN_RIGHT_STICK = 11,
    /////////////////////
    AXIS_LEFT_STICK_X = 0,
    AXIS_LEFT_STICK_Y = 1,
    AXIS_RIGHT_STICK_X = 2,
    AXIS_RIGHT_STICK_Y = 5,
    AXIS_L2 = 3,
    AXIS_R2 = 4,
    AXIS_LEFT_DPAD = 9,
    AXIS_RIGHT_DPAD = 9,
    AXIS_UP_DPAD = 10,
    AXIS_DOWN_DPAD = 10
```

######Controller Functions

Check the example above to find out some of these functions and constants are used.

``` python 
    ControllerOBJ newControllerOBJ(void); // Needed to create a new controller object.     
    
    void shutDown(ControllerOBJ); // Shuts down the controller, only use when completely done.
    
    bool getKeyDown(int); // Checks if the key is activated. Pass a constant in the parameters.
    
    bool getAxisDown(int); // Checks if the axis is activated. Pass a constant in the parameters.
    
    int getAxisValue(int); // Returns the converted value of an axis thats in use.
    
    char* getControllerName(ControllerOBJ); // gets the name of the controllerName
    
    void deviceInfo(ControllerOBJ); // Gets the device information
```
----------------------------------------------------------------------------



####Distance Sensor
=============
How Distance Sensor Works

Distance Sensors uses the HC-sr04 sensor. Using the GPIO pins the pi sends a signal to the HC-sr04 to triger the sensor.
The sensor then recives a echo signal and calculates the diffrence in time between the trigger and echo. 
This gives the distance in cm after mulitipliying the time by 17150. 
```
        GPIO.output(TRIG, True)
        time.sleep(0.00001)
        GPIO.output(TRIG, False)

        while GPIO.input(ECHO) == 0:
            pulse_start = time.time()

        while GPIO.input(ECHO) == 1:
            pulse_end = time.time()
                
        pulse_duration = pulse_end - pulse_start
                
        distance = pulse_duration * 17150
                
        distance = round(distance, 2)
```

When the distance is below a certain distance the car will auto reverse to prevent hiting an obect.
```
        if distance < 20 and prev_value is False:
            prev_value = True
            out_sensor.send(True)
            print "Stop!!!!"
        elif prev_value is True and distance >= 20:
            prev_value = False
            out_sensor.send(False)
```

.....

------------
</br>

####License Plate
============
......

-----------
</br>


##Known Issues / Limitations
==============================
.......

-----------------------------
</br>

## #TeamTux (#TeamLinux)
===========
[![Jesus Diaz](https://avatars1.githubusercontent.com/u/16565647?v=3&s=144)](https://github.com/diazjesu) | [![Michael Reeves](https://avatars1.githubusercontent.com/u/7333415?v=3&s=144)](https://github.com/ReevMich) | [![Walter Cepeda](https://avatars1.githubusercontent.com/u/16603134?v=3&s=144)](https://github.com/waltercpd) | [![Josh Dassigner](https://avatars1.githubusercontent.com/u/14892282?v=3&s=144)](https://github.com/dassjosh)
---|---|---|---
[Jesus Diaz](https://github.com/diazjesu) | [Michael Reeves](https://github.com/ReevMich) | [Walter Cepeda](https://github.com/waltercpd) |  [Josh Dassigner](https://github.com/dassjosh)
