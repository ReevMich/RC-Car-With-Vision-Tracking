// File:                Joystick.h
// Author:              Michael Reeves
// Last Modified:       2/20/2016
// Description:         This source file contains all the important
// structures and definitions for the joystick.


#define JOYSTICK_DEVICE  "/dev/input/js0" /* Device file location */

#define JS_BUTTON         0x01     /* button pressed/released */
#define JS_AXIS           0x02     /* joystick moved */
#define JS_INIT           0x80     /* initial state of device */
#define NUMBER_OF_BUTTONS       0x12     /* number of buttons on the ps4 controller */

#define MIN_AXIS_VALUE         -32767    /* Lowest axis value the controller outputs */
#define MAX_AXIS_VALUE          32767    /* Highest axis value the controller outputs */
#define MIN_RAW_AXIS_VALUE      0        /* Lowest value we want to the controller to output */
#define MAX_RAW_AXIS_VALUE      100      /* Highest value we want to the controller to output */

// The number of buttons and axis our controller has.
typedef struct js_state {
  int button[NUMBER_OF_BUTTONS]; // Contains the states of all the buttons
  int axis[NUMBER_OF_BUTTONS]; // Contains the states of all the axis
} js_state;

