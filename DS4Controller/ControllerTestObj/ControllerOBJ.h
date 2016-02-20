//
// Created by Captain on 2/18/16.
//
// This header should only be accessible from controllerOBJ.c
#include <stdbool.h>

typedef enum{
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
    BTN_RIGHT_STICK = 11
} keycode;

typedef enum{
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
} axiscode;
typedef struct controllerobj * ControllerOBJ;
ControllerOBJ newControllerOBJ();
static void Initialize(ControllerOBJ);
static void* Loop(void* parameters);
//static void ReadEvent(struct js_event *jse);
void deleteControllerOBJ(ControllerOBJ);
bool getActiveState(ControllerOBJ);
bool getKeyDown(keycode key);
bool getAxisDown(axiscode axis);
int getAxisValue(axiscode axis);
static int GetRawAxis(int inputValue);


