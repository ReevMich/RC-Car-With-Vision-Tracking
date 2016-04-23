===========================
RC Car with Vision Tracking
===========================

Author(s)
* **[Jesus Diaz](https://github.com/diazjesu)**
* **[Michael Reeves](https://github.com/ReevMich)**
* **[Josh Dassinger](https://github.com/dassjosh)**
* **[Walter Cepeda](https://github.com/waltercpd)**

The RC Car with Vision Tracking is a custom built RC Car with a raspberry pi as the main computer.
This car uses an arduino and H-drive to control the motor and what speed they run at.
The way the RC car with Vision Tracking moves is by utilizing  a camera to track a ball of a predetermined color.
As a secondary control system we have a bluetooth Playstation 4 control for manual control.

* GitHub: https://github.com/du-linux/Team1/

Features
--------

- Manually able to control Remote Control Car with Playstation 4 Controller -- Wired
- Bluetooth Support with Playstation 4 Controller
- Remote Control Car follows a color ball
- Implemented Changing License Plate -- using Arduino
- Implemented Object avoidance, using Ultra Sonic Sensors, with automatic reverse
- Features an Dual H-Bridge that controls all four wheels
- Controlling all 4-wheels with python w/out Arduino
- Reverse Support with the Playstation 4 Controller.

Dependencies
------------

-------------------
####Vision Tracking
-------------------
......


---------
####DS4DRV
---------
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

    $ sudo pip install ds4drv


Installing a recent version of bluez **Required for Bluetooth**    

    cd ~
    wget http://www.kernel.org/pub/linux/bluetooth/bluez-5.37.tar.xz
    tar xvf bluez-5.37.tar.xz

Installing SWIG - The C code Wrapper to Python ** Required to compile C code to Python **
  
    sudo apt-get install swig

#####Using DS4
---------

Unless your system is using BlueZ 5.14 (which was released recently) or higher
it is not possible to pair with the DS4. Therefore this workaround exists,
which connects directly to the DS4 when it has been started in pairing mode
(by holding **Share + the PS button** until the LED starts blinking rapidly).

This is the default mode when running without any options:

    $ ds4drv

Supported protocols: **Bluetooth** and **USB**

This mode uses the Linux kernel feature *hidraw* to talk to already existing
devices on the system.

    $ ds4drv --hidraw

To use the DS4 via bluetooth in this mode you must pair it first. This requires
**BlueZ 5.14+** as there was a bug preventing pairing in earlier verions. How you
actually pair the DS4 with your computer depends on how your system is setup,
suggested googling: *<distro name> bluetooth pairing*


#####DS4 Permissions
----------------

If you want to use ds4drv as a normal user, you need to make sure ds4drv has
permissions to use certain features on your system.

ds4drv uses the kernel module *uinput* to create input devices in user land and
the module *hidraw* to communicate with DualShock 4 controllers (when using
``--hidraw``), but this usually requires root permissions. You can change the
permissions by copying the `udev rules file <udev/50-ds4drv.rules>`_ to
``/etc/udev/rules.d/``.

You may have to reload your udev rules after this with:


    $ sudo udevadm control --reload-rules
    $ sudo udevadm trigger


#####DS4 Configuration file
---------------------------

The preferred way of configuring ds4drv is via a config file.
Take a look at `ds4drv.conf <ds4drv.conf>`_ for example usage.

ds4drv will look for the config file in the following paths:

- ``~/.config/ds4drv.conf``
- ``/etc/ds4drv.conf``

... or you can specify your own location with ``--config``.


#####DS4 Command line options
--------------------
You can also configure using command line options, this will set the LED
to a bright red:

    $ ds4drv --led ff0000

See ``ds4drv --help`` for a list of all the options.


#####DS4 How to use in (Python)
-------------------------------
- Navigate to the **DS4Controller** folder and run the **run.sh** script. **MAKE SURE SWIG IS ALL THE DEPENDENCIES ARE INSTALLED**
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

Controller Constants
--------------------

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

Controller Functions
--------------------

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


-------------------
####Distance Sensor
-------------------
.....


-------------------
####License Plate
-------------------
......


==============================
##Known Issues / Limitations
==============================
