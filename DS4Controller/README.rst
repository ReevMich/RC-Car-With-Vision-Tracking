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
    
    import ControllerModule
    
    controller = ControllerModule.newControllerOBJ()
     
    while(controller.active):
        if(ControllerModule.getAxisDown(ControllerModule.AXIS_R2)):
            print("R2=%d" % ControllerModule.getAxisValue(ControllerModule.AXIS_R2))
    
        if(ControllerModule.getAxisDown(ControllerModule.AXIS_LEFT_STICK_X)):
            print("LS_X=%d" % ControllerModule.getAxisValue(ControllerModule.AXIS_LEFT_STICK_X))
    
        if(ControllerModule.getAxisDown(ControllerModule.AXIS_LEFT_STICK_Y)):
            print("LS_Y=%d" % ControllerModule.getAxisValue(ControllerModule.AXIS_LEFT_STICK_Y))


Controller Constants
--------------------

IN PROGRESS...


Controller Functions
--------------------

IN PROGRESS...
