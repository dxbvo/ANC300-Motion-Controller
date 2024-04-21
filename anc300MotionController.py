import numpy as np
# import matplotlib.pyplot as plt
from pylablib.devices import Attocube
from nidaqmx import Task

# Initialization
anc300 = Attocube.ANC300("COM3")  # USB
anc300.update_available_axes()

with Task() as task:
    task.ai_channels.add_ai_voltage_chan("Dev1/ai0")

# Parameters
sampleSize = 1.0  # Size of the sample surface in cm
stepSize = 0.1  # Step size for movement in cm
numSteps = int(sampleSize / stepSize)
voltages = np.zeros((numSteps, numSteps))

# Functions
def readVoltage():
    # Read voltage value using USB-6002
    with Task() as task:
        voltage = task.read()
    return voltage

# Instructions
for i in range(numSteps):
    for j in range(numSteps):
        x = i * stepSize
        y = j * stepSize
        anc300.move_to(x, y)
        voltage = readVoltage()
        voltages[i, j] = voltage

# Close devices
anc300.close()
task.close()

# # Plot grayscale image of the voltage values
# plt.imshow(voltages, cmap='gray', origin='lower', extent=(0, sample_size, 0, sample_size))
# plt.xlabel('X Position (cm)')
# plt.ylabel('Y Position (cm)')
# plt.title('Voltage Distribution')
# plt.colorbar(label='Voltage (V)')
# plt.show()



