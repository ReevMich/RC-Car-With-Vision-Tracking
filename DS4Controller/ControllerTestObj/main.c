//
// Created by Captain on 2/18/16.
//
#pragma GCC diagnostic error "-Wformat"

#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include "ControllerOBJ.h"

struct Books{

  int id;
  
};

struct Books book1;

int main()
{
  book1.id = 900;

  ControllerOBJ controller;
  controller = newControllerOBJ();

  while(getActiveState(controller)){ 

    if(getKeyDown(BTN_SQUARE)) {
      puts("Button");
    }
    if(getAxisDown(AXIS_L2)){
      int value = getAxisValue(AXIS_L2);
      printf("L2 = %d \n", value); 
    }
    if(getAxisDown(AXIS_R2)){
      int value = getAxisValue(AXIS_R2);
      printf("R2 = %d \n", value); 
    }

    //sleep(1);
  }
  return 0;
}
