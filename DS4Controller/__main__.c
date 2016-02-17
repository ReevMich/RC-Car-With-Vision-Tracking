#include "controller.c"

int main( int argc, const char* argv[] )
{

  Init_DS4("");

  int fd,rc;
  int done = 0;

  struct JoystickInput jse;

  fd = OpenJoystick();

  if( fd < 0 )
    {
      fprintf(stderr,"Error: Joysticks were found",strerror(errno));
      exit(1);
    }

  int e =  GetJoystickStatus(&jse);

  return 0;
}  
