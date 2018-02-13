import YoMoPie
import time

yomo = YoMoPie.YoMoPie()
##yomo.init_yomopie()

yomo.set_lines(1)
yomo.init_nrf24()

while True:
    yomo.get_sample()
    time.sleep(1)
        
yomo.close()    
