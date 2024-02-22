#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 15 19:32:03 2022

@author : ARHAM ZAKKI EDELO
@contact: edelo.arham@gmail.com
"""
from obspy import UTCDateTime, Stream, read, Trace
import os, glob, subprocess, sys
from pathlib import PurePath, Path

print('''
Python code for waveform trimming 

Before you run this program, make sure you have changed all the path and set the trimming duration correctly      
      ''')
# Global Parameters
#============================================================================================
# trimming duration parameter
before_pick = 5              #  5 seconds before the earlier pick
after_pick  = 25             # 25 seconds after the earlier pick

# List of functions 
#============================================================================================
def Trim(st, AddTime, bef, aft):
    for tr in st:
        OrgTm=tr.stats.starttime
        OrgTm+=AddTime
        tr.trim(OrgTm - bef, OrgTm + aft) ## starttime 7 seconds before origin time, and 15 second after origin time , this values can be changed liberally
        #tr.taper(0.05,type='hann',max_length=None, side='both') # tapering and detrending (optional)
    return st

def WriteSeis(SaveDir,st2,SavePath, Event_ID):
    foldername=os.path.join(SaveDir, str(Event_ID))
    if not os.path.exists(foldername):
        os.makedirs(foldername)
    for tr in st2:
        s=tr.stats
        FilesName=f"{int(SavePath[0:8]):8d}_{int(SavePath[9:13]):04d}_{int(SavePath[14:16]):02d}_{s.station}_{s.channel}_{Event_ID:04d}.mseed"
        tr.write(os.path.join(foldername,FilesName),format='mseed')
    return s
# End of functions 
#============================================================================================

if __name__ == "__main__":
    prompt=str(input('Please type yes/no if you had changed the path :'))
    if prompt != 'yes':
        sys.exit("Ok, please correct the path first!")
    else:
        print("Process the program ....\n\n")
        pass

    # initialize input and output path
    Input1   = Path(r"E:\SEML\DATA PICKING MEQ\DATA PICK 2023\PICK 2023 01")              # pick file as the time reference
    Input2   = Path(r"E:\SEML\DATA RAW MEQ\RAW DATA 2023\2023 01")                        # raw data mseed
    Save     = Path(r"E:\SEML\DATA TRIMMING\EVENT DATA TRIM\2023\2023 01")                # trimmed data destination
    ID_start = int(input('Please input the event 4 digits ID to startwith (ex: 2000):'))

    # gather all picks file as the time reference
    FilesName=glob.glob(os.path.join(Input1, "*.pick"), recursive=True)
    FilesName.sort()
    EventCounter=0
    for i in range(len(FilesName)):
        EventCounter+=1

        # initialize savepath
        SavePath=Path(FilesName[i]).stem
        DateStamp=SavePath.split()[0]

        # set trimming start reference time
        OriginTime=SavePath[-8:].split()
        Hours=OriginTime[0]; Hour=Hours[:2]; Minute=int(Hours[-2:]); second=int(OriginTime[1])
        AddTime=(Minute*60)+second

        # start merging and trimming procedure  
        for (EntryPath, DirChild, FileName) in os.walk(Input2):
            if (Path(EntryPath).stem)[:-4] == DateStamp:
                try:
                    WorkDir= PurePath(os.path.join(EntryPath,Hour))
                    WaveNames=glob.glob(os.path.join(WorkDir,'*.mseed'))
                except Exception:
                    continue
                try:
                    st=Stream()
                    for v in range(len(WaveNames)):
                        st+=read(WaveNames[v])
                    sst=st.copy()
                    sst=Trim(sst,AddTime, before_pick, after_pick)
                    NewSeis=WriteSeis(Save, sst, SavePath, ID_start)
                    print(f"{EventCounter} | Trimming Event {ID_start}.....")
                except Exception as e:
                    print(e)
                    continue
            else:
                continue
        
        ID_start+=1
                
    print("Merging and trimming procedure has been done succesfully ")
    print('-----------  The code has run succesfully! --------------')