#include "controller.h"

static int js_fd;

static js_state state;

// static functions must be defined in the file their used in.
static int GetRawAxis(int inputValue);
static void ReadEvent(struct js_event *jse);
static void deleteControllerOBJ(ControllerOBJ controller);

// Loop -- The infinite loop that will get any sort
// of input from the device.
void* Loop(void* parameters){
  
  ControllerOBJ controller = (ControllerOBJ)parameters; 
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

void deviceInfo(ControllerOBJ controller){
  printf("\t============================================================\n\n");
  printf("\tDevice Name: %s\n",controller->name);
  printf("\tDevice Driver Version: %d\n\n", controller->version);
  printf("\t============================================================\n");
}

// Private methods -----------------------------------------------
// Runs all the necessary functions to ensure connectivity
void Initialize(ControllerOBJ controller){
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

//TODO: ADD COMMAND PARAMETER IN THE CONSTRUCTOR
// Public methods ------------------------------------------------
ControllerOBJ newControllerOBJ(void) {
  ControllerOBJ controller = (ControllerOBJ) malloc(sizeof(struct controllerobj));
  bzero(controller, sizeof(struct controllerobj));

  Initialize(controller);
  
  return controller;
}

static void deleteControllerOBJ(ControllerOBJ controller) {
  free(controller);
}

bool getActiveState(ControllerOBJ controller){
  return controller->active;
}

bool getKeyDown (int button){
  if(state.button[button]>0){
    return true;
  }
  return false;
}

bool getAxisDown (int axis){

  if(axis == AXIS_LEFT_STICK_X || axis == AXIS_LEFT_STICK_Y ||
     axis == AXIS_RIGHT_STICK_X || axis == AXIS_RIGHT_STICK_Y){

    if((state.axis[axis] >= 0 || state.axis[axis] <= 100) && state.axis[axis] != 50){
      return true;
    }
    
  } else if(state.axis[axis] > 0){
    return true;
  }
  
  return false;
}

int getAxisValue(int axis){

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

char* getControllerName(ControllerOBJ controller){
  return controller->name;
}



void shutDown(ControllerOBJ controller){
  printf("Shutting Down %s...\n", getControllerName(controller));
  if(controller == NULL){
    puts("Done...");
    return;
  }
  puts("Please wait a few seconds....");
  controller->active = false;
  pthread_cancel(controller->thread);
  puts("Stopping Running Thread....");
  sleep(3);
  puts("Freeing up memory...");
  deleteControllerOBJ(controller);
  sleep(3);
  puts("Done..");
}
