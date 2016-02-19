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

  while(getActiveState()){ 

    puts("hello");
    sleep(1);
  }
  return 0;
}
