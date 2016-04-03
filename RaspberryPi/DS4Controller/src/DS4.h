#include <linux/types.h>
#include <linux/joystick.h>
#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <fcntl.h>
#include <stdbool.h>
#include <unistd.h>


// ========================================================================
//                             DEFINITIONS
// ========================================================================

#define JOYSTICK_DEVICE  "/dev/input/js0" /* Device file location */

#define NUMBER_OF_BUTTONS       0x12     /* number of buttons on the ps4 controller */
#define MIN_AXIS_VALUE         -32767    /* Lowest axis value the controller outputs */
#define MAX_AXIS_VALUE          32767   /* Highest axis value the controller outputs */
#define MIN_RAW_AXIS_VALUE      0.0        /* Lowest value we want to the controller to output */
#define MAX_RAW_AXIS_VALUE      100.0      /* Highest value we want to the controller to output */
									  
// ========================================================================
//                                 ENUMS
// ========================================================================

	
// keycode -- Is the index that is links to the button array in the
// js_state struct in the Joystick.h header. Useful if you want
// to check out what button is being pressed in the main.
typedef enum KeyCode{
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
  BTN_PS = 12,
  AXIS_LEFT_STICK_X = 0,
  AXIS_LEFT_STICK_Y = 1,
  AXIS_RIGHT_STICK_X = 2,
  AXIS_L2 = 3,
  AXIS_R2 = 4,
  AXIS_RIGHT_STICK_Y = 5,
  AXIS_LEFT_DPAD = 9,
  AXIS_RIGHT_DPAD = 9,
  AXIS_UP_DPAD = 10,
  AXIS_DOWN_DPAD = 10
}keycode;
							  


// ========================================================================
//                              STRUCTS
// ========================================================================


// creates a new type definition of a struct named controllerobj and
// points it to the ControllerOBJ name
typedef struct controller * Controller;

struct controller {
  char* name;
  int version;
  char* numAxis; // Add functionality for this later
  char* numButtons; // Add functionality for this later
  pthread_t thread;
  int active;
  int mode; // Add functionality so that we can incorporate more functionality to the controller.
  int shuttingDown;
};


// The number of buttons and axis our controller has.
typedef struct js_state {
  int button[NUMBER_OF_BUTTONS]; // Contains the states of all the buttons
  float axis[NUMBER_OF_BUTTONS]; // Contains the states of all the axis
} js_state;
