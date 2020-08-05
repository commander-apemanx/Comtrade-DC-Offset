#rate of change 
import matplotlib.pyplot as plt
import csv
import tkinter
from tkinter import filedialog as fd
import numpy as np
import cmath
import math
import time
import faultdetect


class impedance_plot:
    def ptog(self,Vsig,Isig,INsig,kfact):
        Vs = np.array(Vsig)
        Is = np.array(Isig) + np.array(INsig)*kfact
        Impedance = Vs/Is
        RealZ = np.array([x.real for x in Impedance])
        ImagZ = np.array([y.imag for y in Impedance])        
        return RealZ,ImagZ
    
    def phtoph(self,VsigA,VsigB,IsigA,IsigB):
        Vs = np.array(VsigA)- np.array(VsigB)
        Is = np.array(IsigA)- np.array(IsigB)
        Impedance = Vs/Is
        RealZ = np.array([x.real for x in Impedance])
        ImagZ = np.array([y.imag for y in Impedance])
        return RealZ,ImagZ

    def timecalc(self):
        elapsed = time.time() - currtime
        print(round(elapsed,ndigits=3),"s")
            
    def __init__(self):#,startplotsec,endplotsec):#can ad a range here that you need
        root = tkinter.Tk()
        Fdt = faultdetect.FaultDetect
        currtime = time.time()
        phaseVR = 2
        phaseVW = 3
        phaseVB = 4
        phaseR = 6 #for red phase testing
        phaseW = 7 #for white phase testing
        phaseB = 8 #for blue phase testing
        phaseN = 9

        f=50
        k0=0.9

        #filenamecfg = r"E:/Python_Practise/2019-10-21 13-54-38-482.CFG"
        #filename = r"E:/Python_Practise/2019-10-21 13-54-38-482.DAT"
        filenamecfg = fd.askopenfilename(title='Please select .cfg file')
        print(filenamecfg)
        #print(len(filenamecfg))
        if ".cfg" in filenamecfg:
            filename = filenamecfg.replace(".cfg",".dat")
        if ".CFG" in filenamecfg:
            filename = filenamecfg.replace(".CFG",".DAT")

        root.destroy()

        #filename = fd.askopenfilename(title='Please select .dat file')
        #filename = C:\Temp\;lasdjflajdf.cfg
        print(filename)
        #print(len(filename))
        scaleval = []
        t = []
        R = []
        W = []
        B = []
        SynchV = []
        IR = []
        IW = []
        IB = []
        IN = []


        #Currently only works with standard files.. No detection of which values to use has been programmed
        with open(filenamecfg,'r') as csvfile1:
            cfgfile = [row for row in csv.reader(csvfile1, delimiter=',')]
            numberofchannels=int(np.array(cfgfile)[1][0])
            samplingfreq = float(np.array(cfgfile)[numberofchannels+4][0])
            numsamples = int(np.array(cfgfile)[numberofchannels+4][1])
            freq = float(np.array(cfgfile)[numberofchannels+2][0])
            intsample = int(samplingfreq/freq)
            scaleval = float(np.array(cfgfile)[3][5])
            scalevalI = float(np.array(cfgfile)[8][5])
            #TODO neeeed to get number of samples and frequency and detect automatically
            #scaleval = np.array(cfgfile)[3]
            print('multiplier V :',scaleval)
            print('multiplier I :',scalevalI)
            print('SampFrq:',samplingfreq)
            print('NumSamples:',numsamples)
            print('Freq:',freq)
        #TODO Calc how may samples in 20ms wave
            
        with open(filename,'r') as csvfile:
            plots = csv.reader(csvfile, delimiter=',')
            for row in plots:
                t.append(float(row[1])/1000000) #get time from us to s
                R.append(float(row[phaseVR]))
                W.append(float(row[phaseVW]))
                B.append(float(row[phaseVB]))
                IR.append(float(row[phaseR]))
                IW.append(float(row[phaseW]))
                IB.append(float(row[phaseB]))
                IN.append(float(row[phaseN]))        


       
        t = np.array(t)
        print("time vector length in seconds:" , len(t)/samplingfreq)
        kV = 1000
        newR = np.array(R) * scaleval * kV
        newW = np.array(W) * scaleval * kV
        newB = np.array(B) * scaleval * kV
        newIR = np.array(IR) * scalevalI
        newIW = np.array(IW) * scalevalI
        newIB = np.array(IB) * scalevalI
        newIN = np.array(IN) * scalevalI

        startplotsec = float(input("where would you like the plot to start? :"))*samplingfreq
        endplotsec = float(input("where would you like the plot to end? :"))*samplingfreq
        print("Chosen:" , startplotsec,  "and: ", endplotsec)

        
        if startplotsec > len(t) or endplotsec > len(t):
            startplotsec = 0
            endplotsec = len(t)
            print("Time values are out of bounds, reverting to default...")

        myrng = range(int(startplotsec),int(endplotsec))


        In50filt,th,mag = Fdt.mag_and_theta_for_given_freq(f,newIN,t,intsample)

        R50filt,th,mag = Fdt.mag_and_theta_for_given_freq(f,newR,t,intsample)
        IR50filt,th,mag = Fdt.mag_and_theta_for_given_freq(f,newIR,t,intsample)
        W50filt,th,mag = Fdt.mag_and_theta_for_given_freq(f,newW,t,intsample)
        IW50filt,th,mag = Fdt.mag_and_theta_for_given_freq(f,newIW,t,intsample)
        B50filt,th,mag = Fdt.mag_and_theta_for_given_freq(f,newB,t,intsample)
        IB50filt,th,mag = Fdt.mag_and_theta_for_given_freq(f,newIB,t,intsample)
        
        #span = range(22360,22616) #hardcodes correct signal for ngewdi medupi
       
        elapsed = time.time() - currtime
        print(round(elapsed,ndigits=3),"s")

        RR,XX = self.ptog(R50filt,IR50filt,In50filt,k0)
        print("len:", len(RR), "and", len(XX))
        plt.figure("Impedance Plot RED-Ground")
        plt.plot(RR[myrng],XX[myrng], color='red',linewidth = 0.3)#(R50filt)
        RR,XX = self.phtoph(R50filt,W50filt,IR50filt,IW50filt)
        plt.figure("Impedance Plot RED-WHITE Phase")
        plt.plot(RR[myrng],XX[myrng], color='orange',linewidth = 0.3)#(R50filt)

        elapsed = time.time() - currtime
        print(round(elapsed,ndigits=3),"s")

        RR,XX = self.ptog(W50filt,IW50filt,In50filt,k0)

        plt.figure("Impedance Plot White-Ground")
        #myrng = range(0,len(IW50filt))
        #plt.scatter(XX,YY, color='red')#(R50filt)
        plt.plot(RR[myrng],XX[myrng], color='green',linewidth = 0.3)
        RR,XX = self.phtoph(W50filt,B50filt,IW50filt,IB50filt)
        plt.figure("Impedance Plot WHITE-BLUE Phase")
        plt.plot(RR[myrng],XX[myrng], color='cyan',linewidth = 0.3)#(R50filt)
        elapsed = time.time() - currtime
        print(round(elapsed,ndigits=3),"s")

        RR,XX = self.ptog(B50filt,IB50filt,In50filt,k0)
        plt.figure("Impedance Plot BLUE-Ground")
        plt.plot(RR[myrng],XX[myrng], color='blue',linewidth = 0.3)
        RR,XX = self.phtoph(B50filt,R50filt,IB50filt,IR50filt)
        plt.figure("Impedance Plot BLUE-RED PHASE")
        plt.plot(RR[myrng],XX[myrng], color='purple',linewidth = 0.3)#(R50filt)

        



        plt.show()

