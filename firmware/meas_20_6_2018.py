# Measurement script for the IEEE paper

import YoMoPie
import csv, time
from datetime import datetime

def write_to_CSV(destination, data):
    datafile = open(destination, 'a')
    csv_writer = csv.writer(datafile)
    csv_writer.writerow(data)


yomo = YoMoPie.YoMoPie()  ##create a new YoMoPie Object
yomo.set_lines(1)  ##set number of lines to 1. Following commands will do the same
time.sleep(1)



yomo.sample_intervall = 0.1
a = time.time()
write_to_CSV('meas_20_6_2018/final_fancy_10Hz.csv','apparent apparent active ctime t')
while(1):
    sample = []
    b = time.time()
    time_diff = b - a
    energy = yomo.read_24bit(0x04)
    temp = yomo.read_24bit(0x05)
    sample.append(yomo.apparent_power_LSB * temp *  3600/time_diff)
    sample.append(yomo.apparent_power_LSB * temp*  3600/yomo.sample_intervall)
    sample.append(yomo.active_power_LSB * yomo.read_24bit(0x02) *  3600/time_diff)
    sample.append(time.ctime())
    sample.append(b)
    write_to_CSV('meas_20_6_2018/final_fancy_10Hz.csv',sample)
    a = b
    energy_old = energy
    duration = time.time() - b    
    if(yomo.sample_intervall-duration)>0:
        time.sleep(yomo.sample_intervall-duration)
