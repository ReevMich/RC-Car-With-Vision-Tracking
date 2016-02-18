//
// Created by Captain on 2/18/16.
//
#pragma GCC diagnostic error "-Wformat"

#include <stdio.h>
#include <stdlib.h>
#include "ControllerOBJ.h"

int main()
{

    ControllerOBJ controller;
    controller = newControllerOBJ();

    printf("value of private int==%d\n", getIDNumber(controller));

    setIDNumber(controller,26);

    printf("value of private int==%d\n", getIDNumber(controller));

    return 0;
}