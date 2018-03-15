import YoMoPie
import time

yomo = YoMoPie.YoMoPie()
##yomo.init_yomopie()

yomo.set_lines(1)

yomo.disable_board()
time.sleep(1)
yomo.enable_board()


yomo.write_8bit(0x0B, 0x10)  ##MMODE
yomo.write_8bit(0x0D, 0x24)  ##WATMODE
yomo.write_8bit(0x0E, 0x24)  ##VAMODE
yomo.write_16bit(0x13, [0x00, 0xC8])   ##LINCYC
yomo.write_16bit(0x0F, [0x04, 0x00])   ##IRQEN

##print(yomo.read_8bit(0x0B))
##print(yomo.read_8bit(0x0D))
##print(yomo.read_8bit(0x0E))
##print(yomo.read_16bit(0x13))
##print(yomo.read_16bit(0x0F))

while True:
##    periods = yomo.get_period()[1] * 0.0000024
##    print("Line Periods = %f" %(periods))
##    linecycles = yomo.read_16bit(0x13)
##    print("Linecycles = %f" %(linecycles))
##    atime = linecycles*periods/2
##    print("Accumulation time = %f" %(atime))
##    lappenergy = yomo.get_lappenergy()
##    print("LVAENERGY = %d" %(lappenergy[1]))
    ##cf = 61.9*(atime/3600)/(lappenergy[1]/4)
    ##print("KOEFFIZIENT = %f" %(cf))

  
   
##    print(yomo.get_vrms()[1])
##    print(yomo.get_irms()[1])
##    print("Aenergy = %d" %yomo.read_24bit(0x01))
##    print("RAenergy = %d" %yomo.read_24bit(0x02))
    print("LAenergy = %d" %yomo.read_24bit(0x03))
##    print("VAenergy = %d" %yomo.read_24bit(0x04))
##    print("RVAenergy = %d" %yomo.read_24bit(0x05))
##    print("LVAenergy = %d" %yomo.read_24bit(0x06))
    time.sleep(1)    
        
yomo.close()   