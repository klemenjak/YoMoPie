## imports the YoMoPie library
import YoMoPie

## creates a new YoMoPie object
yomo = YoMoPie.YoMoPie()

## sets the YoMoPie to singlephase metering
yomo.set_lines(1)

## creates 5 samples with a period of 1 second and saves the data in "test_logfile.log"
yomo.do_n_measurements(5, 1, "test_logfile.log")

## closes the YoMoPie object        
yomo.close()    