# Comtrade-DC-Offset

How to run the program
Run the Script GetDCOffset_GUI2.1.py or relevant GUI file to start the program then click the buttons

This program is Essentially written to easily obtain the DC offset of a Power System Event Recorder (Disturbance Fault Recorders) on an ASCII COMTRADE file. This can be COMTRADE Files from any Relay, or device so long as it is ASCII and not the Binary format.

Lots of work is still planned and being done on this project and it is in its infancy. 
The end goal is for this program to analyse such a file, detect a Power System Transmission line fault and get the relevant Currents Voltages and Power from the Oscillographic recordings and populate the data on a Spreadsheet. 
Python - pandas libraries are to be included in the Future but as of now OpenpyXL is used. 

All Fault detection and Mathematics happens in the Script: faultdetect.py
DCRUNClass is the script where the program essentially runs and executes. It is dirty and ugly programming but works to to the basic tasks. 
Lots of cleanup still needs to happen.





Future Plans include:
Output window formatted with readability
Basic Impedance plots

