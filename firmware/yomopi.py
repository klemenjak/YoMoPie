import time
import spidev
import sys
import RPi.GPIO as GPIO 
 
class YoMoPi: 
    read = 0b00111111
    write = 0b10000000
    spi=0
    
    def __init__(self):
        self.spi=spidev.SpiDev()
        return 
 
    def init_yomopi(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(19,GPIO.OUT)
        self.spi.open(0,0)
        self.spi.max_speed_hz = 62500
        self.spi.mode = 0b01
        return 

    def enable_board(self):
        GPIO.output(19, GPIO.HIGH)
        return

    def disable_board(self):
        GPIO.output(19, GPIO.LOW)
        return
    
    def write_8bit(self, register, value):
        self.enable_board()
        register = register | self.write
        self.spi.xfer2([register, value])
        return

    def read_8bit(self, register):
        self.enable_board()
        register = register & self.read
        result = self.spi.xfer2([register, 0x00])[1:]        
        return result
        
    def read_16bit(self, register):
        self.enable_board()
        register = register & self.read
        result = self.spi.xfer2([register, 0x00, 0x00])[1:]        
        return result
        
    def read_24bit(self, register):
        self.enable_board()
        register = register & self.read
        result = self.spi.xfer2([register, 0x00, 0x00, 0x00])[1:]        
        return result

    def read_temp(self):
        reg = self.read_8bit(0x08)
        temp = (reg[0]-129)/4
        return temp
    
    def read_aenergy(self):
        reg = self.read_24bit(0x02)
        aenergy = reg[0]<<16+reg[1]<<8+reg[2]
        return aenergy
    
    def read_period(self):
        reg = self.read_16bit(0x07)
        period = reg[0]<<8 + reg[1]
        return period

    def close(self):
        self.spi.close()
        return


