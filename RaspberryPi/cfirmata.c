#include "firmata.h"

int             main()
{
  t_firmata     *firmata;
  int           i = 0;

  //init Firmata
  firmata = firmata_new("/dev/ttyACM0");
  //Wait until device is up
  while(!firmata->isReady)
    firmata_pull(firmata);
  //set pin 13 (led on most arduino) to out
  firmata_pinMode(firmata, 10, MODE_OUTPUT);
  while (1)
    {
      sleep(1);
      if (i++ % 2)
	firmata_digitalWrite(firmata, 13, HIGH); //light led
      else
	firmata_digitalWrite(firmata, 13, LOW); //unlight led
    }
}
