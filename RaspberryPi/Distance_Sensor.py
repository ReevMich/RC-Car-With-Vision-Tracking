import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
#sets the GPIO pins
TRIG = 23
ECHO = 24


def main(dist_pipe):

    print "Distance Measurement In Progress"

    out_sensor, _ = dist_pipe

    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)

    GPIO.output(TRIG, False)

    print "Waiting For Sensor To Settle"
    time.sleep(.5)

    prev_value = False

    while True:
        time.sleep(.25)
      #sends a pulse for .00001 of a second 
        GPIO.output(TRIG, True)
        time.sleep(0.00001)
        GPIO.output(TRIG, False)
        #sends pulse
        while GPIO.input(ECHO) == 0:
            pulse_start = time.time()
        #recives pulse
        while GPIO.input(ECHO) == 1:
            pulse_end = time.time()

        #calculate diffrence between start and end
        pulse_duration = pulse_end - pulse_start

        # find distance in cm
        distance = pulse_duration * 17150
                
        distance = round(distance, 2)

        #when distance is less then 20cm make car stop and reverse 
        if distance < 20 and prev_value is False:
            prev_value = True
            out_sensor.send(True)
            print "Stop!!!!"
        #if greater then 20cm continue with normal commands.
        elif prev_value is True and distance >= 20:
            prev_value = False
            out_sensor.send(False)

        #print "Distance:", distance, "cm"
    
    GPIO.cleanup()
