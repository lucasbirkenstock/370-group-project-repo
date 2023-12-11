from neurosdk.scanner import Scanner
from neurosdk.sensor import Sensor
from neurosdk.brainbit_sensor import BrainBitSensor
from neurosdk.cmn_types import *
from time import sleep
from tools.logging import logger
from em_st_artifacts import emotional_math 
# support classes in em_st_artifacts > utils 
from em_st_artifacts.utils import support_classes
from em_st_artifacts.utils import lib_settings

from .lib_emotions_pipeline import make_pipeline_object

# This code sets up a sensor scanner, connects to discovered sensors, and defines callback functions to handle sensor events and data.

#doing all this a the "module level" in "Demo" server mode it will work fine :)

def on_sensor_state_changed(sensor, state):
    logger.debug('Sensor {0} is {1}'.format(sensor.Name, state))

# Variable to store brain data
#my_data = []

thePipeline = make_pipeline_object()

# This function CONSTANTLY invokes when the headband is connected and the video is playing
def on_brain_bit_signal_data_received(sensor, data):
    # Copy the information from 'data' to the global variable 'my_data'
    #global my_data
    #logger.debug(data)
    #my_data.append(data)
    #print("test123")
    #print(my_data)

    raw_channels = [support_classes.RawChannels]
    for sample in data: 
        left_bipolar = sample.T3-sample.O1
        right_bipolar = sample.T4-sample.O2
        raw_channels.append(support_classes.RawChannels(left_bipolar, right_bipolar))

    thePipeline.push_data(raw_channels)
    thePipeline.process_data_arr()

    if not thePipeline.calibration_finished():
        print(f'Artifacted: {thePipeline.is_both_sides_artifacted()}')
        print(f'Calibration percents: {thePipeline.get_calibration_percents()}')
    else :
        print(f'Artifacted: {thePipeline.is_artifacted_sequence()}')
        print(f'Mental data: {thePipeline.read_mental_data_arr()}')
        print(f'Spectral data: {thePipeline.read_spectral_data_percents_arr()}')
    print(data)


logger.debug("Create Headband Scanner")
gl_scanner = Scanner([SensorFamily.SensorLEBrainBit])
gl_sensor = None
logger.debug("Sensor Found Callback")

def sensorFound(scanner, sensors):
    global gl_scanner
    global gl_sensor



    for i in range(len(sensors)):

        data = []
        logger.debug('Sensor %s' % sensors[i])
        logger.debug('Connecting to sensor')
        gl_sensor = gl_scanner.create_sensor(sensors[i])
        gl_sensor.sensorStateChanged = on_sensor_state_changed
        gl_sensor.connect()
        gl_sensor.signalDataReceived = on_brain_bit_signal_data_received
        gl_scanner.stop()

        
        #################### Pipeline stuff: may need to be moved elsewhere later. ####################
        
        if gl_sensor.is_supported_command(SensorCommand.StartSignal()):
            gl_sensor.exec_command(SensorCommand.StartSignal)
            print("Start signal")
            thePipeline.start_calibration()
            sleep(120)
            gl_sensor.exec_command(SensorCommand.StopSignal)

        
        
        break
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
