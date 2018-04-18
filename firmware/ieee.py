# Measurement script for the IEEE paper

import YoMoPie


yomo = YoMoPie.YoMoPie()  ##create a new YoMoPie Object
yomo.set_lines(1)  ##set number of lines to 1. Following commands will do the same


measruement_selector = 1

'''
Measurement #1: Measurement accuracy

Measurement #2: Maximal sampling freuency

Measurement #3: Measurement accuracy vs Sampling freuency

'''


if measruement_selector == 1:
    yomo.do_metering(1,'out.csv')

if measurement_selector ==2:
