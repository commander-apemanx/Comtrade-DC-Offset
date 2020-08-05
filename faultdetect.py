import math
import numpy as np
import cmath
import logging
#import statistics
LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(filename = "DCGUI.log",level = logging.INFO,format=LOG_FORMAT,filemode='w')
logger = logging.getLogger()

class FaultDetect:
    
    def analyze20ms_window(f,signal20ms,timesignal20ms):
        #f =  0#0 #50 #frequency you want in hertz
        #print("calculating DC value... which is of frequency:",f)
        pi = math.pi
        #print(" this is pi:" , pi)
        w = 2*pi*f #for dc this would be 0
        
        if f == 0: # when we only want the DC component which is special case of F =0
            #print("Calculation the DC component because f=", f)
            N = len(signal20ms) #get number of samples of my current Freq
            Xr = sum(signal20ms)/N
            #Xr = statistics.mean(signal20ms)
            #Xc = 0#(1/N)*sum(ImagI)
            Z = Xr#complex(Xr,Xc)
            #DCvalue,thRad = cmath.polar(Z) #value of the fundamental or DC and angle in rad
            thRad =0
            thetadeg = 0#thRad*180/pi
            #print("this is my DC values:" ,Xr,"more", Z, "more:", DCvalue)
            return Z,Xr,thetadeg,thRad,Xr #no square needed RMS of DC = DC 
        
        #print("omega:",w)
        ##DFT CALC Begins
        N = len(signal20ms) #get number of samples of my current Freq
        RealI = np.multiply(signal20ms, np.cos(w*timesignal20ms)) #sine is real for fourier function in this case
        ImagI = -1*np.multiply(signal20ms, np.sin(w*timesignal20ms)) # DFT - Discrete Fourier Transform
