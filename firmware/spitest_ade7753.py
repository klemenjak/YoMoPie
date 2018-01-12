import time
import spidev
import sys
import RPi.GPIO as GPIO
 
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(19,GPIO.OUT)
spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz = 62500
spi.mode = 0b01

if len(sys.argv) > 1:
    register = int(sys.argv[1], 16)
else:
    register = 0x1C

GPIO.output(19, GPIO.HIGH)

result = spi.xfer2([register, 0x00, 0x00, 0x00])[1:]
print "reading register {}:".format(hex(register))
print [bin(x) for x in result]
print [hex(x) for x in result]
print result[0]
print result[1]
print result[2]

print "done"
 
spi.close()
