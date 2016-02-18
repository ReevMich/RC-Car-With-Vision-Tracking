#include <fcntl.h>
#include <stdio.h>
#include <linux/types.h>
#include <errno.h>
#include <stdlib.h>
#include <pthread.h>
#include <stdbool.h>

#define JOYSTICK_DEVICE  "/dev/input/js0"
#define JOYSTICK_DEVICE1  "/dev/input/js1"

#define JS_BUTTON         0x01     /* button pressed/released */
#define JS_AXIS           0x02     /* joystick moved */
#define JS_INIT           0x80     /* initial state of device */
#define NUMBER_OF_BUTTONS       0x12     /* number of buttons on the ps4 controller */

#define MIN_AXIS_VALUE         -32767    /* Lowest axis value the controller outputs */
#define MAX_AXIS_VALUE          32767    /* Highest axis value the controller outputs */

#define MIN_RAW_AXIS_VALUE      0        /* Lowest value we want to the controller to output */
#define MAX_RAW_AXIS_VALUE      255      /* Highest value we want to the controller to output */

typedef struct JoystickEvent {
  __u32 time;     /* event timestamp in milliseconds */
  __s16 value;    /* value */
  __u8 type;      /* event type */
  __u8 number;    /* axis/button number */
} JoystickEvent;

typedef struct JoystickInput {
  int button[NUMBER_OF_BUTTONS];
  int axis[NUMBER_OF_BUTTONS];
} JoystickInput;

typedef enum DS4Buttons{
  BTN_SQUARE = 0,
  BTN_CROSS = 1,
  BTN_CIRCLE = 2  
} DS4Buttons;

//
void Init_DS4(const char *command);

// Opens the joystick device file
int OpenJoystick();

//
void* GetJoystickStatus(void* parameter);
//
int GetJoystickEvents(struct JoystickEvent *jse);

int GetRawAxis(int inputValue);

void* Loop(void* obj);

void GetButtonDown(DS4Buttons *parameter);
