#rate of change 
import matplotlib.pyplot as plt
import csv
import tkinter as tik
from tkinter import filedialog as fd
import numpy as np
import cmath
import math
import time
import re
import warnings
import logging
import faultdetect
import impedance_plot



LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(filename = "DCGUI.log",level = logging.INFO,format=LOG_FORMAT,filemode='w')
logger = logging.getLogger()


class DCRUNclass:
       
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
    
    def calc_impedance(self,newVvec,newIRvec,newINvec,t,intsample,k0=0.9,colour1='k',startplotsec=1,endplotsec=2):
        f=50
        logger.info("Calculating an Impedance")
        Fdt = faultdetect.FaultDetect
        R50filt,mag,theta = Fdt.mag_and_theta_for_given_freq(f,newVvec,t,intsample)
        In50filt,mag,theta = Fdt.mag_and_theta_for_given_freq(f,newINvec,t,intsample)
        IR50filt,mag,theta = Fdt.mag_and_theta_for_given_freq(f,newIRvec,t,intsample)
        if startplotsec > len(t) or endplotsec > len(t):
            startplotsec = 0
            endplotsec = len(t)
            print("Time values are out of bounds, reverting to default...")

        myrng = range(int(startplotsec),int(endplotsec))
        RR,XX = self.ptog(R50filt,IR50filt,In50filt,k0)

        f,ax = plt.subplots()#figsize=fig_size)#figure("Impedance Plot: ")#,colour1)
        myrng = range(0,len(IR50filt))
        #plt.scatter(XX,YY, color='red')#(R50filt)
        ax.plot(RR[myrng],XX[myrng], color=colour1,linewidth = 0.3)
        return ax
        #plt.show()

        #print("def in class with init has been called correctly")
        
    def calc_all_phase_faults(self,timevec,newIRvec,newIWvec,newIBvec,newINvec,sensitivity=1000,starting=1):
    # make which phase the fault is function
        Fdt = faultdetect.FaultDetect
        rocR = Fdt.get_rate_of_change_vector(newIRvec,timevec,1)#provide resolution to the rate of change 
        rocW = Fdt.get_rate_of_change_vector(newIWvec,timevec,1)#provide resolution to the rate of change 
        rocB = Fdt.get_rate_of_change_vector(newIBvec,timevec,1)
        faultindexR = Fdt.fault_det_sens_ef(rocR,newINvec,newIRvec,sensitivity,start = starting)#,start=8920)
        faultindexW = Fdt.fault_det_sens_ef(rocW,newINvec,newIWvec,sensitivity,start = starting)#,start=faultindex[0]+intsample*5)
        faultindexB = Fdt.fault_det_sens_ef(rocB,newINvec,newIBvec,sensitivity,start = starting)#,start=faultindex[0]+intsample*5)
        #plt.figure(3)
        #plt.plot(rocR)
        #plt.figure(4)
        #plt.plot(rocW)
        #plt.figure(5)
        #plt.plot(rocB)
        #returnF_index = list(set(faultindexR) & set(faultindexW) & set(faultindexB))
        #return returnF_index,returnF_index,returnF_index
        return faultindexR,faultindexW,faultindexB

    #def calc_amp_det(self,SignalIV,SamplesSize)
        #return faultindex
    
    def printoutDC_RMS(self,DCmag,amp,fund): #(r,amp,mag
        print("DC Value (A):",round(DCmag,2),"A")
        print("Amplitude of Phase (A): ",round(amp))
        print("Value of the Fundamental (A): ",round(fund))
        print("DC offset: ",round(DCmag/amp*100,2 ),"%")

    def __init__(self,whichcurr,sensitivity,start=4,firstorsecondset=0):
        #lass Preamble
        plt.close("all") #close all previous possible open plots...
        logger.info("Start index that was given to function: %s", start)

        #get second set
        
        
        #Get Fault - Call fault detector first
        Fdt = faultdetect.FaultDetect
        currtime = time.time()
        root = tik.Tk()
        fdc = 0 # 0 Hz component is the DC component
        """           
        phaseR = 6 #for red phase testing
        phaseW = 7 #for white phase testing
        phaseB = 8 #for blue phase testing
        phaseN = 9  #for neutral phase 
        """
        
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

        print(filename)
        #scaleval = []
        kV = 0
        R = []
        W = []
        B = []
        SynchV = []
        IR = []
        IW = []
        IB = []
        IN = []
        IR2 = []
        IW2 = []
        IB2 = []
        IN2 = []

        #SOME HAS BEEN DONE: Currently only works with standard files.. No detection of which values to use has been programmed
        with open(filenamecfg,'r') as csvfile1:
            logger.info("cfg has been opened...")
            cfgfile = [row for row in csv.reader(csvfile1, delimiter=',')]
            numberofchannels=int(np.array(cfgfile[1][0]))
            numberofAnalogchannels=re.sub("\D", "",cfgfile[1][1]) # Some recorings analog channels not dete4cte
            logger.info("Number of analog channels detected: %s" ,numberofAnalogchannels)
            analogAchannellistindex = []
            analogVchannellistindex = []
            for i in range(int(numberofAnalogchannels)): #numberofAnalogchannels:
                if  cfgfile[i+2][4] == 'A' or cfgfile[i+2][4] == 'kA':
                    print("Which phases current:",cfgfile[i+2][3])
                    logger.info("Currents have been searched for...")
                    #print("Which phases:",cfgfile[i+2][6])
                    analogAchannellistindex.append(int(cfgfile[i+2][0]))
                    
                if  cfgfile[i+2][4] == 'V' or cfgfile[i+2][4] == 'kV' or cfgfile[i+2][4] == 'kv':
                    if cfgfile[i+2][4] == 'kV' or cfgfile[i+2][4] == 'kv' or cfgfile[i+2][4] == 'KV':
                        kV = 1000
                    print("Which phases voltage:",cfgfile[i+2][3])
                    logger.info("Voltages have been searched for...")
                    #print("Which phases:",cfgfile[i+2][6])
                    analogVchannellistindex.append(int(cfgfile[i+2][0]))
                    
                else:
                    continue
            logger.info("analogAchannellistindex: %s", analogAchannellistindex)
            logger.info("analogVchannellistindex: %s", analogVchannellistindex)

            samplingfreq = float(np.array(cfgfile[numberofchannels+4][0]))
            numsamples = int(np.array(cfgfile[numberofchannels+4][1]))
            freq = float(np.array(cfgfile[numberofchannels+2][0]))
            intsample = int(samplingfreq/freq)
            scaleval = float(np.array(cfgfile[analogVchannellistindex[0]+1][5])) # +1 to get the next one on the list since we start from row 2.... and not 3 in a CFG file
            scalevalI = float(np.array(cfgfile[int(analogAchannellistindex[0]+1)][5])) #somewhat dynamic works if all the scaling values are the same for all phases
            #scaleval = np.array(cfgfile)[3]
            print('multiplier for V:',scaleval)
            print('multiplier for I:',scalevalI)
            print('SampFrq:',samplingfreq)
            print('NumSamples:',numsamples)
            print('Samples for Freq:', intsample)
            print('Freq:',freq)
        #TODO Calc how may samples in 20ms wave

        getsecondsetI=0
        logger.info("Which set?:%s",firstorsecondset)
        if firstorsecondset == 2:
            getsecondsetI=len(analogAchannellistindex)+1 #to get the second set dynamically if analog channel list is weird
            logger.info(analogAchannellistindex[0]+1+getsecondsetI)
            logger.info(analogAchannellistindex[1]+1+getsecondsetI)
            logger.info(analogAchannellistindex[2]+1+getsecondsetI)
            logger.info(analogAchannellistindex[3]+1+getsecondsetI)
        
        with open(filename,'r') as csvfile:
                plots = csv.reader(csvfile, delimiter=',')
                t = []
                for row in plots:
                    t.append(float(row[1])/1000000) # get us to sec
                    IR.append(float(row[analogAchannellistindex[0]+1+getsecondsetI]))
                    IW.append(float(row[analogAchannellistindex[1]+1+getsecondsetI]))
                    IB.append(float(row[analogAchannellistindex[2]+1+getsecondsetI]))
                    IN.append(float(row[analogAchannellistindex[3]+1+getsecondsetI]))
                    R.append(float(row[analogVchannellistindex[0]+1+firstorsecondset]))
                    W.append(float(row[analogVchannellistindex[1]+1+firstorsecondset]))
                    B.append(float(row[analogVchannellistindex[2]+1+firstorsecondset]))
                    #N.append(float(row[analogVchannellistindex[3]+1]))
                    
                    
        print("Amount of Current analogs:", len(analogAchannellistindex))
        logger.info("Amount of Current analogs:%s", len(analogAchannellistindex))
        
        #if there are 4 analogs.
        t = np.array(t)

        newR = np.array(R) * scaleval * kV
        newW = np.array(W) * scaleval * kV
        newB = np.array(B) * scaleval * kV
        #newN = np.array(N) * scaleval
        newIR = np.array(IR) * scalevalI
        newIW = np.array(IW) * scalevalI
        newIB = np.array(IB) * scalevalI
        newIN = np.array(IN) * scalevalI
        logger.info("All arrays have been added to the vectors...")
        #What if there are more than 4 A channels?
       
        elapsed = time.time() - currtime
        print(round(elapsed,ndigits=3),"s")

        # FAULT DETECT WITH AMPLITUDE
        logger.info("Detecting fault by amplitude...")
        Fdt = faultdetect.FaultDetect
        faultindexR_Amp = Fdt.fl_detect_amp(newIR,intsample)
        faultindexW_Amp = Fdt.fl_detect_amp(newIW,intsample)
        faultindexB_Amp = Fdt.fl_detect_amp(newIB,intsample)
        print ("This is Amplitude RED fault detect:",faultindexR_Amp[0])
        print ("This is Amplitude WHITE fault detect:",faultindexW_Amp[0])
        print ("This is Amplitude BLUE fault detect:",faultindexB_Amp[0])
        # FAULT DETECT WITH AMPLITUDE ENDS
        
        faultindexR,faultindexW,faultindexB = self.calc_all_phase_faults(t,newIR,newIW,newIB,newIN,sensitivity,start)
        logger.info("faultindexR:%s",faultindexR)
        logger.info("faultindexW:%s",faultindexW)
        logger.info("faultindexB:%s",faultindexB)
        if not faultindexR:
            print(" No fault found faultindexR please change sensitivity...")
            faultindexR.append(100)
        if not faultindexW:
            print(" No fault found faultindexW please change sensitivity...")
            faultindexW.append(100)
        if not faultindexB:
            print(" No fault found faultindexB please change sensitivity...")
            faultindexB.append(100)
            #exit()
        logger.info("First fault index have been assigned...")
