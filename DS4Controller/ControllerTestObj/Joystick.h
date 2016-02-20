//
// Created by Captain on 2/18/16.
//

#define JOYSTICK_DEVICE  "/dev/input/js0"

#define JS_BUTTON         0x01     /* button pressed/released */
#define JS_AXIS           0x02     /* joystick moved */
#define JS_INIT           0x80     /* initial state of device */
#define NUMBER_OF_BUTTONS       0x12     /* number of buttons on the ps4 controller */

#define MIN_AXIS_VALUE         -32767    /* Lowest axis value the controller outputs */
#define MAX_AXIS_VALUE          32767    /* Highest axis value the controller outputs */

#define MIN_REV_AXIS_VALUE     -100
#define MAX_REV_AXIS_VALUE     0

#define MIN_RAW_AXIS_VALUE      0        /* Lowest value we want to the controller to output */
#define MAX_RAW_AXIS_VALUE      100      /* Highest value we want to the controller to output */

typedef struct js_event {
    __u32 time;     /* event timestamp in milliseconds */
    __s16 value;    /* value */
    __u8 type;      /* event type */
    __u8 number;    /* axis/button number */
} js_event;

typedef struct js_state {
    int button[NUMBER_OF_BUTTONS];
    int axis[NUMBER_OF_BUTTONS];
} js_state;


//TODO: Find out where this can go!!!

