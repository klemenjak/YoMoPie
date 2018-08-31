# Servus!

Computational methods for the enhancement of energy efficiency rely on a measurement process with sufficient accuracy and number of measurements. Networked energy meters, energy monitors, serve as a vital link between the energy consumption of households and key insights that reveal strategies to achieve significant energy savings.
With YoMoPie, we propose a user-oriented energy monitor for the Raspberry Pi platform that aims to enable intelligent energy services in households. YoMoPie measures active as well as apparent power, stores data locally, and integrates a user-friendly Python library. Furthermore, the presented energy monitor allows users to run self-designed services in their home to enhance energy efficiency. Potential services are (but not limited to) residential demand response, immediate user feedback, smart meter data analytics, or energy disaggregation.

<!--- YoMoPie builds on [the work published in [1]](https://link.springer.com/article/10.1007%2Fs00450-014-0290-8#/page-1).
YoMoPie provides the following advancements:

* It doesn't suffer from a data update rate of 1 second
* It stores data locally
* It integrates a new measurement IC that allows poly-phase metering
* It builds on the Raspberry platform
* The YoMoPie Python package enables easy handling -->


## Research Paper on YomoPie

All design files and pieces of software are available free of charge. However, in case you use the PCB design, code, or other material for research purposes, we kindly ask you to cite our peer-reviewed research paper:

* *Title*: YoMoPie: A User-Oriented Energy Monitor to Enhance Energy Efficiency in Households
* *Authors*: Mr. Christoph Klemenjak, Mr. Stefan Jost and Dr. Wilfried Elmenreich
* *Conference*: 2018 IEEE Conference on Technologies for Sustainability (SusTech)

Recommended Citation:
```
@INPROCEEDINGS{klemenjak2018yomopie,
author={C. Klemenjak and S. Jost and W. Elmenreich},
booktitle={2018 IEEE Conference on Technologies for Sustainability (SusTech)},
title={Yo{M}o{P}ie: {A} User-Oriented Energy Monitor to Enhance Energy Efficiency in Households},
year={2018},
volume={},
number={},
pages={},
keywords={},
doi={},
ISSN={},
month={Nov}}
```

![](/Images/ypi_blos.JPG)


|                 | YoMoPie  |
| ------------- | -----:|
|Communication|  WiFi, Ethernet, RF |
|Measurement|  P, Q, S, I, U |
|Number of connections| 1 or 3 |
|Integrated relay |  yes |
|Sampling frequency|  tba. |
|Data update rate |  tba. |
|Power calculation|  Hardware |
|Open-Source|  yes |
|RaspberryPi-compatible|  yes  |
|Costs| approx. 50€  |

Beside a current and a voltage sensor, the board integrates an energy metering chip, the ADE7754. Our library is designed in a way to offer single-phase as well as multi-phase metering.

## Installation

The YoMoPie Python package is available on Python Package Index (PyPI), a repository of software for the Python programming language, and can be installed by issuing one command:

```python
pip3 install YoMoPie
```
Additionally, the entire source code and a manual can be obtained from our YoMoPie Github repository.

## Examples of use

After a successful installation process, the YoMoPie package is available system-wide and can be accessed by a simple import command:
```python
import YoMoPie as yomopie
yp = yomopie.YoMoPie()
```

During initialisation, the number of line conductors has to be set (single or polyphase metering):
```python
yomo.set_lines(1)
```

To test the operation, we recommend to call the function *do_n_measurements*. Based on the number of samples and the sampling period, the function will return first measurement values and saves it into the target file:
```python
yomo.do_n_measurements(number of samples, sampling period, target file)
```

Active power, apparent power, current, and voltage samples can be read with commands such as:
```python
[t, I] = yp.get_irms()
[t, U] = yp.get_vrms()
[t, P] = yp.get_active_energy()
[t, S] = yp.get_apparent_energy()
```
In the same vein, users can activate continuous data logging or perform a fixed amount of subsequent measurements:
```python
yp.do_metering()
yp.do_n_measurements(quantity, rate, file)
```

The operational mode (OPMODE) register defines the general configuration of the integrated measurement chip ADE7754. By writing to this register, A/D converters can be turned on/off, sleep mode can be activated, or a software chip reset can be triggered. For further information, we refer to the datasheet of the measurement chip.

```python
yp.set_operational_mode(OPMODE)
```



# YoMoPie Python package documentation
**[Imports](#imports)**<br>
**[Classvariables](#classvariables)**<br>
**[Methods](#methods)**<br>
*[-init](#init)*<br>
*[-init_yomopie](#init_yomopie)*<br>
*[-set_lines](#set_lines)*<br>
*[-enable_board](#enable_board)*<br>
*[-disable_board](#disable_board)*<br>
*[-chip_reset](#chip_reset)*<br>
*[-write_8bit](#write_8bit)*<br>
*[-read_8bit](#read_8bit)*<br>
*[-write_16bit](#write_16bit)*<br>
*[-read_16bit](#read_16bit)*<br>
*[-read_24bit](#read_24bit)*<br>
*[-get_temp](#get_temp)*<br>
*[-get_laenergy](#get_laenergy)*<br>
*[-get_lappenergy](#get_lappenergy)*<br>
*[-get_period](#get_period)*<br>
*[-set_operational_mode](#set_operational_mode)*<br>
*[-set_measurement_mode](#set_measurement_mode)*<br>
*[-close_SPI_connection](#close_SPI_connection)*<br>
*[-get_aenergy](#get_aenergy)*<br>
*[-get_active_energy](#get_active_energy)*<br>
*[-get_apparent_energy](#get_apparent_energy)*<br>
*[-get_sample](#get_sample)*<br>
*[-get_sampleperperiod](#get_sampleperperiod)*<br>
*[-get_vrms](#get_vrms)*<br>
*[-get_irms](#get_irms)*<br>
*[-do_n_measurements](#do_n_measurements)*<br>
*[-do_metering](#do_metering)*<br>
*[-change_factors](#change_factors)*<br>
*[-reset_factors](#reset_factors)*<br>
*[-init_nrf24](#init_nrf24)*<br>
*[-write_nrf24](#write_nrf24)*<br>
*[-read_nrf24](#read_nrf24)*<br>
**[OPMODE](#opmode)**<br>
**[MMODE](#mmode)**<br>

## Imports
YomoPie requires some additional libraries:

**time**: The time package is required to obtain timestamps.

**math**: YoMoPie requires the math lib for calculations such as reactive energy.

**spidev**: The YoMoPie integrates an energy monitor IC, which communicates via SPI to the RPi. To enable this communication, YoMoPie exploits the spidev lib.

**sys**: This module provides access to some variables used or maintained by the interpreter and to functions that interact strongly with the interpreter.

**RPi.GPIO**: In order to allow further extensions of the YoMoPie eco-system, our package integrates the RPi.GPIO. Also, the reset pin is controlled via GPIO.

**NRF24**: This package allows to utilize the RF module for 2.4 GHz communication.

```python
import time
import math
import spidev
import sys
import RPi.GPIO as GPIO
from lib_nrf24 import NRF24
```
## Class variables

To correctly access the internal registers of the energy monitor IC, several custom variables are required to adjust the register values.

* **read** and **write**: These variables hold the mask that defines the operational mode. Therefore, for reading a register the given address and the **read** variable are the inputs of a bitwise AND operation. On the other hand, for writing to a register the register address and the **write** variable are the inputs of a bitwise OR operation.

* **spi**, **active_lines** and **debug**: These variables hold the SPI object, save the number of active lines, and enable/disable the debug mode.

* **radio**: This object will be used for the RF communication and its functions.
* **sample interval** and **max_f_sample**: defines the time between two samples (with respect to the start_sampling method) in seconds and the maximum sampling frequency (with respect to the sampling error).
* **active_power_LSB**, **apparent_power_LSB**, **vrms_factor** and **irms_factor**: Convert register values to physical quantities and represent permanent conversion factors.

```python
read = 0b00111111
write = 0b10000000
spi=0
radio=0
active_lines = 1
debug = 1

sample_intervall = 1
max_f_sample = 10

active_power_LSB= 0.000013292
apparent_power_LSB= 0.00001024
vrms_factor = 0.000047159
irms_factor = 0.000010807
```

## Methods

In this Section, we describe every method of our  package. A description of function parameters and return values is given.

### __init__

**Description**: This method represents  the constructor and creates a new YoMoPie object.

**Parameters**: None.

**Returns**: Nothing.

```python
def __init__(self):
	self.spi=spidev.SpiDev()
	self.init_yomopie()
	return
```

### init_yomopie

**Description**: Initialises the YoMoPie object. Sets the GPIO mode, disables GPIO warnings and defines pin 19 as output. Also opens a new SPI connection via the SPI device (0,0), sets the SPI speed to 62500 Hz and sets the SPI mode to 1. Finally, the function set_lines is called to set the MMODE, WATMODE and VAMODE.

**Parameters**: None.

**Returns**: Nothing.

```python
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
```

### set_lines

**Description**: This function sets the number of active phases that will be measured.

**Parameters**:
* lines - Number of phases

**Returns**: Nothing.

```python
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
```

### enable_board

**Description**: Enables the board by pulling pin 19 to HIGH.

**Parameters**: None.

**Returns**: Nothing.

```python
def enable_board(self):
	GPIO.output(19, GPIO.HIGH)
	return
```

### disable_board

**Description**: Disables the board by pulling pin 19 to LOW.

**Parameters**: None.

**Returns**: Nothing.

```python
def disable_board(self):
	GPIO.output(19, GPIO.LOW)
	return
```

### chip_reset

**Description**: Resets the chip to the manufacturer settings

**Parameters**: None.

**Returns**: Nothing.

```python
def chip_reset(self):
	self.write_8bit(0x0A, 0x40)
	time.sleep(1);
	return
```		
### write_8bit    

**Description**: Writes 8 bit to the given address.

**Parameters**:

* register - 8 bit address of the register (see ADE7754 register table)

* value - 8 bit of value that will be written into the register

**Returns**: Nothing.

```python
def write_8bit(self, register, value):
	self.enable_board()
	register = register | self.write
	self.spi.xfer2([register, value])
	return
```

### read_8bit

**Description**: Reads 8 bit of data from the given address.

**Parameters**:
* register - 8 bit address of the register (see ADE7754 register table)

**Returns**: the 8 bit of data in the register as decimal

```python
def read_8bit(self, register):
	self.enable_board()
	register = register & self.read
	result = self.spi.xfer2([register, 0x00])[1:]        
	return result[0]
```

### write_16bit

**Description**: Writes 16 bit to the given address.

**Parameters**:

* register - 8 bit address of the register (see ADE7754 register table)

* value - 16 bit of value that will be written into the register

**Returns**: Nothing.

```python
def write_16bit(self, register, value):
	self.enable_board()
	register = register | self.write
	self.spi.xfer2([register, value[0], value[1]])
	return
```		

### read_16bit  

**Description**: Reads 16 bit of data from the given address.

**Parameters**:
* register - 8 bit address of the register (see ADE7754 register table)

**Returns**: the 16 bit of data in the register as decimal

```python
def read_16bit(self, register):
	self.enable_board()
	register = register & self.read
	result = self.spi.xfer2([register, 0x00, 0x00])[1:]
	dec_result = (result[0]<<8)+result[1]
	return dec_result
```

### read_24bit        

**Description**: Reads 24 bit of data from the given address.

**Parameters**:
* register - 8 bit address of the register (see ADE7754 register table)

**Returns**: the 24 bit of data in the register as decimal

```python
def read_24bit(self, register):
	self.enable_board()
	register = register & self.read
	result = self.spi.xfer2([register, 0x00, 0x00, 0x00])[1:]
	dec_result = (result[0]<<16)+(result[1]<<8)+(result[2])
	return dec_result
```

### get_temp

**Description**: Reads the temperature register (0x08).

**Parameters**: None.

**Returns**: A list [timestamp, temperature in °C]

```python
def get_temp(self):
	reg = self.read_8bit(0x08)
	temp = [time.time(),(reg-129)/4]
	return temp
```

### get_laenergy

**Description**: Reads the active energy register (0x03).

**Parameters**: None.

**Returns**: A list [timestamp, value of the register]

```python
def get_laenergy(self):
	laenergy = [time.time(), self.read_24bit(0x03)]
	return laenergy
```

### get_lappenergy

**Description**: Reads the apparent energy register (0x06).

**Parameters**: None.

**Returns**: A list [timestamp, value of the register]

```python
def get_lappenergy(self):
	lappenergy = [time.time(), self.read_24bit(0x06)]
	return lappenergy
```

### get_period   

**Description**: Reads the period register (0x07).

**Parameters**: None.

**Returns**: A list [timestamp, value of the register]

```python
def get_period(self):
       period = [time.time(), self.read_16bit(0x07)]
       return period
```

### set_operational_mode

**Description**: Sets the OPMODE. For more information see section OPMODE.

**Parameters**:
* value - 8 bit of data representing the OPMODE

**Returns**: Nothing.

```python
def set_operational_mode(self, value):
	self.write_8bit(0x0A, value)
	return
```

### set_measurement_mode

**Description**: Sets the MMODE. For more information see section MMODE.

**Parameters**:
* value - 8 bit of data representing the MMODE

**Returns**: Nothing.

```python
def set_measurement_mode(self, value):
	self.write_8bit(0x0B, value)
	return
```

### close_SPI_connection

**Description**: Closes the SPI connection.

**Parameters**: None.

Returns**: 0 if connection is closed.

```python
def close_SPI_connection(self):
	self.spi.close()
	return 0
```
### get_aenergy

**Description**: Reads the active energy register (0x01).

**Parameters**: None.

**Returns**: A list [timestamp, value of register converted to real value]

```python
def get_aenergy(self):
	aenergy = [time.time(), self.active_power_LSB * self.read_24bit(0x01) *  3600/self.sample_intervall]
	return aenergy
```
### get_active_energy

**Description**: Reads the active energy register (0x02) and resets the register value.

**Parameters**: None.

**Returns**: A list [timestamp, value of register converted to real value]

```python
def get_active_energy(self):
	aenergy =  [time.time(), self.active_power_LSB * self.read_24bit(0x02) *  3600/self.sample_intervall]
	return aenergy
```
### get_apparent_energy

**Description**: Reads the apparent energy register (0x05) and resets the register vlaue.

**Parameters**: None.

**Returns**: A list [timestamp, value of register converted to real value]

```python
def get_apparent_energy(self):
	appenergy = [time.time(), self.apparent_power_LSB * self.read_24bit(0x05)*  3600/self.sample_intervall]
	return appenergy
```
### get_sample

**Description**: Takes one sample and calculates the active energy, apparent energy, reactive energy, VRMS and IRMS.

**Parameters**: None.

**Returns**: A list of 7 elements [timestamp, active energy, apparent energy, reactive energy, period, VRMS, IRMS]

```python
def get_sample(self):
	aenergy = self.get_aenergy()[1] *self.active_factor
	appenergy = self.get_appenergy()[1] *self.apparent_factor
	renergy = math.sqrt(appenergy*appenergy - aenergy*aenergy)
	if self.debug:
		print"Active energy: %f W, Apparent energy: %f VA, Reactive Energy: %f var" %(aenergy, appenergy, renergy)
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
```

### get_vrms

**Description**: Reads the VRMS register depending.

**Parameters**: None.

**Returns**: A list of 2 elements [timestamp, Phase A VRMS] or 4 elements [timestamp, Phase A VRMS, Phase B VRMS, Phase C VRMS]

```python
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
```

### get_irms

**Description**: Reads the IRMS register.

**Parameters**: None.

**Returns**: A list of 2 elements [timestamp, Phase A IRMS] or 4 elements [timestamp, Phase A IRMS, Phase B IRMS, Phase C IRMS]

```python
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
```

### get_sampleperperiod

**Description**: Reads multiple register and returns the values adjusted to the sampling frequency. This function will be used in the do_n_measurements
 function.

**Parameters**:
* samplerate - the actual samplerate

**Returns**: A list of 7 elements [timestamp, active energy, apparent energy, reactive energy, period, VRMS, IRMS]

```python
def get_sampleperperiod(self, samplerate):
	aenergy = self.get_aenergy()[1] *self.active_factor * 3600/samplerate
	appenergy = self.get_appenergy()[1] *self.apparent_factor * 3600/samplerate
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
```

### do_n_measurements

**Description**: Takes *nr_samples* with sampling period *samplerate* and saves the measurements into the give file.

**Parameters**:

* nr_samples - this are the number of samples that will be taken, integer greater then 0
* samplerate - this is the time between each sample, integer greater then 0
* file - this will be the path and name of the file, where the date will be stored

**Returns**: A list of samples (each sample is a list of 7 elements)

```python
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
```

### do_metering

**Description**: Starts a sampling process and saves the data into a file.

**Parameters**:

* f_sample - the sampling frequency (<= 10, but if max_f_sample is changed, this value can be up to 100 with a higher error)
* file - this will be the path and name of the file, where the date will be stored. If this parameter is empty the data will be stored in "smart_meter_output.csv".

**Returns**: Nothing.

```python
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
```

### change_factors

**Description**: Changes the multiplication factors for the register values.

**Parameters**:

* active_f - this is the factor for the active energy calculation
* apparent_f - this is the factor for the apparent energy calculation
* vrms_f - this is the factor for the vrms calculation
* irms_f  this is the factor for the irms calculation

**Returns**: Nothing.

```python
def change_factors(self, active_f, apparent_f, vrms_f, irms_f):
	self.active_power_LSB = active_f
	self.apparent_power_LSB = apparent_f
	self.vrms_factor = vrms_f
	self.irms_factor = irms_f
	return
```

### reset_factors

**Description**: Resets the multiplication factors to the default values. The default values are calculated by our measurements with calibrated equipment.

**Parameters**: None.

**Returns**: Nothing.

```python
def reset_factors(self):
	self.active_power_LSB= 0.000013292
	self.apparent_power_LSB= 0.00001024
	self.vrms_factor = 0.000047159
	self.irms_factor = 0.000010807
	return
```

### init_nrf24

**Description**: Initializes the RF communication via the NRF24 chip.

**Parameters**: None.

**Returns**: Nothing.

```python
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
```

### write_nrf24

**Description**: Sends a message via the RF communication.

**Parameters**:
* command - the message that will be written via RF

**Returns**: Nothing.

```python
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
```

### read_nrf24

**Description**: Reads a message via the RF communication.

**Parameters**: None.

**Returns**: Nothing.

```python
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
```
## OPMODE
The operational mode (OPMODE) register defines the general configuration of the ADE7754 chip. For detailed information about the individual bits of this register we refer to [Table IX](https://github.com/klemenjak/YoMoPie/blob/master/Datasheets/ADE7754.pdf).


## MMODE
The configuration of period and peak measurements are defined by writing to the MMODE register (0x0B). For more information about the register we refer to [Table XII](https://github.com/klemenjak/YoMoPie/blob/master/Datasheets/ADE7754.pdf).
