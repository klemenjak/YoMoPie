import yomopi
import time

yomo = yomopi.YoMoPi()
yomo.init_yomopi()

yomo.set_lines(1)

yomo.get_sample()
print yomo.read_aenergy()
print yomo.read_temp()
        
yomo.close()    