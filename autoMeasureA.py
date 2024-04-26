from pylablib.devices import Attocube
from nidaqmx import Task
from PIL import Image

import time
import math
import numpy as np

# Variables Size of chip & lens scope
chip_length = 1         #   1 mm
chip_height = 1         #   1 mm
lens_scope = 0.1        # 100 um
# Constants for 1 um steps
step_size_1um = 0.001   #   1 um
step_volt_1um = 44      # 44 V
# Each step takes 5 ms (Frequency = 200 Hz)
step_volt = step_volt_1um
f = 200
T = 1/f
continue_meas = 'y'
chip_ready = 'n'

# initialise the Attocube
atc = Attocube.ANC300("COM3")          # USB Connection solidified

# Axes prepared for Programm
atc.enable_axis(axis='all', mode='stp') # X, Y & Z Axes enabled
# Voltages for steps set 
atc.set_voltage(1, step_volt)
atc.set_voltage(2, step_volt)

# Set Frequencies for x- & y-axis
atc.set_frequency(1, f)
atc.set_frequency(2, f)

# Positions of all 3 Axes are updated
atc.update_available_axes()             

# NI measurements prepared
task = Task()

# Calculates how many steps need to be taken to cover the whole length & height of the silicon chip
steps_length = int(chip_length/lens_scope)
steps_height = int(chip_height/lens_scope)
amount_steps = int(lens_scope/step_size_1um)

print(steps_length)
print(steps_height)
print(amount_steps)

# starting Point 
x_starting_point = int((chip_length/2)/step_size_1um)  # Number of steps from center position to starting point x-Axis
y_starting_point = int((chip_height/2)/step_size_1um)  # Number of steps from center position to starting point y-Axis

# Matrix for Measurements
voltages = np.zeros((steps_length+1, steps_height+1))  

# Get Frequency & Voltage from x- & y-axis
x_voltage = atc.get_voltage(1)
y_voltage = atc.get_voltage(2)
x_freq = atc.get_frequency(1)
y_freq = atc.get_frequency(2)


# Set to starting point
atc.move_by(1, x_starting_point)
time.sleep(T*(x_starting_point+10))
atc.move_by(2, y_starting_point)
time.sleep(T*(y_starting_point+10))

# Beginning of Measurement
while continue_meas == 'y':

    # Makes sure the chip is in place

        # Move one step to the right, measure voltage until you reach at the end of the chip (lengthwise)
        # Ends while when all the way down the chip
        for y_step in range(steps_height+1):

            for x_step in range(steps_length):
                # Measures Voltage
                with Task() as task:
                    task.ai_channels.add_ai_voltage_chan("Dev1/ai5")
                    voltages[x_step, y_step] = task.read()
                print(voltages[x_step, y_step])
                # X-Axis Movement
                atc.move_by(1, -amount_steps)
                time.sleep(T*(amount_steps+10))
        
            # Final measurement in the Line => otherwise last measurement not covered
            with Task() as task:
                task.ai_channels.add_ai_voltage_chan("Dev1/ai5")
                voltages [(steps_length - 1), y_step] = task.read()
                
            # Go back to Original X Coordinate
            atc.move_by(1, (amount_steps*steps_length))
            time.sleep(T*(amount_steps+10)*steps_length)

            # New Y Coordinate for next samples
            atc.move_by(2, -amount_steps)
            time.sleep(T*(amount_steps+10))
    
        # Goes back to starting point
        atc.move_by(2, amount_steps*(steps_height+1))
        time.sleep(T*(amount_steps+10)*(steps_length+1))

    # Do another Measurement

# Close everything
atc.close()         # All Axes are closed
task.close()        # Task closed

# Convert the matrix to a NumPy array for easier manipulation
meas_volt_array = np.array(voltages)

# Normalize the values in the matrix between 0 and 1
min_value = meas_volt_array.min()
max_value = meas_volt_array.max()
normalized_meas_volt = (meas_volt_array - min_value) / (max_value - min_value)

# Scale the normalized values to the range 0-255
scaled_meas_volt = (normalized_meas_volt * 255).astype(np.uint8)

# Repeat each value for a 20x20 block
scaled_meas_volt_repeat = np.repeat(np.repeat(scaled_meas_volt, 20, axis=0), 20, axis=1)

# Create a new grayscale image from the scaled matrix
chip_volt_image = Image.fromarray(scaled_meas_volt_repeat, mode="L")

time.sleep(0.5)
     
print(x_voltage)                 
print(y_voltage)
print(x_freq)                 
print(y_freq)

# Save or display the image
chip_volt_image.save("grayscale_measured_voltages_on_chip.png")
chip_volt_image.show()



