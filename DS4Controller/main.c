// File:                
// Author:              
// Last Modified:       2/20/2016
// Description:         ...
#pragma GCC diagnostic error "-Wformat"

#include "ControllerOBJ.h"

int main()
{
  ControllerOBJ controller;
  controller = newControllerOBJ();

  printDeviceInfo(controller);
  
  while(getActiveState(controller)){ 
    // puts("h");
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
  }
  return 0;
}
