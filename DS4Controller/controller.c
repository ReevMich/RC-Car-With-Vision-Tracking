 #include "controller.h"

int joystick_id = -1;

void Init_DS4(const char *command)
{

  int found = -1;

  system(command);
  
  while(found < 0)
  {
    /* int read = open ("log.txt"); */    
    /*       //system(""); */
    /*     printf("Connecting to ds4 controller... \n"); */
    sleep(2);
  }
  printf("Found it");
  
}

int OpenJoystick()
{
  // Trys and read from the first joystick location
  joystick_id = open(JOYSTICK_DEVICE, O_RDONLY);

  // will return -1 if not joystick is avaliable  
  if(joystick_id < 0 )
  {
    return joystick_id;
  }

  return joystick_id;
}

int GetJoystickStatus(struct JoystickInput *wjse)
{
  
  int rc;
  struct JoystickEvent jse;

  while ((rc = GetJoystickEvents(&jse) == 1))
  {
    jse.type &= ~JS_EVENT_INIT;

   if(jse.type == JS_EVENT_AXIS)
    {
     
      switch(jse.number)
	{
	case 0: wjse->axis[jse.number] = jse.value; /* Left Stick X */
	  printf("Left Stick X Axis %d \n", GetRawAxis(jse.value));
	  break;
	case 1: wjse->axis[jse.number] = jse.value; /* Left Stick Y */
	  printf("Left Stick Y Axis %d \n", GetRawAxis(jse.value));
	  break;
	case 2: wjse->axis[jse.number] = jse.value; /* Right Stick X */
	  printf("Right Stick X Axis %d \n", GetRawAxis(jse.value));
	  break;
	case 3: wjse->axis[jse.number] = jse.value; /* L2 Tigger Axis */
	  printf("L2 Trigger Axis %d \n",GetRawAxis(jse.value));
	  break;
	case 4: wjse->axis[jse.number] = jse.value; /* R2 Trigger Axis */
	  printf("R2 Trigger Axis %d \n", GetRawAxis(jse.value));
	  break;
	case 5: wjse->axis[jse.number] = jse.value; /* Right Stick Y */
	  printf("Right Stick Y Axis %d \n", GetRawAxis(jse.value));
	  break;
	case 9:
	  if(jse.value < 0){
	    wjse->axis[jse.number] = jse.value; /* Left DPAD */
	    printf("Left DPAD Axis \n");
	  }
	  else if (jse.value > 0){  
	    wjse->axis[jse.number] = jse.value; /* Right DPAD */
	    printf("Right DPAD Axis \n");
	  }
	  break;
	case 10:
	  if(jse.value < 0){
	    wjse->axis[jse.number] = jse.value; /* Up DPAD */
	    printf("Up DPAD Axis \n");
	  }
	  else if (jse.value > 0){  
	    wjse->axis[jse.number] = jse.value; /* Down DPAD */
	    printf("Down DPAD Axis \n");
	  }
	  break;
	default:
	  break;
	}
      
      }
        else if(jse.type == JS_EVENT_BUTTON)
      {
      if(jse.number <= NUMBER_OF_BUTTONS && jse.value == 1)
	{
	switch (jse.number)
	  {
	  case 0: wjse->button[jse.number] = jse.value; /* Square Button */
	    printf("Square was pressed \n");
	    break;
	  case 1: wjse->button[jse.number] = jse.value; /* Cross Button */
	    printf("Cross was pressed \n");
	    break;
	  case 2: wjse->button[jse.number] = jse.value; /* Circle Button */
	    printf("Circle was pressed \n");
	    break;
	  case 3: wjse->button[jse.number] = jse.value; /* Triangle Button */
	    printf("Triangle was pressed \n");
	    break;
	  case 4: wjse->button[jse.number] = jse.value; /* L1 Button */
	    printf("L1 was Pressed \n");
	    break;
	  case 5: wjse->button[jse.number] = jse.value; /* R1 Button */
	    printf("R1 was Pressed \n");
	    break;
	  case 6: wjse->button[jse.number] = jse.value; /* L2 Button */
	    printf("L2 was Pressed \n");
	    break;
	  case 7: wjse->button[jse.number] = jse.value; /* R2 Button */
	    printf("R2 was Pressed \n");
	    break;
	  case 8: wjse->button[jse.number] = jse.value; /* R2 Share */
	    printf("Share was Pressed \n");
	    break;
	  case 9: wjse->button[jse.number] = jse.value; /* R2 Options */
	    printf("Options was Pressed \n");
	    break;
	  case 10: wjse->button[jse.number] = jse.value; /* Left Stick Button Options */
	    printf("Left Stick Button was Pressed \n");
	    break;
	  case 11: wjse->button[jse.number] = jse.value; /* Right Stick Button Options */
	    printf("Right Stick Button was Pressed \n");
	    break;
	  default:   
	    break;
	     }
	}
    }
  }
    

  return 0;
}

int GetRawAxis(int inputValue)
{
  int value = ((inputValue - MIN_AXIS_VALUE) * (MAX_RAW_AXIS_VALUE - MIN_RAW_AXIS_VALUE) / (MAX_AXIS_VALUE - MIN_AXIS_VALUE) + 0);

  return value;
}

int GetJoystickEvents(struct JoystickEvent *jse)
{
  int bytes;

  bytes = read(joystick_id, jse, sizeof(*jse));

  if(bytes == -1)
    return 0;
  
  if(bytes == sizeof(*jse))
    return 1;

  printf("Unexpected bytes from joystick: %d\n", bytes);
  return -1;
}
