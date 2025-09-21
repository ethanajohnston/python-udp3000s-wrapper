# Python Wrapper for UNI-T UDP3000S Series Power Supplies (UDP3305S &amp; UDP3305S-E)

**UNI-T Downloads:**
https://instruments.uni-trend.com/download?cate=33

**Installing UNI-T Drivers:**
1. Connect PSU USB B port to computer USB. 
2. Power on PSU. Device will show in the “Other Devices” tab as a device without a driver named UDP3000S or similar.
3. Download and install “Instrument Application” using all the default options.
4. Update the PSU to the latest firmware. In my case it was V1.17. Firmware is on downloads page. This might not be required for you.
5. Download UNI-T SDK and install the 2 drivers in the driver's folder. 
6. Restart computer

**Python Wrapper Usage:**
1. Ensure you have python 3 and VS-CODE installed on your computer.
2. Open folder attached to this task.
3. There is a wrapper I wrote for all the most useful commands to control and monitor the UNI-T power supply, a test script that demos the commands, and a script which scans for all SCPI devices and prints their resource address and ID.
4. Run the scan-for-devices.py. You should hear a beep from the PSU and see the resource address and device ID of PSU in the terminal output. You might get an error about not having the pyvisa library installed so install it with: pip install pyvisa. 
5. Open test.py and change the resource address in class init to the address of your PSU.
6. Run test.py. Fingers crossed it should work to control you UNI-T PSU. 
7. Enjoy! The commands should be pretty self explanatory.
