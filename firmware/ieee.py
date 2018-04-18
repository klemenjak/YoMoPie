# Measurement script for the IEEE paper

import YoMoPie

import csv

def write_to_CSV(destination, data):
    datafile = open(destination, 'a')
    csv_writer = csv.writer(datafile)
    csv_writer.writerow(data)


yomo = YoMoPie.YoMoPie()  ##create a new YoMoPie Object
yomo.set_lines(1)  ##set number of lines to 1. Following commands will do the same


measruement_selector = 1

'''
Measurement #1: Measurement accuracy

Measurement #2: Maximal sampling freuency

Measurement #3: Measurement accuracy vs Sampling freuency

'''


if measruement_selector == 1:
    yomo.sample_intervall = 1
    a = time.time()
    write_to_CSV('measurements_exp1.csv','time_now, time_diff, active power, apparent power')
    while(1):
        sample = []
        b = time.time()
        time_diff = b - a
        sample.append(b)
        sample.append(time_diff)
        sample.append(yomo.active_power_LSB * yomo.read_24bit(0x02) *  3600/time_diff)
        sample.append(yomo.apparent_power_LSB * yomo.read_24bit(0x05)*  3600/time_diff)
        write_to_CSV('measurements_exp1.csv',sample)
        a = b
        energy_old = energy
        duration = time.time() - b
        if(yomo.sample_intervall-duration)>0:
            time.sleep(yomo.sample_intervall-duration)


if measurement_selector ==2:
    yomo.sample_intervall = 1
    a = time.time()
    energy_old = yomo.read_24bit(0x01)
    write_to_CSV('measurements_exp2.csv','time_now, time_diff, active power method 1,  active power method 2')
    while(1):
        sample = []
        b = time.time()
        time_diff = b - a
        sample.append(b)
        sample.append(time_diff)
        energy = yomo.read_24bit(0x01)
        sample.append(yomo.active_power_LSB * (energy-energy_old) *  3600/time_diff)
        sample.append(yomo.active_power_LSB * yomo.read_24bit(0x02) *  3600/time_diff)
        write_to_CSV('measurements_exp2.csv',sample)
        a = b
        energy_old = energy
        duration = time.time() - b
        if(yomo.sample_intervall-duration)>0:
			time.sleep(yomo.sample_intervall-duration)
