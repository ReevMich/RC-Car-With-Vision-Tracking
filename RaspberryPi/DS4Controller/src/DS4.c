///////////////////////////////////////////////////////////////////////
// Author(s): Michael Reeves
// File: DS4.c
// Description: DS4 Controller driver takes input from the controller 
//          and stores the values into an array of buttons and inputs.
///////////////////////////////////////////////////////////////////////
#include "DS4.h"

static int js_fd;

static js_state state;

// static functions must be defined in the file their used in. (FROM WHAT I UNDERSTAND)
static int GetRawAxis(int inputValue);
static void ReadEvent(struct js_event *jse);
static void deleteController(Controller controller);

// Loop -- The infinite loop that will get any sort
// of input from the device.
void* Loop(void* parameters){
  
  Controller controller = (Controller)parameters; 
  struct js_event jse;
  
  while(controller->active){
    ReadEvent(&jse);
  }

  return 0;
}

// ReadEvent -- Reads from the controller everytime an input button is pressed.
// Also we store 
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

// DeviceInfo -- Prints a controller information
void deviceInfo(Controller controller){
  printf("\t============================================================\n\n");
  printf("\tDevice Name: %s\n",controller->name);
  printf("\tDevice Driver Version: %d\n\n", controller->version);
  printf("\t============================================================\n");
}

// Private methods -----------------------------------------------
// Runs all the necessary functions to ensure connectivity
void Initialize(Controller controller){
  int fd = open(JOYSTICK_DEVICE, O_RDONLY);

  if(fd > 0){
    char name[128];
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
    
    controller->name = strdup(name);

    deviceInfo(controller);
    pthread_attr_t attr;
    pthread_attr_init(&attr);
    pthread_create(&controller->thread,&attr, Loop, (void*)controller);
  }

}

// Public methods ------------------------------------------------
Controller newController(void) {
  Controller controller = (Controller) malloc(sizeof(struct controller));
  bzero(controller, sizeof(struct controller));

  Initialize(controller);
  
  return controller;
}

// deleteController -- Frees memory after we are done.
static void deleteController(Controller controller) {
  free(controller);
}

// getActiveState -- Checks to see if the controller is active
bool getActiveState(Controller controller){
  return controller->active;
}

// getKeyDown -- Check if the specific key is currently being pressed
bool getKeyDown (int button){
  if(state.button[button]>0){
    return true;
  }
  return false;
}

// getAxisDown -- Check if the specific axis is currently being pressed
bool getAxisDown (int axis){

  // if the controller input is equal to one of the 4 options then we want to check if the value is
  // between 0 and 100, to know if we are actually return 100 meaning the wheels will be max out or 
  // 0 where the wheels arent turning
  if((axis == AXIS_LEFT_STICK_X || axis == AXIS_LEFT_STICK_Y) ||
     (axis == AXIS_RIGHT_STICK_X || axis == AXIS_RIGHT_STICK_Y)){
      
    if((state.axis[axis] >= 0 || state.axis[axis] <= 100) && state.axis[axis] != 50){
      return true;
    }
  
  // return the axis is greater than 0 then just return true.
  // These axis can only be 0 or 1
  } else if(state.axis[axis] > 0){
    return true;
  }
 
  return false;
}


// Returns the value of a specific axis button
int getAxisValue(int axis){

  if(getAxisDown(axis)) {
    return state.axis[axis];
  }
  
  return 0;
}

// Converts the standard controller output value to a readable and understandable value 0 - 100
static int GetRawAxis(int inputValue)
{
  int value = ((inputValue - MIN_AXIS_VALUE) * (MAX_RAW_AXIS_VALUE - MIN_RAW_AXIS_VALUE) / (MAX_AXIS_VALUE - MIN_AXIS_VALUE) + 0);

  return value;
}

// Returns the controller name
char* getControllerName(Controller controller){
  return controller->name;
}

// Free memory, and sets the controller from active to not active and kills the thread.
void shutDown(Controller controller){
  sleep(3);
  puts("Freeing up memory...");
  controller->active = false;
  deleteController(controller);
  sleep(3);
  puts("Done..");
  pthread_cancel(controller->thread);
}
