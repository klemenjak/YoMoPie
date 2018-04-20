# Measurement script for the IEEE paper

import YoMoPie
import csv, time

def write_to_CSV(destination, data):
    datafile = open(destination, 'a')
    csv_writer = csv.writer(datafile)
    csv_writer.writerow(data)


yomo = YoMoPie.YoMoPie()  ##create a new YoMoPie Object
yomo.set_lines(1)  ##set number of lines to 1. Following commands will do the same
time.sleep(1)

measurement_selector = 2

'''
Measurement #1: Measurement accuracy

Measurement #2: Maximal sampling freuency

Measurement #3: Measurement accuracy vs Sampling freuency

'''


if measurement_selector == 1:
    yomo.sample_intervall = 1
    a = time.time()
    write_to_CSV('/home/pi/Schreibtisch/YoMoPie/firmware/measurements_exp1.csv','t, d, a,b')
    while(1):
        sample = []
        b = time.time()
        time_diff = b - a
        sample.append(b)
        sample.append(time_diff)
        #sample.append(yomo.read_24bit(0x01))
        sample.append(yomo.active_power_LSB * yomo.read_24bit(0x02) *  3600/time_diff)
        sample.append(yomo.apparent_power_LSB * yomo.read_24bit(0x05)*  3600/time_diff)
        #write_to_CSV('/home/pi/Schreibtisch/YoMoPie/firmware/measurements_exp1x.csv',sample)
        a = b
        print(sample)
        duration = time.time() - b
        if(yomo.sample_intervall-duration)>0:
            time.sleep(yomo.sample_intervall-duration)


if measurement_selector ==2:
    yomo.sample_intervall = 0.001
    a = time.time()
    energy_old = 0
    write_to_CSV('exps/measurements_1000Hzv2.csv','t, d, a,b')
    while(1):
        sample = []
        b = time.time()
        time_diff = b - a
        sample.append(b)
        sample.append(time_diff)
        energy = yomo.read_24bit(0x04)
        #print(energy)
        #sample.append(yomo.apparent_power_LSB * (energy-energy_old) *  3600/time_diff)
        temp = yomo.read_24bit(0x05)
        sample.append(yomo.apparent_power_LSB * temp *  3600/time_diff)
        sample.append(yomo.apparent_power_LSB * temp*  3600/yomo.sample_intervall)
        write_to_CSV('exps/measurements_1000Hzv2.csv',sample)
        a = b
        energy_old = energy
        duration = time.time() - b
        #print(sample)
        if(yomo.sample_intervall-duration)>0:
			time.sleep(yomo.sample_intervall-duration)


if measurement_selector == 3:
    yomo.sample_intervall = 1
    a = time.time()
    write_to_CSV('/home/pi/Schreibtisch/YoMoPie/firmware/measurements_exp3.csv','t,d,a,r,p,r')
    while(1):
        sample = []
        b = time.time()
        time_diff = b - a
        sample.append(b)
        sample.append(time_diff)
        active = yomo.read_24bit(0x02)
        apparent = yomo.read_24bit(0x05)
        sample.append(active)
        sample.append(yomo.active_power_LSB * active *  3600/time_diff)
        sample.append(apparent)
        sample.append(yomo.apparent_power_LSB * apparent *  3600/time_diff)
        write_to_CSV('/home/pi/Schreibtisch/YoMoPie/firmware/measurements_exp3.csv',sample)
        a = b
        print(sample)
        duration = time.time() - b
        if(yomo.sample_intervall-duration)>0:
            time.sleep(yomo.sample_intervall-duration)
