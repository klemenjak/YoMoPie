import time
import math
import spidev
import sys
import RPi.GPIO as GPIO
from lib_nrf24 import NRF24

class YoMoPie:
    read = 0b00111111
    write = 0b10000000
    spi=0
    radio =0
    active_lines = 1
    debug = 1

    sample_intervall = 1
    max_f_sample = 10
    
    active_power_LSB= 0.000013292
    apparent_power_LSB= 0.00001024
    vrms_factor = 0.000047159
    irms_factor = 0.000010807

    #YoMoPie functions
	
    def __init__(self):
        self.spi=spidev.SpiDev()
        self.init_yomopie()
        return
         
    def init_yomopie(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(19,GPIO.OUT)
        self.spi.open(0,0)
        self.spi.max_speed_hz = 62500
        self.spi.mode = 0b01
        self.set_lines(self.active_lines)
        self.sampleintervall = 1
        return

    def set_lines(self, lines):
        if (lines != 1) and (lines != 3):
            print("Incompatible number of power lines")
            return
        else:
            self.active_lines = lines
            if self.active_lines == 3:
                self.write_8bit(0x0D, 0x3F)
                self.write_8bit(0x0E, 0x3F)
                self.set_measurement_mode(0x70)
            elif self.active_lines == 1:
                self.write_8bit(0x0E, 0x24)
                self.set_measurement_mode(0x10)
                self.write_8bit(0x0D, 0x24)
            return

    def enable_board(self):
        GPIO.output(19, GPIO.HIGH)
        return

    def disable_board(self):
        GPIO.output(19, GPIO.LOW)
        return
		
    def chip_reset(self):
        self.write_8bit(0x0A, 0x40)
        time.sleep(1)
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
    
    def write_16bit(self, register, value):
        self.enable_board()
        register = register | self.write
        self.spi.xfer2([register, value[0], value[1]])
        return

    def read_24bit(self, register):
        self.enable_board()
        register = register & self.read
        result = self.spi.xfer2([register, 0x00, 0x00, 0x00])[1:]
        dec_result = (result[0]<<16)+(result[1]<<8)+(result[2])
        return dec_result

    def get_temp(self):
        reg = self.read_8bit(0x08)
        temp = [time.time(),(reg-129)/4]
        return temp
        
    def get_laenergy(self):
        laenergy = [time.time(), self.read_24bit(0x03)]
        return laenergy

    def get_lappenergy(self):
    	lappenergy = [time.time(), self.read_24bit(0x06)]
    	return lappenergy

    def get_period(self):
        period = [time.time(), self.read_16bit(0x07)]
        return period

    def set_operational_mode(self, value):
    	self.write_8bit(0x0A, value)
    	return

    def set_measurement_mode(self, value):
    	self.write_8bit(0x0B, value)
    	return
    	
    def close_SPI_connection(self):
        self.spi.close()
        return 0
        
    def get_aenergy(self):
        aenergy = [time.time(), self.active_power_LSB * self.read_24bit(0x01) *  3600/self.sample_intervall]
        return aenergy

    def get_active_energy(self):
        aenergy =  [time.time(), self.active_power_LSB * self.read_24bit(0x02) *  3600/self.sample_intervall] 
        return aenergy

    def get_apparent_energy(self):
    	appenergy = [time.time(), self.apparent_power_LSB * self.read_24bit(0x05)*  3600/self.sample_intervall]
    	return appenergy
    	
    def get_vrms(self):
        if self.active_lines == 1:
            avrms = self.vrms_factor * [time.time(), self.read_24bit(0x2C)]
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
    '''
    def get_sample(self):
    	aenergy = self.get_aenergy()[1] *self.active_power_LSB
    	appenergy = self.get_appenergy()[1] *self.apparent_power_LSB
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
	'''
    
    def get_sampleperperiod(self, samplerate):
    	aenergy = self.get_aenergy()[1] *self.active_power_LSB * 3600/samplerate
    	appenergy = self.get_appenergy()[1] *self.apparent_power_LSB * 3600/samplerate
    	renergy = math.sqrt(abs(appenergy*appenergy - aenergy*aenergy))
    	vrms = self.get_vrms()[1]*self.vrms_factor
    	irms = self.get_irms()[1]*self.irms_factor
    	if self.debug:
    		print("Active energy: %f W, Apparent energy: %f VA, Reactive Energy: %f var" % (aenergy, appenergy, renergy))
    		print("VRMS: %f IRMS: %f" %(vrms,irms))
    	sample = []
    	sample.append(time.time())
    	sample.append(aenergy)
    	sample.append(appenergy)
    	sample.append(renergy)
    	sample.append(self.get_period()[1])
    	sample.append(vrms)
    	sample.append(irms)
    	return sample

    def do_n_measurements(self, nr_samples, samplerate, file):
        if (samplerate<1) or (nr_samples<1):
            return 0
        self.sample_intervall = samplerate
        samples = []
        for i in range(0, nr_samples):
            for j in range(0, samplerate):
                time.sleep(1)
            sample = self.get_sampleperperiod(samplerate)
            samples.append(sample)
            logfile = open(file, "a")
            for value in sample:
                logfile.write("%s; " % value)
            logfile.write("\n")
            logfile.close()
        return samples

    def do_metering(self, f_sample, file):
        if (f_sample > max_f_sample):
            print('Incompatible sampling frequency!')
            return 1
        if (file == ''):
            file = 'smart_meter_output.csv'
        for i in range(0,86400):
            sample = []
            sample.append(time.time())
            sample.append(i)
            sample.append(self.get_active_energy())
            sample.append(self.get_apparent_energy())
            data_file = open(file,'a')
            for value in sample:
                logfile.write("%s; " % value)
            logfile.write("\n")
	    ##print(sample)
            time.sleep(1/f_sample);
        return 0
'''
    def change_factors(self, active_f, apparent_f, vrms_f, irms_f):
	self.active_power_LSB = active_f
	self.apparent_power_LSB = apparent_f
	self.vrms_factor = vrms_f
	self.irms_factor = irms_f
	return
		
    def reset_factors(self):
    self.active_power_LSB= 0.000013292
    self.apparent_power_LSB= 0.00001024
    self.vrms_factor = 0.000047159
    self.irms_factor = 0.000010807
	return
	
	#NRF24 communication

    def init_nrf24(self):
	pipes = [[0xe7, 0xe7, 0xe7, 0xe7, 0xe7], [0xc2, 0xc2, 0xc2, 0xc2, 0xc2]]

	self.radio = NRF24(GPIO, self.spi)
	self.radio.begin(1, 13)
	self.radio.setPayloadSize(32)
	self.radio.setChannel(0x60)

	self.radio.setDataRate(NRF24.BR_2MBPS)
	self.radio.setPALevel(NRF24.PA_MIN)
	self.radio.setAutoAck(True)
	self.radio.enableDynamicPayloads()
	self.radio.enableAckPayload()
	self.radio.openWritingPipe(pipes[1])
	self.radio.openReadingPipe(1, pipes[0])
	self.radio.printDetails()
	return

    def write_nrf24(self, command):	
	message = []
	message = list(command)
	self.radio.write(message)
	print("Send: {}".format(message))
		
	if self.radio.isAckPayloadAvailable():
            pl_buffer = []
            self.radio.read(pl_buffer, self.radio.getDynamicPayloadSize())
            print(pl_buffer)
            print("Translating the acknowledgment to unicode chars...")
            string = ""
            for n in pl_buffer:
		if(n >= 32 and n <= 126):
                    string += chr(n)
		print(string)
	return
		
    def read_nrf24(self):
	print("Ready to receive data...")
	self.radio.startListening()
	pipe = [0]
	while not self.radio.available(pipe):
            time.sleep(1/100)
	receivedMessage = []
	self.radio.read(receivedMessage, self.radio.getDynamicPayloadSize())
		
	print("Translating the receivedMessage to unicode chars...")
	string = ""
	for n in receivedMessage:
            if (n >= 32 and n <= 126):
                string += chr(n)
            print("Our sensor sent us: {}".format(string))
        self.radio.stopListening()
	return
	'''