import spidev

print "Try to setup SPI..."
spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz = 62500
spi.mode = 0b01

print "Try to send via SPI..."
to_send = [0x1C, 0x00, 0x00]
print to_send
print spi.xfer2(to_send)
print "Programm successfuly ended!"
