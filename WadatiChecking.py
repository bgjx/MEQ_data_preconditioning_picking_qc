#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 27 17:46:08 2022

@author : ARHAM ZAKKI EDELO
@contact: edelo.arham@gmail.com
"""

import pandas as pd;
import os,math, glob, sys
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict
from obspy import UTCDateTime

print('''
Python code for picking quality control using Wadati Diagram 

    
      ''')
    
def WadatiChecking(file):

    ## create dict holder for each station
    dict_holder= defaultdict(list)
    arrival=defaultdict(list)
    
    split_lines=[line.split() for line in open(file,'r').readlines()]
    for line in split_lines:

        ## Changing the station code (only if it is necessary)
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
            
        # Insert the respected values to the dictionary holder
        try:
            ## dict_holder={"STATION_NAME":[DATE, HH, MM_p, ATp, MM_s, ATs]}
            if line[2]== 'BHZ' or 'P' in line[4]:
                dict_holder[line[0]].append(line[6])
                dict_holder[line[0]].append(line[7][:2])
                dict_holder[line[0]].append(line[7][2:])
                dict_holder[line[0]].append(float(line[8]))
            elif line[2]== 'BHN' or line[2]== 'BHE' or 'S' in line[4]:
                dict_holder[line[0]].append(line[7][2:])
                dict_holder[line[0]].append(float(line[8]))
            else:
                pass
        except Exception:
            pass
            
    # Create another dictionary to be the dataframe
    arrival[0]= [v for v in list(dict_holder.keys())]
    for x in range(1,7):
        arrival[x] = [dict_holder[v][x-1] for v in list(dict_holder.keys())]
        
    # Convert Time to UTCDateTime Format
    ATp_UTC, ATs_UTC =[], []
    for i in range(0, len(arrival[5])):
    
        utc_p="{}-{:02d}-{:02d}T{:02d}:{:02d}:{:012.9f}". \
                            format(int(arrival[1][i][:4]),int(arrival[1][i][4:6]),int(arrival[1][i][6:]),int(arrival[2][i]),int(arrival[3][i]), float(arrival[4][i]))
        utc_s="{}-{:02d}-{:02d}T{:02d}:{:02d}:{:012.9f}". \
                            format(int(arrival[1][i][:4]),int(arrival[1][i][4:6]),int(arrival[1][i][6:]),int(arrival[2][i]),int(arrival[5][i]), float(arrival[6][i]))
        ATp_UTC.append(utc_p)
        ATs_UTC.append(utc_s)
    
    # calculate the lag time ts-tp
    for Tp,Ts in zip(ATp_UTC,ATs_UTC):
        TsTp=UTCDateTime(Ts, precision=9)- UTCDateTime(Tp, precision=9)
        arrival[7].append(float(TsTp))
        
    date_time= ATp_UTC[0]              ## time for plotting purpose only
    
    #create the dataframe
    df=pd.DataFrame.from_dict(arrival)
    df.columns=["Station", "Date", "Hour","Minutes_P", "P_Arr_Sec", "Minutes_S", "S_Arr_Sec", "Ts-Tp"]
    
    #For plotting purpose
    x=df['P_Arr_Sec']; y=df['Ts-Tp'];annot=df['Station']
    z=np.polyfit(x,y,1)
    p=np.poly1d(z)    
    print('\n\nFor Event ',date_time,' \n',df.to_string(index=False))
    fig,ax=plt.subplots()
    ax.scatter(x, y,  s=100, alpha=0.6, edgecolor='black', linewidth=1)
    ax.plot(x,p(x))
    ax.set_xlabel('P Arrival')
    ax.set_ylabel('Ts-Tp')
    plt.title("Events %s \n wadati trendline y=%.6fx+%.6f , Vp/Vs %5.3f"%(date_time,z[0],z[1], 1+z[0]))
    for i, label in enumerate(annot):
        plt.text(x[i], y[i], label)
    plt.show()
    return None

if __name__ == "__main__":
    file_name=glob.glob('*.pick') #gather all the picking file
    print("""
Before you run please choose the checking mode below:
    [1] Looping Mode   :QC will continue to the next pick when you close the plot window
    [2] Selection Mode :Choose spesific pick file by ID number, after closing the plot window you can choose other pick.
    """)
    prompt=int(input('Please type 1/2 to select the mode :'))
    if prompt != 1 and prompt != 2:
        sys.exit("You didn't choose the correct mode")
    # looping mode
    elif prompt == 1:
        for i in file_name:
            WadatiChecking(i)
    # selection mode
    elif prompt == 2:
        file_holder=defaultdict(int)
        for i in range(len(file_name)):
            file_holder[i]=file_name[i]
        print("There are {} picks here, please select one for QC:".format(len(file_name)))
        for v in range(len(file_holder)):
            print("[{}] {}".format(v, file_holder[v]))
           
        selection=0
        while type(selection) == int:
            try:
                selection = int(input("Which pick do you want to check [input the number or 'ctrl + c' to cancel]?:"))
                WadatiChecking(file_holder[selection])
            except Exception as e:
                print(e)
                break
    else:
        print("End the process of the program ....\n\n")
        pass
