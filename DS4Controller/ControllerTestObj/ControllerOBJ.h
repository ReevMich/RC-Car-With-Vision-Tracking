//
// Created by Captain on 2/18/16.
//
// This header should only be accessible from controllerOBJ.c
typedef enum{
    BTN_SQUARE,
    BTN_CROSS,
    BTN_CIRCLE
} keycode;

typedef struct controllerobj * ControllerOBJ;
ControllerOBJ newControllerOBJ();
static void Initialize(ControllerOBJ);
static void* Loop(void* parameters);
//static void ReadEvent(struct js_event *jse);
void deleteControllerOBJ(ControllerOBJ);
bool getActiveState(ControllerOBJ);
bool getKeyDown(keycode key);


