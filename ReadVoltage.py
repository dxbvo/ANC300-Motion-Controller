from nidaqmx import Task

with Task() as task:
    task.ai_channels.add_ai_voltage_chan("Dev1/ai5")
    voltage = task.read()

print(voltage)