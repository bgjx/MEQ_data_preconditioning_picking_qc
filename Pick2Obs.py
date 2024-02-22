#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  6 10:12:53 2022

@author : ARHAM ZAKKI EDELO
@contact: edelo.arham@gmail.com
"""
import glob

print('''
Python code for collecting picks and generating NonLinLoc .obs input file 
  
      ''')
    
file_name=glob.glob('*.pick') #gather all the picking file

# set the output file name
output_format=input("Write the name for your gathered pick file: ")

# write the document
with open ((output_format + ".obs"), "w") as file_output: #handle the output file
    for i in file_name:
        split_lines=[line.split() for line in open(i,'r').readlines()]
        for line in split_lines:
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
            try:
                if (line[0] != '\n'):
                
                    # start writing the *.obs file
                    file_output.write("%s %s %s %s %s %s %8i %4s %11.8f %s %3.8f %3.1f %.5f %3.1f\n" % (line[0],line[1],line[2],line[3],line[4],line[5],int(line[6]),line[7],float(line[8]),line[9],float(line[10]), float(line[11]), float(line[12]), float(line[13])  )) # writing file according to the format
                else:
                    pass
            except Exception:
                pass
        file_output.write('\n')
    file_output.close()
    print('-----------  The code has run succesfully! --------------')