#include "DS4.h"
#include <errno.h>

static int js_fd;

static js_state state;

// static functions must be defined in the file their used in.
static float GetRawAxis(float inputValue);
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
  int errorNum;
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
  } else {
    errorNum = fd;
    fprintf(stderr, "Error: problem opening controller input file: %s\nError: the controller is not connected.\n", strerror( errorNum ));
  }
}

//TODO: ADD COMMAND PARAMETER IN THE CONSTRUCTOR
// Public methods ------------------------------------------------
Controller newController(void) {
  Controller controller = (Controller) malloc(sizeof(struct controller));
  bzero(controller, sizeof(struct controller));

  Initialize(controller);
  
  return controller;
}

static void deleteController(Controller controller) {
  free(controller);
}

bool getActiveState(Controller controller){
  return controller->active;
}

bool getButtonDown (int button){
  if(state.button[button]>0){
    return true;
  }
  return false;
}

bool getAxisDown (int axis){

  if((axis == AXIS_LEFT_STICK_X || axis == AXIS_LEFT_STICK_Y) ||
     (axis == AXIS_RIGHT_STICK_X || axis == AXIS_RIGHT_STICK_Y)){

    if((state.axis[axis] >= 0 || state.axis[axis] <= 1) && state.axis[axis] != .5){
      return true;
    }
    
  } else if(state.axis[axis] > 0){
    return true;
  }
  
  return false;
}

float getAxisValue(int axis){

  if(getAxisDown(axis)) {
    // printf("Debug: Axis Value --- %f", state.axis[axis]); // Debug Code
    return state.axis[axis];
  }
  
  return 0;
}

static float GetRawAxis(float inputValue)
{
  float value = ((inputValue - MIN_AXIS_VALUE) * (MAX_RAW_AXIS_VALUE - MIN_RAW_AXIS_VALUE) / (MAX_AXIS_VALUE - MIN_AXIS_VALUE) + 0);
  return value/100.0;
}

char* getControllerName(Controller controller){
  return controller->name;
}



void shutDown(Controller controller){
  printf("Shutting Down %s...\n", getControllerName(controller));
  if(controller == NULL){
    puts("Done...");
    return;
  }
  controller->shuttingDown = true;
  puts("Please wait a few seconds....");
  controller->active = false;
  pthread_exit(&controller->thread);
  puts("Stopping Running Thread....");
  sleep(1);
  puts("Freeing up memory...");
  controller->shuttingDown = false;
  deleteController(controller);
  puts("Done..");
}