# a test to ensure that we do not pass a larger value of the length of a signal to the fault detector in order to start detectin the second fault
        maxindex0 = max(faultindexR[0],faultindexW[0],faultindexB[0])+ intsample*20 # get somewhere futher than any detected fault
        if (maxindex0+intsample*20 > max(len(newIR),len(newIW),len(newIB))):
            maxindex0 = max(len(newIR),len(newIW),len(newIB)) - intsample -1
            logger.info("MaxIndex fault to search for next fault is longer than record lenght thus: %s", str(maxindex0))
        logger.info("Max Index singal length for second fault to start at: %s", maxindex0)

        #for a second fault
        faultindexR2,faultindexW2,faultindexB2 = self.calc_all_phase_faults(t,newIR,newIW,newIB,newIN,sensitivity,starting=maxindex0)
#        Coincide = list(set(faultindexR) & set(faultindexW) &set(faultindexB))
        no2faultdet = 0
        if not faultindexR2 or not faultindexW2 or not faultindexB2:
            no2faultdet = 1
            print("NO SECOND FAULT DETECTED...")
            logger.info("NO SECOND FAULT DETECTED...")
        logger.info("Second fault index have been assigned if if there was a second fault")
        #print("Index where all fault are the same for the first time:", Coincide[0])
        try:
            print("Number of Possible faults:",len(faultindexR),len(faultindexW),len(faultindexB))
            print("Fault index Red:  ",faultindexR[0])
            print("Fault index White:",faultindexW[0])
            print("Fault index Blue: ",faultindexB[0])
            #print("All co-incide: ",Coincide[0])
        except:
            print("Fault cannot be displayed!")#,indpoints[len(indpoints)-1])
            
        try:
            print("Number of Possible 2nd faults:",len(faultindexR2),len(faultindexW2),len(faultindexB2))
            print("Fault 2 index Red:  ",faultindexR2[0])
            print("Fault 2 index White:",faultindexW2[0])
            print("Fault 2 index Blue: ",faultindexB2[0])
            #print("All co-incide: ",Coincide[0])
        except:
            print("Fault 2 cannot be displayed!")#,indpoints[len(indpoints)-1])
            #faultindexR2[0] = 2
            #faultindexW2[0] = 2
            #faultindexB2[0] = 2
            

        
        warnings.filterwarnings("ignore",category=plt.cbook.mplDeprecation)
        if whichcurr == 'r' or whichcurr == 'w' or whichcurr == 'b':
            fig = plt.figure("Currents detected with rate of change and higher than 300A neutral")
            fig = plt.subplot(411)
            
            #print("THIS IS THE MIDDLE:",round((len(somerange)-1)/2))
            try:
                plotrange = range(faultindexR[0]-intsample,faultindexR[0]+intsample)
                fig = plt.plot(newIR[faultindexR[0]-intsample:faultindexR[0]+intsample],'r',linewidth=0.5)
                plt.axvline(x=round((len(plotrange)-1)/2))#faultindexR[0],color='k')
            except:
                print("I could not plot RED of the phases")
                logger.error("Could not plot RED Phase fault 1")
            fig = plt.subplot(412)    
            try:
                plotrange = range(faultindexW[0]-intsample,faultindexW[0]+intsample)
                fig = plt.plot(newIW[faultindexW[0]-intsample:faultindexW[0]+intsample],'g',linewidth=0.5)
                plt.axvline(x=round((len(plotrange)-1)/2))#faultindexR[0],color='k')
            except:
                print("I could not plot WHITE of the phases")
                logger.error("Could not plot WHITE Phase fault 1")
            fig = plt.subplot(413)
            try:
                plotrange = range(faultindexB[0]-intsample,faultindexB[0]+intsample)
                fig = plt.plot(newIB[faultindexB[0]-intsample:faultindexB[0]+intsample],'b',linewidth=0.5)
                plt.axvline(x=round((len(plotrange)-1)/2))#faultindexR[0],color='k')
            except:
                print("I could not plot BLUE of the phases")
                logger.error("Could not plot BLUE Phase fault 1")
                
            timegap = t[2]-t[3]
            print("Timegap between samples",timegap)

            if whichcurr == 'r':
                fig = plt.subplot(414)
                try:
                    fig = plt.plot(newIR,'r',linewidth=0.4)
                    fig = plt.axvline(x=faultindexR[0],color='k')#,'r')
                #plt.show()
                except:
                    print("No fault found on the RED phase. Pehaps not sensitive enough?")
                    
                userange= range(faultindexR[0],faultindexR[0]+intsample)
                ZZ,r,theta,thet,dcamp = Fdt.analyze20ms_window(fdc,newIR[userange],t[userange])
                ZZ2,mag2,theta,thet2,amp = Fdt.analyze20ms_window(freq,newIR[userange],t[userange])
                print("These are results for the RED Phase")
                self.printoutDC_RMS(r,amp,mag2)

            if whichcurr == 'w':
                fig = plt.subplot(414)
                try:
                    fig = plt.plot(newIW,'g',linewidth=0.4)
                    fig = plt.axvline(x=faultindexW[0],color='k')#,'r')
                except:
                    print("No fault found on the WHITE phase. Pehaps not sensitive enough?")
                    
                userange= range(faultindexW[0],faultindexW[0]+intsample)
                ZZ,r,theta,thet,dcamp = Fdt.analyze20ms_window(fdc,newIW[userange],t[userange])
                ZZ2,mag2,theta,thet2,amp = Fdt.analyze20ms_window(freq,newIW[userange],t[userange])
                print("These are results for the WHITE")
                self.printoutDC_RMS(r,amp,mag2)

            if whichcurr == 'b':
                fig = plt.subplot(414)
                try:
                    fig = plt.plot(newIB,'b',linewidth=0.4)
                    fig = plt.axvline(x=faultindexB[0],color='k')#,'r')
                except:
                    print("No fault found on the BLUE phase. Pehaps not sensitive enough?")
                    
                userange= range(faultindexB[0],faultindexB[0]+intsample)
                ZZ,r,theta,thet,dcamp = Fdt.analyze20ms_window(fdc,newIB[userange],t[userange])
                ZZ2,mag2,theta,thet2,amp = Fdt.analyze20ms_window(freq,newIB[userange],t[userange])
                print("These are results for the BLUE Phase")
                self.printoutDC_RMS(r,amp,mag2)
                
