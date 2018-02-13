import yomopi
import time

yomo = yomopi.YoMoPi()
yomo.init_yomopi()

yomo.set_lines(1)

print yomo.start_sampling(5, 1)
        
yomo.close()    