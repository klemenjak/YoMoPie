import time
import math
import spidev
import sys
import RPi.GPIO as GPIO 
 
class YoMoPi: 
    read = 0b00111111
    write = 0b10000000
    spi=0
    active_lines = 1
    debug = 1
	
    sampleintervall = 1
    active_factor = 1
    apparent_factor = 1
    
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
	self.set_lines(self.active_lines)
        return 
		
    def set_lines(self, lines):
	if (lines != 1) and (lines != 3):
            return
	else:
            self.active_lines = lines
            if self.active_lines == 3:
                self.write_8bit(0x0D, 0x3F)
                self.write_8bit(0x0E, 0x3F)
		self.set_mmode(0x70)
            elif self.active_lines == 1:
            		self.write_8bit(0x0D, 0x24)
            		self.write_8bit(0x0E, 0x24)	
            		self.set_mmode(0x10)				
            return
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
        return result[0]
        
    def read_16bit(self, register):
        self.enable_board()
        register = register & self.read
        result = self.spi.xfer2([register, 0x00, 0x00])[1:]
        return result[0]<<8+result[1]
        
    def read_24bit(self, register):
        self.enable_board()
        register = register & self.read
        result = self.spi.xfer2([register, 0x00, 0x00, 0x00])[1:]        
        return result[0]<<16+result[1]<<8+result[0]

    def read_temp(self):
        reg = self.read_8bit(0x08)
        temp = (reg-129)/4
        return temp
    
    def read_aenergy(self):
        aenergy = self.read_24bit(0x02)
        return aenergy
		
    def read_appenergy(self):
    	appenergy = self.read_24bit(0x05)
    	return appenergy
    
    def read_period(self):
        period = self.read_16bit(0x07)
        return period
		
    def set_opmode(self, value):
    	self.write_8bit(0x0A, value)
    	return

    def set_mmode(self, value):
    	self.write_8bit(0x0B, value)
    	return
		
    def get_sample(self):
    	aenergy = self.read_aenergy() *self.active_factor * 3600/self.sampleintervall
    	appenergy = self.read_appenergy() *self.apparent_factor * 3600/self.sampleintervall
    	renergy = math.sqrt(appenergy*appenergy - aenergy*aenergy)
    	if self.debug:
    		print"Active energy: %f W, Apparent energy: %f VA, Reactive Energy: %f var" % (aenergy, appenergy, renergy)
    		print"VRMS: %f IRMS: %f" %(self.vrms(),self.irms())
    	return
		
    def vrms(self):
    	if self.active_lines == 1:
    		avrms = self.read_24bit(0x2C)
    		return avrms
    	elif self.active_lines == 3:
    		vrms[0] = self.read_24bit(0x2C)
    		vrms[1] = self.read_24bit(0x2D)
    		vrms[2] = self.read_24bit(0x2E)
    		return vrms
    	return 0
		
    def irms(self):
    	if self.active_lines == 1:
    		airms = self.read_24bit(0x29)
    		return airms
    	elif self.active_lines == 3:
    		irms[0] = self.read_24bit(0x29)
    		irms[1] = self.read_24bit(0x2A)
    		irms[2] = self.read_24bit(0x2B)
    		return vrms
    	return 0
		
    def close(self):
        self.spi.close()
        return