##        Xr = (math.sqrt(2)/N)*sum(RealI)#get RMS of the above filtered frequency
##        Xc = (math.sqrt(2)/N)*sum(ImagI)#get RMS of the above filtered frequency
        Xr = (2/N)*sum(RealI)# GET Signal Amplitude... needs sqrt to become RMS 2/sqrt(2) = sqrt(2)
        Xc = (2/N)*sum(ImagI)# GET Signal Amplitude... needs sqrt to become RMS
        ##DFT CALC ENDS
        #print("my complex nums ",Xr,"and ",Xc)
        Z = complex(Xr,Xc)
        #mag = abs(Z)
        #amp = math.sqrt(2)*abs(Z)
        #print("mag with abs:",mag)
        #print("mag with abs:",mags)
        PhasorAmplitude,thRad = cmath.polar(Z) #value of the fundamental or DC and angle in rad
        thetadeg = thRad*180/pi
        #print("Mag:",r,"theta",theta)
        #print(cmath.polar(Z))
        RMSValue = PhasorAmplitude/math.sqrt(2)
        return Z,RMSValue,thetadeg,thRad,PhasorAmplitude # complexValue, RMSofFundvalue, DegreeAngle,RadAngle,PhasorAmplitude

    def fl_detect_amp(Signal,NumSamples,AmpSens=150,start=1):
        #Get a Signal of some length and measue 2 values NumSamples apart and return the point where they are different....
        FoundFaultInd = []
        for index in range(len(Signal)-NumSamples):
            if (index == len(Signal)-NumSamples-1):
                FoundFaultInd.append(1)
                break
            AmpCheck = (abs(Signal[index+NumSamples])+abs(Signal[index+1+NumSamples]))/2 - (abs(Signal[index])+abs(Signal[index+1]))/2
            #logger.info("Amplitude check values %s", abs(AmpCheck))
            if (abs(AmpCheck) > AmpSens):
                FoundFaultInd.append(index+NumSamples)
                logger.info("Amplitude determined at: %s", index+NumSamples)
                break
        return FoundFaultInd


    
    def get_rate_of_change_vector(ISignal,Tsignal,res=1):
        roc = []
        for index in range(len(ISignal)-(res+1)): #round((samplesize/2))):
            deltax = Tsignal[index+res]-Tsignal[index]
            detaly = ISignal[index+res]-ISignal[index]
            roc.append(abs(detaly/deltax)) #newIR[index] #make roc vector
        return roc

    def fault_det_sens_ef(roc,neut,Isig,sens=1000,start=1,pickup=300):
        logger.info("Fault Detector called... with start value: %s", start)
        indpoints = []
        neutindpoints = []
        #get neutral current points to be higher that 300A...
        for sta in range(len(neut)-4):
            if (sta+start == len(roc)-4):
                break                                   
            if abs(neut[sta+start+1]) > abs(neut[sta+start]) and abs(neut[sta+start+3]) > pickup:# and abs(Isig[sta+start+2]) > abs(np.average(Isig[:sta+start])+pickup):
                neutindpoints.append(sta+start)
                #logger.info("Neut ROC First Index: %s", neutindpoints[0])
        if not neutindpoints:
            #print("No fault found on neutral")
            logger.warning("NO FAULT FOUND ON THE NEUTRAL PHASE!!!")
            neutindpoints.append(1)
        #logger.info("Neut ROC First Index: %s", neutindpoints[0])
            #return neutindpoints
        #else:
        #    return indpoints
        # get rate of change diffrence greater than sensitivity...
        for ind in range(len(roc)-4):
            if (ind+start == len(roc)-4):
                break
            if (abs(roc[ind+start+1]) > abs(roc[ind+start]+sens)) and (abs(roc[ind+start+2]) > abs(roc[ind+start]+sens)):# and (abs(roc[ind+start+3]) > abs(roc[ind+start]+sens)):# and (abs(roc[ind+start+4]) > abs(roc[ind+start]+sens)):
                indpoints.append(ind+start)#abs(roc[ind+1]))
                #logger.info("Neut ROC First Index: %s", neutindpoints[0])
            #logger.info("Current ROC First Index: %s", indpoints[0])   
        if not indpoints:
            #print("No fault found on the phase") 
            logger.warning("NO FAULT FOUND ON THE PHASE CURRENT!!!")
            indpoints.append(1)
            logger.info("There is no ROC index: %s", indpoints[0])
            return indpoints
        return_index = list(set(indpoints) & set(neutindpoints))#indpoints,neutindpoints # Returns a vetor with all index points where conditions where true
        return_index.sort()
        #print("sensitivity in FL detect:", sens)
        return return_index
    #fautl drop of def
    #def faultdis():
        
    

    
    def mag_and_theta_for_given_freq(f,IVsignal,Tsignal,samples):#f in hertz, IVsignal, Tsignal in numpy.array
        timegap = Tsignal[2]-Tsignal[3]
        pi = math.pi
        w = 2*pi*f
        Xr = []
        Xc = []
        Cplx = []
        mag = []
        theta = []
        #print("Calculating for frequency:",f)
        for i in range(len(IVsignal)-samples): 
            newspan = range(i,i+samples)
            timewindow = Tsignal[newspan]
            #print("this is my time: ",timewindow)
            Sig20ms = IVsignal[newspan]
            N = len(Sig20ms) #get number of samples of my current Freq
            RealI = np.multiply(Sig20ms, np.cos(w*timewindow)) #Get Real and Imaginary part of any signal for given frequency
            ImagI = -1*np.multiply(Sig20ms, np.sin(w*timewindow)) #Filters and calculates 1 WINDOW RMS (root mean square value).
            #calculate for whole signal and create a new vector. This is the RMS vector (used everywhere in power system analysis)
            Xr.append((math.sqrt(2)/N)*sum(RealI)) ### TAKES SO MUCH TIME
            Xc.append((math.sqrt(2)/N)*sum(ImagI)) ## these steps make RMS
            Cplx.append(complex(Xr[i],Xc[i]))
            mag.append(abs(Cplx[i]))
            theta.append(np.angle(Cplx[i]))#th*180/pi # this can be used to get Degrees if necessary
            #also for freq 0 (DC) id the offset is negative how do I return a negative to indicate this when i'm using MAGnitude or Absolute value
        return Cplx,mag,theta #mag[:,1]#,theta # BUT THE MAGNITUDE WILL NEVER BE zero
    #return mag,theta
