# A User-Oriented Energy Monitor to Enhance Energy Efficiency in Households

The YoMo project aims to empower people using low-cost open-hardware energy monitor.

With YoMoPie, we provide a user-oriented energy monitor based on the Raspberry Pi platform that aims to enable intelligent energy services in households.

The introduced energy monitor measures active as well as apparent power, stores data locally, and integrates an easy to use Python library. Furthermore, the presented energy monitor enables the execution of user-designed services to enhance energy efficiency in buildings and households.

Along with the design, possible applications that could run on top of our system such as residential demand response, immediate user feedback, smart meter data analytics, or energy disaggregation are discussed.

The YoMoPie builds on [the work published in [1]](https://link.springer.com/article/10.1007%2Fs00450-014-0290-8#/page-1). 
YoMoPie provides the following advancements:

* It doesn't suffer from a data update rate of 1 second
* It stores data locally
* It integrates a new measurement IC that allows poly-phase metering
* It builds on the Raspberry platform
* The YoMoPie Python package enables easy handling

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

Coming soon!

## Examples of use

In order to start using YoMoPie, all the user needs to do is importing the Python library:

```python
import YoMoPie as yomopi
```

After a successful import, the YoMoPie object can be created and initialised:

```python
yomo = yomopi.YoMoPie()
```

By setting the *set_lines' variable, the user can switch between single and multi-phase metering mode:

```python
yomo.set_lines(1)
```

To test the operation, we recommend to call the function *do_n_measurements*. Based on the number of samples and the sampling period, the function will return first measurement values:

```python
yomo.do_n_measurements(number of samples, sampling period)
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
*[-write_8bit](#write_8bit)*<br>
*[-read_8bit](#read_8bit)*<br>
*[-read_16bit](#read_16bit)*<br>
*[-read_24bit](#read_24bit)*<br>
*[-get_temp](#get_temp)*<br>
*[-get_aenergy](#get_aenergy)*<br>
*[-get_appenergy](#get_appenergy)*<br>
*[-get_period](#get_period)*<br>
*[-set_opmode](#set_opmode)*<br>
*[-set_mmode](#set_mmode)*<br>
*[-get_sample](#get_sample)*<br>
*[-get_vrms](#get_vrms)*<br>
*[-get_irms](#get_irms)*<br>
*[-do_n_measurements](#do_n_measurements)*<br>
*[-change_factors](#change_factors)*<br>
*[-reset_factors](#reset_factors)*<br>
*[-close](#close)*<br>
**[OPMODE](#opmode)**<br>
**[MMODE](#mmode)**<br>

## Imports
YomoPie requires some additional libraries:

**time**: The time package is required to obtain timestaps.

**math**: YoMoPie requires the math lib for calculations such as reactive energy.

**spidev**: The YoMoPie integrates an energy monitor IC, which communicates via SPI to the RPi. To enable this communication, YoMoPie exploits the spidev lib.

**sys**:

**RPi.GPIO**: In order to allow further extensions of the YoMoPie eco-system, our package integrates the RPi.GPIO. Also, the reset pin is controlled via GPIO.

```python
import time
import math
import spidev
import sys
import RPi.GPIO as GPIO
```
## Class variables

To correctly access the internal registers of the energy monitor IC, several custom variables are required to adjust the register values.

* **read** and **write**: These variables hold the mask that defines the operational mode. Therefore, for reading a register the given address and the **read** variable are the inputs of a bitwise AND operation. On the other hand, for writing to a register the register address and the **write** variable are the inputs of a bitwise OR operation.

* **spi**, **active_lines** and **debug**: These variables hold the SPI object, save the number of active lines, and enable/disable the debug mode.

* **sample interval** defines the time between two samples (with respect to the start_sampling method) in seconds
* **active_factor**, **apparent_factor**, **vrms_factor** and **irms_factor**: Convert register values to physical quantities and represent permanent conversion factors.

```python
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
       try:
			self.init_yomopie()
		except Error as err:
			print("Unexpected error:", format(err.args))
			return 0
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
       dec_result = (result[0]<<16)+(result[1]<<8)+(result[0])
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

### get_aenergy

**Description**: Reads the active energy register (0x02) and resets the register.

**Parameters**: None.

**Returns**: A list [timestamp, value of the register]

```python
def get_aenergy(self):
       aenergy = [time.time(), self.read_24bit(0x02)]
       return aenergy
```

### get_appenergy

**Description**: Reads the apparent energy register (0x05) and resets the register.

**Parameters**: None.

**Returns**: A list [timestamp, value of the register]

```python
def get_appenergy(self):
    appenergy = [time.time(), self.read_24bit(0x05)]
        return appenergy
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

### set_opmode

**Description**: Sets the OPMODE. For more information see section OPMODE.

**Parameters**:
* value - 8 bit of data representing the OPMODE

**Returns**: Nothing.

```python
def set_opmode(self, value):
    self.write_8bit(0x0A, value)
        return
```

### set_mmode

**Description**: Sets the MMODE. For more information see section MMODE.

**Parameters**:
* value - 8 bit of data representing the MMODE

**Returns**: Nothing.

```python
def set_mmode(self, value):
    self.write_8bit(0x0B, value)
        return
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
            print"Active energy: %f W, Apparent energy: %f VA, Reactive Energy: %f var"
        % (aenergy, appenergy, renergy)
            print"VRMS: %f IRMS: %f"
        %(self.get_vrms()[1]*self.vrms_factor,self.get_irms()[1]*self.irms_factor)
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

### do_n_measurements

**Description**: Takes *nr_samples* with sampling period *samplerate* and saves the measurements into the samples.log file.

**Parameters**:

* nr_samples - this are the number of samples that will be taken, integer greater then 0
* samplerate - this is the time between each sample, integer greater then 0

**Returns**: A list of samples (each sample is a list of 7 elements)

```python
def do_n_measurements(self, nr_samples, samplerate):
	if (samplerate<1) or (nr_samples<1):
		return 0
	self.sampleintervall = samplerate
	samples = []
	for i in range(0, nr_samples):
		for j in range(0, samplerate):
			time.sleep(1)
		sample = self.get_sample()
		samples.append(sample)
		logfile = open("samples.log", "a")
		for value in sample:
			logfile.write("%s, " % value)
		logfile.write("\n")
		logfile.close()
	return samples
```

### change_factors

**Description**: Changes the multiplication factors for the register values.

**Parameters**:

* apparent_f - this is the factor for the apparent energy calculation
* vrms_f - this is the factor for the vrms calculation
* irms_f  this is the factor for the irms calculation

**Returns**: Nothing.

```python
def change_factors(self, apparent_f, vrms_f, irms_f):
	self.apparent_factor = apparent_f
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
	self.apparent_factor = 1
	self.vrms_factor = 1
	self.irms_factor = 1
	return
```

### close

**Description**: Closes the SPI connection between the Raspberry Pi and the YoMoPie.

**Parameters**: None.

**Return**: Nothing.

```python
def close(self):
    self.spi.close()
    return
```

## OPMODE
The operational mode (OPMODE) register defines the general configuration of the ADE7754 chip. For detailed information about the individual bits of this register we refer to [Table IX](https://github.com/klemenjak/YoMoPie/blob/master/Datasheets/ADE7754.pdf).


## MMODE
The configuration of period and peak measurements are defined by writing to the MMODE register (0x0B). For more information about the register we refer to [Table XII](https://github.com/klemenjak/YoMoPie/blob/master/Datasheets/ADE7754.pdf).
