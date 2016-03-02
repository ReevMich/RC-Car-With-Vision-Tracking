DS4 Controller Module!
=============================

DS4 Controller Module is for #TeamTux's Unix School project.



How to use in (Python)
^^^^^^^^^^^^^^^^^^^^^^
- Navigate to the **DS4Controller** folder and run the **run.sh** script.
    - DO NOT CHANGE THE FILE UNLESS YOU KNOW WHAT YOURE DOING.

- In order to implement the DS4 controller module into a python project, you have to 'import ControllerModule'.
- Below is an example of a file that uses this module.

.. code-block:: python

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

Controller Constants
--------------------

.. code-block:: c

    /* Do not change any of these harded enums values in the source code. */
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


Controller Functions
--------------------

Check the example above to find out some of these functions and constants are used.

.. code-block:: c
 
    ControllerOBJ newControllerOBJ(void); // Needed to create a new controller object.      
    void shutDown(ControllerOBJ); // Shuts down the controller, only use when completely done.
    bool getKeyDown(int); // Checks if the key is activated. Pass a constant in the parameters.
    bool getAxisDown(int); // Checks if the axis is activated. Pass a constant in the parameters.
    int getAxisValue(int); // Returns the converted value of an axis thats in use.
    char* getControllerName(ControllerOBJ); // gets the name of the controllerName
    void deviceInfo(ControllerOBJ); // Gets the device information
