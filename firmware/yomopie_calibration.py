import YoMoPie
import time

yomo = YoMoPie.YoMoPie()  ##create a new YoMoPie Object

yomo.set_lines(1)  ##set number of lines to 1. Following commands will do the same

yomo.write_8bit(0x0B, 0x10)  ##MMODE 0x10
yomo.write_8bit(0x0D, 0x24)  ##WATMODE 0x24
yomo.write_8bit(0x0E, 0x24)  ##VAMODE 0x24
yomo.write_16bit(0x13, [0x00, 0xC8])   ##LINCYC 0d200
yomo.write_16bit(0x0F, [0x04, 0x00])   ##IRQEN 0x0400


pe=0.1

Cf = 0.000013171
CfVA= 0.000010045


CfV = 0.000047159
CfI = 0.000010807


watt = 1026.2
VA = 56.04 ##Vrms * Irms
    
'''
        Wh/LSB constant = (W * Accumulation time(s)/3600)/(LAENERGY/4)
        
        with
        
        Accumulation time(s) = LINCYC[15:0] * Line Period/(2*#of phase selected)
        
        and
        
        Line Period(s) = Period Register * 2.4 * 10^-6
        
        
        Simulated load with 100mVpp @ 50Hz on the input of the AMC1100 and the output of the CST1020:
        calculated Load: 61,778Vpp and 1,92App
        Ueff = 61,778/sqrt(2) = 43,68V
        Ieff = 1,92/sqrt(2) = 1,375A
        -> load = 59,30W/h
        
        -> Cf = 0.000014
        
        -> Cf(VRMS) = 0.000047159
        -> Cf(IRMS) = 0.000010807
        
        
        VRMS = VRMS0 + 64*VRMSOS
        VRMSOS = 1/64*(V1*VRMS2 - V2*VRMS1)/(V2-V1)
        
        IRMS2 = IRMS02 + 32768 * IRMSOS
        IRMSOS = 1/32768*(I12*IRMS22 - I22*IRMS12)/(I22-I12)
        
        
        
        Measurements 11.4.2018
        
        Cf(Wh/LSB) = 0.000013292   for 56.83W Lamp
        Cf(Wh/LSB) = 0.000013050   for 1025.2W Heater
        -> Cf(Wh/LSB) = 0.000013171
        
        
        Cf(VA/LSB) = 0.00001024   for 56.04VA Lamp
        Cf(VA/LSB) = 0.00000985   for 1025.2VA Heater
        -> Cf(VA/LSB) = 0.000010045
'''


##    print("--------------------------")
##    period = yomo.get_period()[1] * 0.0000024
##    print("Line Period = %f s" %(period))
##    linecycles = yomo.read_16bit(0x13)
##    print("Linecycles = %f" %(linecycles))
##    atime = linecycles*period/2
##    print("Accumulation time = %f s" %(atime))
##    laenergy = yomo.get_lappenergy()
##    print("LAPPENERGY = %d" %(laenergy[1]))
##    cf = VA*(atime/3600)/((laenergy[1]+10))
##    print("Wh/LSB const = %f" %(cf))
##    print("Wh/LSB const *1000 = %f" %(cf*1000))
##    print("--------------------------")
yomo.disable_board()
yomo.enable_board()
yomo.do_n_measurements(1000,5,"calibration_11_4_2018.log")
   
##    print("VRMS = %f V" %(yomo.get_vrms()[1]*CfV))
##    print("IRMS = %f A" %(yomo.get_irms()[1]*CfI))
##    print("Aenergy = %d" %yomo.read_24bit(0x01))
##    raen=yomo.read_24bit(0x02)
    ##print("RAenergy = %d" %raen)
##    print("VAenergy = %d" %yomo.read_24bit(0x04))
##    print("RVAenergy = %d" %yomo.read_24bit(0x05))
##    raven=yomo.read_24bit(0x05)
##    print("%f Watt/h, %f VA/h" %((raen*Cf*3600/pe), (raven*CfVA*3600/pe)))
    ##print("RVAenergy = %d" %raven)    
    ##print("%f VA/h" %(raven*CfVA*3600/pe))
    
   ## time.sleep(pe)    
        
yomo.close()   