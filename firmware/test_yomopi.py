import yomopi
import time

yomo = yomopi.YoMoPi()
yomo.init_yomopi()

print yomo.read_temp()
print yomo.read_aenergy()
time.sleep(1)
        
yomo.close()    