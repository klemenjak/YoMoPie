import yomopi
import time

yomo = yomopi.YoMoPi()
yomo.init_yomopi()

yomo.set_lines(1)
print yomo.read_aenergy()
print yomo.read_temp()


while True:
    yomo.get_sample()
    time.sleep(1)
        
yomo.close()    