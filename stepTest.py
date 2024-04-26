from pylablib.devices import Attocube

# Initialization
anc300 = Attocube.ANC300("COM3")  # USB
anc300.enable_axis(axis='all', mode='stp')
anc300.set_voltage(1, 50) 
anc300.set_frequency(1, 1000)
anc300.update_available_axes()             

anc300.move_by(1, 1000)

# Close devices
anc300.close()
