import time
import spidev
import sys
import RPi.GPIO as GPIO
 
read = 0b00111111
write = 0b10000000
 
def init_yomopi():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(19,GPIO.OUT)
    spi = spidev.SpiDev()
    spi.open(0,0)
    spi.max_speed_hz = 62500
    spi.mode = 0b01
    return spi

def enable_board():
    GPIO.output(19, GPIO.HIGH)
    return

def disable_board():
    GPIO.output(19, GPIO.LOW)
    return

def read_8bit(register):
    enable_board()
    register = register & read
    result = spi.xfer2([register, 0x00])[1:]        
    return result
    
def read_16bit(register):
    enable_board()
    register = register & read
    result = spi.xfer2([register, 0x00, 0x00])[1:]        
    return result
    
def read_24bit(register):
    enable_board()
    register = register & read
    result = spi.xfer2([register, 0x00, 0x00, 0x00])[1:]        
    return result

def read_temp():
    reg = read_8bit(0x08)
    temp = reg[0]
    if temp > 127:
        return (temp-1)^0xFF
    else:
        return temp
    
def read_aenergy():
    reg = read_24bit(0x02)
    aenergy = reg[0]<<16+reg[1]<<8+reg[2]
    return aenergy

if len(sys.argv) > 1:
    register = int(sys.argv[1], 16)
else:
    register = 0x0B
    
spi=init_yomopi()

while True:
    print read_temp()
    print read_aenergy()
    time.sleep(1)

spi.close()
