//
// Created by Captain on 2/18/16.
//

#include <stdio.h>
#include <strings.h>
#include <stdlib.h>
#include <stdbool.h>
#include <pthread.h>
#include "ControllerOBJ.h"
#include "Joystick.h"



struct controllerobj {

    int fd;
    bool active;
    pthread_t thread;
    char name[256];

};

// Private methods -----------------------------------------------
// Runs all the necessary functions to ensure connectivity
static void Initialize(ControllerOBJ controller){

    controller->fd = open(JOYSTICK_DEVICE, O_RDONLY);

}

//TODO: ADD COMMAND PARAMETER IN THE CONSTRUCTOR
// Public methods ------------------------------------------------
ControllerOBJ newControllerOBJ() {

    ControllerOBJ controller = (ControllerOBJ) malloc(sizeof(struct controllerobj));
    bzero(controller, sizeof(struct controllerobj));

    Initialize(controller);

    return controller;

}

void setIDNumber(ControllerOBJ controller, int number) {
    if (controller==NULL) return;

    controller->id = number;
}

int getIDNumber(ControllerOBJ controllerOBJ)
{
    return controllerOBJ->id;
}

void deleteControllerOBJ(ControllerOBJ controller) {
    free(controller);
}

