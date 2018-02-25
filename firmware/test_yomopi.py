import yomopie
import time

yomo = yomopi.YoMoPie()
##yomo.init_yomopie()

yomo.set_lines(1)

print yomo.do_n_measurements(5, 1)
        
yomo.close()    