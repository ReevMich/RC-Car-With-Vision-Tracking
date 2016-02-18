#include "controller.c"

int main( int argc, const char* argv[] )
{
  Init_DS4("sudo ds4drv --daemon");

  int fd,rc;
  int done = 0;

  JoystickInput jse;
  DS4Buttons button = BTN_SQUARE;
  
  printf("Button number %d", button);
  fd = OpenJoystick();

  if( fd < 0 )
    {
      fprintf(stderr,"Error: Joysticks were found",strerror(errno));
      exit(1);
    }

  pthread_t thread_handle;
  pthread_attr_t attr;
  pthread_attr_init(&attr);
  pthread_create(&thread_handle,&attr, GetJoystickStatus_Log, &jse);
 
  while(1)
    {
      printf("CALLING");
      GetButtonDown(&button);
      
    } 
  // Wait until thread is done with its work
  pthread_join(thread_handle,NULL);
  
  
  return 0;
}  
