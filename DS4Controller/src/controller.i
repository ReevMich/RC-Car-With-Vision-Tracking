
%module ControllerModule
%{
#include "controller.h"

  void Initialize(ControllerOBJ parameters);
  void* Loop(void*);
  void shutDown(ControllerOBJ);
  bool getKeyDown(int);
  bool getAxisDown(int);
  int getAxisValue(int);
  char* getControllerName(ControllerOBJ);
  void deviceInfo(ControllerOBJ);
  ControllerOBJ newControllerOBJ(void);
%}
#include "controller.h"

typedef struct controllerobj * ControllerOBJ;
struct controllerobj {
  char* name;
  int version;
  char* numAxis;
  char* numButtons; 
  pthread_t thread;
  int active;
  int mode; 
};

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
  /////////////////////
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

void Initialize(ControllerOBJ);
void* Loop(void*);
void shutDown(ControllerOBJ);
bool getKeyDown(int);
bool getAxisDown(int);
int getAxisValue(int);
char* getControllerName(ControllerOBJ);
void deviceInfo(ControllerOBJ);
ControllerOBJ newControllerOBJ(void);