# now plot all the phases if one phase has a fault

        if whichcurr == 'all':
            #print("enters the for loop for ALLLL")
            fig2 = plt.figure("All Phases for the FIRST fault")
            userange= range(faultindexR[0],faultindexR[0]+intsample)
            ZZ,r,theta,thet,dcamp = Fdt.analyze20ms_window(fdc,newIR[userange],t[userange])
            ZZ2,mag2,theta,thet2,amp = Fdt.analyze20ms_window(freq,newIR[userange],t[userange])
            print("These are results for the RED Phase")
            self.printoutDC_RMS(r,amp,mag2)
            #print("Angle: ", theta)
##            plt.subplot(411)
##            try:
##                plt.plot(newIR[faultindexR[0]-intsample:faultindexR[0]+intsample],'r',linewidth=0.5)
##                #plt.axvline(x=faultindexR[0],color='k')
##            except:
##                print("I could not plot RED of the phases")

            userange= range(faultindexW[0],faultindexW[0]+intsample)
            ZZ,r,theta,thet,dcamp = Fdt.analyze20ms_window(fdc,newIW[userange],t[userange])
            ZZ2,mag2,theta,thet2,amp = Fdt.analyze20ms_window(freq,newIW[userange],t[userange])
            print("These are results for the WHITE")
            self.printoutDC_RMS(r,amp,mag2)
            #print("Angle: ", theta)
