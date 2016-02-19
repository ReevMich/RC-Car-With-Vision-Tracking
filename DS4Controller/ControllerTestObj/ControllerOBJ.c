//
// Created by Captain on 2/18/16.
//

#include <pthread.h>
#include <fcntl.h>
#include <linux/types.h>
#include <stdio.h>
#include <strings.h>
#include <stdlib.h>
#include <stdbool.h>
#include "ControllerOBJ.h"
#include "Joystick.h"

struct controllerobj {

  pthread_t thread;
  
};

static pthread_mutex_t mutex_lock;
static bool active;
static int js_fd;

static js_state state;

static void ReadEvent(struct js_event *jse);

// Private methods -----------------------------------------------
// Runs all the necessary functions to ensure connectivity
static void Initialize(ControllerOBJ controller)
{
  int fd = open(JOYSTICK_DEVICE, O_RDONLY | O_NONBLOCK);
  
  if(fd > 0)
    {
      js_fd = fd;
      active = true;
      pthread_attr_t attr;
      pthread_attr_init(&attr);
      pthread_create(&controller->thread,&attr, Loop, &controller);
    }
}

static void* Loop(void* parameters){

  pthread_mutex_lock(&mutex_lock);
  
  struct js_event jse;
  
  while(active){    
    ReadEvent(&jse);
  }

  pthread_mutex_lock(&mutex_lock);
  
}


static void ReadEvent(struct js_event *jse){
  
  int bytes = read(js_fd,jse, sizeof(*jse));

  if(bytes > 0)
    {
      jse->type &= ~JS_INIT;
      if(jse->type == JS_AXIS){
	state.axis[jse->number] = jse->value;
	printf("AXIS \n");
      }
      if(jse->type == JS_BUTTON){
	printf("BUTTON \n");
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

void deleteControllerOBJ(ControllerOBJ controller) {
  free(controller);
}

bool getActiveState(ControllerOBJ controller){
  return active;
}

bool getKeyDown (enum KeyCode key){
  return false;
}
