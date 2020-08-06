# Comtrade-DC-Offset

How to run the program:

Run the Script GetDCOffset_GUI.py or relevant GUI file to start the program then click the buttons

This program is Essentially written to easily obtain the DC offset of a Power System Event Recorder (Disturbance Fault Recorders) on an ASCII COMTRADE file. This can be COMTRADE Files from any Relay, or device so long as it is ASCII and not the Binary format.

Lots of work is still planned and being done on this project and it is in its infancy. 
The end goal is for this program to analyse such a file, detect a Power System Transmission line fault and get the relevant Currents Voltages and Power from the Oscillographic recordings and populate the data on a Spreadsheet. 
Python - pandas libraries are to be included in the Future but as of now OpenpyXL and csv_read is used. 

All Fault detection and Mathematics happens in the Script: faultdetect.py
DCRUNClass is the script where the program essentially runs and executes. It is dirty and ugly programming but works to to the basic tasks. 
Lots of cleanup still needs to happen.

This Program used a Discrete Fourier Transform to obtain the necessary data. You can refer to this as Phasors or Fourier-RMS values
DC value is the value at 0Hz
50Hz value is the Fundamental frequency and can be 60Hz in the Americas
1-nth harmonics will be multiples of 50Hz. 



Future Plans include:
Output window formatted with readability
Complete Spreadsheet population of all results
better fault detection
Basic Impedance plots