##            plt.subplot(412)    
##            try:
##                plt.plot(newIW[faultindexW[0]-intsample:faultindexW[0]+intsample],'g',linewidth=0.5)
##                #plt.axvline(x=faultindexW[0],color='k')
##            except:
##                print("I could not plot WHITE of the phases")
##            plt.subplot(413)
            userange= range(faultindexB[0],faultindexB[0]+intsample)
            ZZ,r,theta,thet,dcamp = Fdt.analyze20ms_window(fdc,newIB[userange],t[userange])
            ZZ2,mag2,theta,thet2,amp = Fdt.analyze20ms_window(freq,newIB[userange],t[userange])
            print("These are results for the BLUE Phase")
            self.printoutDC_RMS(r,amp,mag2)
            #print("Angle: ", theta)
##            try:
##                plt.plot(newIB[faultindexB[0]-intsample:faultindexB[0]+intsample],'b',linewidth=0.5)
##                #plt.axvline(x=faultindexB[0],color='k')
##            except:
##                print("I could not plot BLUE of the phases")
      
            #plt.subplot(414)
            try:
                plt.plot(newIR,'r',linewidth=0.3)
                plt.axvline(x=faultindexR[0],color='r')#,'r')
            except:
                print("No fault found on the RED phase. Pehaps not sensitive enough?")

            #plt.subplot(414)
            try:
                plt.plot(newIW,'g',linewidth=0.3)
                plt.axvline(x=faultindexW[0],color='g')#,'r')
            except:
                print("No fault found on the WHITE phase. Pehaps not sensitive enough?")
                      
            #plt.subplot(414)
            try:
                plt.plot(newIB,'b',linewidth=0.3)
                plt.axvline(x=faultindexB[0],color='b')#,'r')
            except:
                print("No fault found on the BLUE phase. Pehaps not sensitive enough?")

            #plt.show() 
