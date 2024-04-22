import numpy as np
from pylablib.devices import Attocube
from nidaqmx import Task

# Initialization
anc300 = Attocube.ANC300("COM3")  # USB
anc300.enable_axis(axis='all', mode='stp')
task = Task()
task.ai_channels.add_ai_voltage_chan("Dev1/ai5")

# Parameters
voltages = np.zeros(2)

for i in range(1):
    anc300.move_by(1, 1)
    voltages[i] = task.read()

print(voltages)

# Close devices
anc300.close()
task.close()





