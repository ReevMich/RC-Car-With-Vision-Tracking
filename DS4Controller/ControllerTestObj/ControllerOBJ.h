//
// Created by Captain on 2/18/16.
//

typedef struct controllerobj * ControllerOBJ;
ControllerOBJ newControllerOBJ();
static void Initialize(ControllerOBJ);

void setIDNumber(ControllerOBJ,int);
int getIDNumber(ControllerOBJ);
void deleteControllerOBJ(ControllerOBJ);



