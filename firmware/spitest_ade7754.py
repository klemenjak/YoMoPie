import spidev
import time

print "Try to setup SPI..."
spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz = 10000000

print "Try to send via SPI..."
while True:
    spi.xfer([0x3F])
    spi.readbytes(1)
print "Programm successfuly ended!"
