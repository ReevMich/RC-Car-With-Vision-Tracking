
%module controller
%{
#include "DS4.h"

  void Initialize(Controller parameters);
  void* Loop(void*);
  void shutDown(Controller);
  bool getButtonDown(int);
  bool getAxisDown(int);
  int getAxisValue(int);
  char* getControllerName(Controller);
  void deviceInfo(Controller);
  Controller newController(void);
%}
#include "DS4.h"

typedef struct controller * Controller;
struct controller {
  char* name;
  int version;
  char* numAxis;
  char* numButtons; 
  pthread_t thread;
  int active;
  int mode;
  int shuttingDown;
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
  BTN_PS = 12,
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

void Initialize(Controller);
void* Loop(void*);
void shutDown(Controller);
bool getButtonDown(int);
bool getAxisDown(int);
int getAxisValue(int);
char* getControllerName(Controller);
void deviceInfo(Controller);
Controller newController(void);
