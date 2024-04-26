import numpy as np
from pylablib.devices import Attocube
from nidaqmx import Task
import matplotlib.pyplot as plt
import time
from tqdm import tqdm

# Parameters
xRange = 50 # in steps
yRange = 50 # has to be even integer in order to return to starting position
voltages = np.zeros([yRange, xRange])
V = 44 # 44V -> 1um
f = 1000

# Initialization
anc300 = Attocube.ANC300("COM3")  # USB
anc300.enable_axis(axis='all', mode='stp')
anc300.set_voltage(1, V) 
anc300.set_voltage(2, V)
anc300.set_frequency(1, f)
anc300.set_frequency(2, f)
anc300.update_available_axes()             
task = Task()
task.ai_channels.add_ai_voltage_chan("Dev1/ai5")

startTime = time.time()

for y in tqdm(range(yRange), desc="Progress", unit="row"):
    direction = 1 if y % 2 == 0 else -1

    for x in range(xRange):
        anc300.move_by(1, direction)
        time.sleep(0.05)
        voltages[y, x] = task.read()
    
    anc300.move_by(2, 1)

# Execution time
endTime = time.time()
excTime = endTime - startTime
print("Execution time:", round(excTime, 2), "seconds")

# Move back to starting position
anc300.move_by(2, -yRange)

# Close devices
anc300.close()
task.close()

# flip every second row because of negative direction
voltages[1::2] = voltages[1::2, ::-1]

plt.figure(1)
plt.imshow(voltages, cmap = 'gray', origin = 'lower')
plt.title(f'Voltage map \n (Execution time: {round(excTime, 2)}s, {V}V, {f}Hz)')
plt.xlabel('x')
plt.ylabel('y')
plt.show()