import yomopi
import time

yomo = yomopi.YoMoPi()
yomo.init_yomopi()

print yomo.read_temp()
print yomo.read_aenergy()
print yomo.read_period()

yomo.write_8bit(0x0E, 0x24)

while True:
    print yomo.read_24bit(0x06)
    time.sleep(1)
time.sleep(3)       
        
yomo.close()    