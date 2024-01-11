#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 27 17:46:08 2022

@author : ARHAM ZAKKI EDELO
@contact: edelo.arham@gmail.com
"""
import pandas as pd;
import os; import math; import glob;
import numpy as np
from collections import defaultdict
from obspy import UTCDateTime

print('''
Python code for generating catalog picking

  
      ''')
    

# initialize file input output
OutputName=input("Output catalog picking name(ex. 2023_10): " )
ID=int(input('Insert custom ID (4 digits integer ex. 1000): '))

# gather all pick file
file_name=glob.glob('*.pick') #gather all the picking file

# initialize dataframe header
df_all=pd.DataFrame(
    columns=["Event ID", "Station", "Date", "Hour", "Minutes_P","P_Arr_Sec", "+/-","I/E","Minutes_S","S_Arr_Sec","+/-","I/E","Ts-Tp","T0","P Travel","S Travel","Vp/Vs"]
    )

Index=[]
Count=0
for i in file_name:
    Count+=1
    
    ## create dict holder for each station data_collect
    dict_holder= defaultdict(list)
    arrival=defaultdict(list)
    split_lines=[line.split() for line in open(i, 'r').readlines()]
    for line in split_lines:
        ## Changing the station code (only if conversion needed) !!!!
        try:
            
            if   line[0]=='0AD13' or line[0]== 'ML01':
                line[0]='ML01'
            elif line[0]=='0A022' or line[0]== 'ML02':
                line[0]='ML02'
            elif line[0]=='0B4AC' or line[0]== 'ML03':
                line[0]='ML03'
            elif line[0]=='0AD26' or line[0]== 'ML04':
                line[0]='ML04'
            elif line[0]=='0AD1A' or line[0]== 'ML05':
                line[0]='ML05'
            elif line[0]=='0B4BC' or line[0]== 'ML06':
                line[0]='ML06'
            elif line[0]=='0B48F' or line[0]== 'ML07':
                line[0]='ML07'
            elif line[0]=='0AD16' or line[0]== 'ML08':
                line[0]='ML08'
            elif line[0]=='0AD14' or line[0]== 'ML09':
                line[0]='ML09'
            elif line[0]=='0B207' or line[0]== 'ML10':
                line[0]='ML10'
            elif line[0]=='0B4A5' or line[0]== 'ML11':
                line[0]='ML11'
            elif line[0]=='0B262' or line[0]== 'ML12':
                line[0]='ML12'
            elif line[0]=='0B492' or line[0]== 'ML13':
                line[0]='ML13'
            elif line[0]=='0AD17' or line[0]== 'ML14':
                line[0]='ML14'
            elif line[0]=='0B48E' or line[0]== 'ML15':
                line[0]='ML15'
            else:
                pass
        except Exception:
            pass
        
        # Change the first break polarity notation from c/d to +/-
        try:
            if line[5] == "c":
                line[5]="+"
            elif line[5]=="d":
                line[5]="-"
            else:
                line[5]="?"
        except Exception:
            pass
        
        # Capitalized the Impulsive and Emergent notation
        try:
            if line[3] == "i":
                line[3]="I"
            elif line[3]=="e":
                line[3]="E"
            else:
                line[3]="?"
        except Exception:
            pass
            
        # Insert the respected values to the dictionary holder
        try:
            ## dict_holder={"STATION_NAME":[DATE, HH, MM_p, ATp, AMPp, ONSETp, MM_s, ATs, AMPs, ONSETs, ID]}
            if line[2]== 'BHZ' or 'P' in line[4]:
                dict_holder[line[0]].append(line[6])
                dict_holder[line[0]].append(line[7][:2])
                dict_holder[line[0]].append(line[7][2:])
                dict_holder[line[0]].append(float(line[8]))
                dict_holder[line[0]].append(line[5])
                dict_holder[line[0]].append(line[3])
            elif line[2]== 'BHN' or line[2]== 'BHE' or 'S' in line[4]:
                dict_holder[line[0]].append(line[7][2:])
                dict_holder[line[0]].append(float(line[8]))
                dict_holder[line[0]].append(line[5])
                dict_holder[line[0]].append(line[3])
                dict_holder[line[0]].append(ID)
                Index.append(Count)
            else:
                pass
        except Exception:
            pass
    
    # Insert the respected values to the dictionary holder
    arrival[0]= [dict_holder[v][-1] for v in list(dict_holder.keys())]
    arrival[1]= [v for v in list(dict_holder.keys())]
    for x in range(2, 12):
        arrival[x] = [dict_holder[v][x-2] for v in list(dict_holder.keys())]
        
    # Convert Time to UTCDateTime Format
    ATp_UTC, ATs_UTC =[], []
    for i in range(0, len(arrival[5])):
    
        utc_p="{}-{:02d}-{:02d}T{:02d}:{:02d}:{:012.9f}". \
                            format(int(arrival[2][i][:4]),int(arrival[2][i][4:6]),int(arrival[2][i][6:]),int(arrival[3][i]),int(arrival[4][i]), float(arrival[5][i]))
        utc_s="{}-{:02d}-{:02d}T{:02d}:{:02d}:{:012.9f}". \
                            format(int(arrival[2][i][:4]),int(arrival[2][i][4:6]),int(arrival[2][i][6:]),int(arrival[3][i]),int(arrival[8][i]), float(arrival[9][i]))
        ATp_UTC.append(utc_p)
        ATs_UTC.append(utc_s)
    # calculate the lag time ts-tp
    for Tp,Ts in zip(ATp_UTC,ATs_UTC):
        TsTp=UTCDateTime(Ts, precision=9)- UTCDateTime(Tp, precision=9)
        arrival[12].append(float(TsTp))
    ID+=1
    
    # Create the dataframe using Pandas
    df=pd.DataFrame.from_dict(arrival)
    df.columns=["Event ID", "Station", "Date", "Hour", "Minutes_P","P_Arr_Sec", "+/-","I/E","Minutes_S","S_Arr_Sec","+/-","I/E","Ts-Tp"]
    
    #calculate T0
    origin=[]
    x=df['P_Arr_Sec']; y=df['Ts-Tp'];
    z=np.polyfit(x,y,1)
    T0= (-1*z[1])/z[0]
    
    #calculate the vpvs
    VpVs, TTP=[], []
    for i in list(arrival[5]):
        origin.append(T0)
        vpvs=1+z[0]
        VpVs.append(vpvs)
        TTp=i-T0           
        TTP.append(TTp)
    #update the dataframe and concate the long version of dataframe
    df["T0"]=origin
    df["P Travel"]=TTP
    df["S Travel"] = df["Ts-Tp"]+df["P Travel"]
    df["Vp/Vs"]=VpVs
    df_all=pd.concat([df_all,df], ignore_index=True)
    df_all.index=Index
df_all.to_excel(OutputName+'.xlsx')
print('-----------  The code has run succesfully! --------------')
