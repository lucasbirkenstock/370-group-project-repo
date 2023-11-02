from neurosdk.scanner import Scanner
from neurosdk.sensor import Sensor
from neurosdk.brainbit_sensor import BrainBitSensor
from neurosdk.cmn_types import *

from tools.logging import logger
from em_st_artifacts import emotional_math 

from .lib_emotions_pipeline import make_pipeline_object

#doing all this a the "module level" in "Demo" server mode it will work fine :)

def on_sensor_state_changed(sensor, state):
    logger.debug('Sensor {0} is {1}'.format(sensor.Name, state))

def on_brain_bit_signal_data_received(sensor, data):
    logger.debug(data)

logger.debug("Create Headband Scanner")
gl_scanner = Scanner([SensorFamily.SensorLEBrainBit])
gl_sensor = None
logger.debug("Sensor Found Callback")

# Create emotionalmath object for calculating emotions from video
# might remove this line later and replace with some sort of call to lib_emotions_pipeline


def sensorFound(scanner, sensors):
    global gl_scanner
    global gl_sensor



    for i in range(len(sensors)):
        logger.debug('Sensor %s' % sensors[i])
        logger.debug('Connecting to sensor')
        gl_sensor = gl_scanner.create_sensor(sensors[i])
        gl_sensor.sensorStateChanged = on_sensor_state_changed
        gl_sensor.connect()
        gl_sensor.signalDataReceived = on_brain_bit_signal_data_received
        
        gl_scanner.stop()

        
        #################### Pipeline stuff: may need to be moved elsewhere later. ####################
        thePipeline = make_pipeline_object()
        data = []
        data = on_brain_bit_signal_data_received # change to whatever sensor data is, todo 
        thePipeline.push_data(data)
        thePipeline.process_data_arr()
        
        mind_data = thePipeline.read_average_mental_data()
        mind_data_list = thePipeline.read_mental_data_arr()

        # Average data
        print("Mind Data: {} {} {} {}".format(mind_data.rel_attention,
                                            mind_data.rel_relaxation,
                                            mind_data.inst_attention,
                                            mind_data.inst_relaxation))


        # All vals: probably unnecessary.
        for i in range(thePipeline.read_mental_data_arr_size()):
             print("{}: {} {} {} {}".format(i,
                mind_data_list[i].rel_attention,
                mind_data_list[i].rel_relaxation,
                mind_data_list[i].inst_attention,
                mind_data_list[i].inst_relaxation))
             
        
        
        #################### Pipeline stuff: may need to be moved elsewhere later.  ####################
        
        
        del gl_scanner

gl_scanner.sensorsChanged = sensorFound

logger.debug("Start scan")
gl_scanner.start()


def get_head_band_sensor_object():
    return gl_sensor

#print(gl_sensor.commands)