#print("enters the for loop for ALLLL")
#-----------------------FAULT 2 -----------------------------------------------------------------
###################################################################################################                
            if no2faultdet == 0:
                fig3 = plt.figure("All Phases for the SECOND fault")
                userange= range(faultindexR2[0],faultindexR2[0]+intsample)
                ZZ,r,theta,thet,dcamp = Fdt.analyze20ms_window(fdc,newIR[userange],t[userange])
                ZZ2,mag2,theta,thet2,amp = Fdt.analyze20ms_window(freq,newIR[userange],t[userange])
                print("These are results for the RED Phase fault 2")
                self.printoutDC_RMS(r,amp,mag2)
##                plt.subplot(411)
##                try:
##                    plt.plot(newIR[faultindexR2[0]-intsample:faultindexR2[0]+intsample],'r',linewidth=0.5)
##                    #plt.axvline(x=faultindexR[0],color='k')
##                except:
##                    print("I could not plot RED of the phases fault 2")

                userange= range(faultindexW2[0],faultindexW2[0]+intsample)
                ZZ,r,theta,thet,dcamp = Fdt.analyze20ms_window(fdc,newIW[userange],t[userange])
                ZZ2,mag2,theta,thet2,amp = Fdt.analyze20ms_window(freq,newIW[userange],t[userange])
                print("These are results for the WHITE fault 2")
                self.printoutDC_RMS(r,amp,mag2)
                
