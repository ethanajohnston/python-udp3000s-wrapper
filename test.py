from udp3000s import UDP3000S
import time

psu = UDP3000S("USB0::0x0483::0x5740::ADP3423060093::INSTR") # Change this to your PSUs SCPI resource address
print(psu.idn())

# CH1 basic setup
psu.set_voltage(1, 5.000)  # Channel 1
psu.set_current(1, 0.500)  # Channel 1

# OVP/OCP config per channel if desired
# psu.set_ovp_level(1, 5.500)
# psu.set_ovp_state(1, True)
# psu.set_ocp_level(1, 2.100)
# psu.set_ocp_state(1, True)

# Enable output
psu.set_output(1, True)
time.sleep(1)

# Readback
v, i = psu.get_v_i(1) # Channel 1
print(f"CH1: {v:.3f} V, {i:.3f} A")

time.sleep(5)

psu.set_output(1, False) # Channel 1
psu.close()
