// File:                ControllerOBJ.c
// Author:              Michael Reeves
// Last Modified:       2/20/2016
// Description:         This source file glue to all the other controller
// modules and this runs on a seperate thread from the main program.
//#include "Joystick.h"
#include "ControllerOBJ.h"


struct controllerobj {
  char* name;
  int version;
  char* numAxis; // Add functionality for this later
  char* numButtons; // Add functionality for this later
  pthread_t thread;
  int active;
  int mode; // Add functionality so that we can incorporate more
            // functionality to the controller.
};

static pthread_mutex_t mutex_lock;
static int js_fd;

static js_state state;

// Private methods -----------------------------------------------
// Runs all the necessary functions to ensure connectivity
static void Initialize(ControllerOBJ controller)
{
  int fd = open(JOYSTICK_DEVICE, O_RDONLY);
  
  if(fd > 0){
    char name[1024];
    int version;
    js_fd = fd;
    controller->active = true;
    
    // store driver version, if it is less than
    // version 1.0 there will be no support for it
    ioctl(fd, JSIOCGVERSION, &version);
    if (version < 0x010000){
      return;
    }
    controller->version = version;

    // store size of the name and makes sure its not null
    // if its valid store the name into our struct.
    int ret = ioctl(fd, JSIOCGNAME(sizeof(name)), name);
    if (ret < 0){
      return;
    }
    controller->name = name;
 
    pthread_attr_t attr;
    pthread_attr_init(&attr);
    pthread_create(&controller->thread,&attr, Loop, (void*)controller);

  }
}

// Loop -- The infinite loop that will get any sort
// of input from the device.
static void* Loop(void* parameters){
  
  ControllerOBJ controller = (ControllerOBJ)parameters; 
  struct js_event jse;
  
  while(controller->active){    
    ReadEvent(&jse);
  }
  
}

// ReadEvent -- 
static void ReadEvent(struct js_event *jse){
  
  int bytes = read(js_fd,jse, sizeof(*jse));
  
  if(bytes > 0){
    jse->type &= ~JS_EVENT_INIT;
    if(jse->type == JS_EVENT_AXIS){
      state.axis[jse->number] = GetRawAxis(jse->value);
    }
    if(jse->type == JS_EVENT_BUTTON){
      state.button[jse->number] = jse->value;
    }
  }
  
}

//TODO: ADD COMMAND PARAMETER IN THE CONSTRUCTOR
// Public methods ------------------------------------------------
ControllerOBJ newControllerOBJ() {
  ControllerOBJ controller = (ControllerOBJ) malloc(sizeof(struct controllerobj));
  bzero(controller, sizeof(struct controllerobj));

  Initialize(controller);
  
  return controller;
}

char* getControllerName(ControllerOBJ controller){
  return controller->name;
}

void deleteControllerOBJ(ControllerOBJ controller) {
  free(controller);
}

bool getActiveState(ControllerOBJ controller){
  return controller->active;
}

bool getKeyDown (keycode button){
  if(state.button[button]>0){
    return true;
  }
  return false;
}

bool getAxisDown (axiscode axis){
  if(state.axis[axis] > 0){
    return true;
  }
  
  return false;
}

int getAxisValue(axiscode axis){

  if(getAxisDown(axis)) {
    return state.axis[axis];
  }
  
  return 0;
}

static int GetRawAxis(int inputValue)
{
  int value = ((inputValue - MIN_AXIS_VALUE) * (MAX_RAW_AXIS_VALUE - MIN_RAW_AXIS_VALUE) / (MAX_AXIS_VALUE - MIN_AXIS_VALUE) + 0);

  return value;
}

void printDeviceInfo(ControllerOBJ controller){
   printf("\t============================================================\n\n");
  printf("\tDevice Name: %s\n", controller->name);
  printf("\tDevice Driver Version: %d\n\n", controller->version);
  printf("\t============================================================\n");
}
