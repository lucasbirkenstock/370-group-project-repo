import neurosdk
from neurosdk.scanner import Scanner
from neurosdk.sensor import Sensor
from neurosdk.brainbit_sensor import BrainBitSensor
from neurosdk.cmn_types import *


# https://sdk.brainbit.com/
scanner = Scanner([SensorFamily.SensorLEBrainBit])
# sensor = scanner.create_sensor(sensInfo)

