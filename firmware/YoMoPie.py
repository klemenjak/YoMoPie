import time
import math
import spidev
import sys
import RPi.GPIO as GPIO

class YoMoPie:
    read = 0b00111111
    write = 0b10000000
    spi=0
    active_lines = 1
    debug = 1

    sampleintervall = 1
    active_factor = 1
    apparent_factor = 1
    vrms_factor = 1
    irms_factor = 1

    def __init__(self):
        self.spi=spidev.SpiDev()
        return

    def init_yomopie(self):
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
            print "Wrong number of lines"
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
        dec_result = (result[0]<<8)+result[1]
        return dec_result

    def read_24bit(self, register):
        self.enable_board()
        register = register & self.read
        result = self.spi.xfer2([register, 0x00, 0x00, 0x00])[1:]
        dec_result = (result[0]<<16)+(result[1]<<8)+(result[0])
        return dec_result

    def get_temp(self):
        reg = self.read_8bit(0x08)
        temp = [time.time(),(reg-129)/4]
        return temp

    def get_aenergy(self):
        aenergy = [time.time(), self.read_24bit(0x02)]
        return aenergy

    def get_appenergy(self):
    	appenergy = [time.time(), self.read_24bit(0x05)]
    	return appenergy

    def get_period(self):
        period = [time.time(), self.read_16bit(0x07)]
        return period

    def set_opmode(self, value):
    	self.write_8bit(0x0A, value)
    	return

    def set_mmode(self, value):
    	self.write_8bit(0x0B, value)
    	return

    def get_sample(self):
    	aenergy = self.get_aenergy()[1] *self.active_factor
    	appenergy = self.get_appenergy()[1] *self.apparent_factor
    	renergy = math.sqrt(appenergy*appenergy - aenergy*aenergy)
    	if self.debug:
    		print"Active energy: %f W, Apparent energy: %f VA, Reactive Energy: %f var" % (aenergy, appenergy, renergy)
    		print"VRMS: %f IRMS: %f" %(self.get_vrms()[1]*self.vrms_factor,self.get_irms()[1]*self.irms_factor)
    	sample = []
    	sample.append(time.time())
    	sample.append(aenergy)
    	sample.append(appenergy)
    	sample.append(renergy)
    	sample.append(self.get_period()[1])
    	sample.append(self.get_vrms()[1]*self.vrms_factor)
    	sample.append(self.get_irms()[1]*self.irms_factor)
    	return sample

    def get_vrms(self):
    	if self.active_lines == 1:
    		avrms = [time.time(), self.read_24bit(0x2C)]
    		return avrms
    	elif self.active_lines == 3:
                vrms = []
                vrms.append(time.time())
    		vrms.append(self.read_24bit(0x2C))
    		vrms.append(self.read_24bit(0x2D))
    		vrms.append(self.read_24bit(0x2E))
    		return vrms
    	return 0

    def get_irms(self):
    	if self.active_lines == 1:
    		airms = [time.time(), self.read_24bit(0x29)]
    		return airms
    	elif self.active_lines == 3:
                irms = []
                irms.append(time.time())
    		irms.append(self.read_24bit(0x29))
    		irms.append(self.read_24bit(0x2A))
    		irms.append(self.read_24bit(0x2B))
    		return vrms
    	return 0


    def start_sampling(self, nr_samples, samplerate):
        if (samplerate<1) or (nr_samples<1):
            return 0
        self.sampleintervall = samplerate
        samples = []
        for i in range(0, nr_samples):

            for j in range(0, samplerate):
                time.sleep(1)

            samples.append(self.get_sample())
        return samples

    def close(self):
        self.spi.close()
        return