##                plt.subplot(412)    
##                try:
##                    plt.plot(newIW[faultindexW2[0]-intsample:faultindexW2[0]+intsample],'g',linewidth=0.5)
##                    #plt.axvline(x=faultindexW[0],color='k')
##                except:
##                    print("I could not plot WHITE of the phases fault 2")
##                plt.subplot(413)
                userange= range(faultindexB2[0],faultindexB2[0]+intsample)
                ZZ,r,theta,thet,dcamp = Fdt.analyze20ms_window(fdc,newIB[userange],t[userange])
                ZZ2,mag2,theta,thet2,amp = Fdt.analyze20ms_window(freq,newIB[userange],t[userange])
                print("These are results for the BLUE Phase fault 2")
                self.printoutDC_RMS(r,amp,mag2)
##                try:
##                    plt.plot(newIB[faultindexB2[0]-intsample:faultindexB[0]+intsample],'b',linewidth=0.5)
##                    #plt.axvline(x=faultindexB[0],color='k')
##                except:
##                    print("I could not plot BLUE of the phases fault 2")
##          
##                plt.subplot(414)
                try:
                    plt.plot(newIR,'r',linewidth=0.3)
                    plt.axvline(x=faultindexR2[0],color='r')#,'r')
                except:
                    print("No fault found on the RED phase fault 2. Pehaps not sensitive enough?")

#                plt.subplot(414)
                try:
                    plt.plot(newIW,'g',linewidth=0.3)
                    plt.axvline(x=faultindexW2[0],color='g')#,'r')
                except:
                    print("No fault found on the WHITE phase fault 2. Pehaps not sensitive enough?")
                          
#                plt.subplot(414)
                try:
                    plt.plot(newIB,'b',linewidth=0.3)
                    plt.axvline(x=faultindexB2[0],color='b')#,'r')
                except:
                    print("No fault found on the BLUE phase fault 2. Pehaps not sensitive enough?")


        if whichcurr == 'impedance':
            print("calculating 3 Ph-G Impdances")
        #"""plot all three phase to ground impdances"""
            #plt.figure(3)
            redimp = self.calc_impedance(newR,newIR,newIN,t,intsample,k0=0.9,colour1='r',startplotsec=faultindexR[0],endplotsec=len(t))
            #plt.figure(4)
            whiteimp = self.calc_impedance(newW,newIW,newIN,t,intsample,k0=0.9,colour1='g',startplotsec=faultindexW[0],endplotsec=len(t))
            #plt.figure(5)
            blueimp = self.calc_impedance(newB,newIB,newIN,t,intsample,k0=0.9,colour1='b',startplotsec=faultindexB[0],endplotsec=len(t))
                
##### Below this comment is a copy and paste code of the above for when there is a second fault on the phase

                
                        
        elapsed = time.time() - currtime
        print(round(elapsed,ndigits=3),"s")
        logging.info("end of class, plots to be shown next")
        plt.show()
        label: end
        #end of class






