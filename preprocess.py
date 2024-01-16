# Copyright (c) John Owusu Duah

#dependencies
import os
import re
from statistics import mean
import numpy as np
import pandas as pd
from io import StringIO

def read_extract_data(file_path, pwave_duration=5):
    '''
    Extracts seismic recordings of P-wave and PGA of S-waves from raw JapanQuakeData (K-NET) into an array

    Input: File path to K-NET seismograms downloaded from https://www.kyoshin.bosai.go.jp/
           Maximum Duration of P-wave 
    Output: Array of P-wave seismograms and PGA of S-waves
    '''
    #pwave start time in seconds
    pwave_starttime = 10
    pwave_duration = pwave_duration
    pwave_window = pwave_starttime*100, (pwave_starttime+pwave_duration)*100
    
    #define a variable to store PGA and Height of Station in first and last index
    #features are in between first and last index
    result = []

    #open file
    with open(file_path, 'r') as f:
        # collect header data
        line_no = 1
        counter = 0
        header_data = {}
        for line in f:
            counter += 1
            line = line.strip()
            columns = line.split()
            header_data["line_"+str(line_no)] = columns
            line_no += 1
            if counter == 15:
                break
            pass
    
        height = int(header_data["line_9"][-1])

        #collect acceleration data
        acc_data = []
        for line in f:
            counter += 1
            if (counter > 17):
                line = line.strip()
                columns = line.split()
                acc_data.append(columns)
                # remove nested list
                flat_acc_data = [int(val) for sublist in acc_data for val in sublist]
        
        #extract scale factor
        raw_scale = header_data['line_14'][2]
        num = int(re.search(r'^\d+', raw_scale).group())
        denom = int(re.search(r'\d+$', raw_scale).group())
        
        scale_factor = num/denom
        scaled_acc_data = [num * scale_factor for num in flat_acc_data]

        mean_acc_data = mean(scaled_acc_data)
        norm_acc_data = [(num - mean_acc_data)*0.01 for num in scaled_acc_data]

        selected_normacc_data = norm_acc_data[pwave_window[0]:pwave_window[1]]

        result.append(max(norm_acc_data))
        result.extend(selected_normacc_data)
        
        result.append(height)
    
    return result


#uncomment insert folder path to K-NET seismograms downloaded from https://www.kyoshin.bosai.go.jp/
#folder_path = 
#example: folder_path = "C:\\Users\\johno\\OneDrive\\Desktop\\Earthquake\\data\\JapanQuakeData-2000-2020\\2004-10-23-181200\\KNET\\"

#uncomment and insert folder prefix (i.e. path of path to location of folder downloaded from https://www.kyoshin.bosai.go.jp/)
#folder_prefix = 
#example: folder_prefix = "C:\\Users\\johno\\OneDrive\\Desktop\\Earthquake\\data\\JapanQuakeData-2000-2020\\"

#uncomment and insert subfolders in folder downloaded from https://www.kyoshin.bosai.go.jp/ representating seismic events
#suffixes = 
#example: suffixes = ["2004-10-23-183400\\KNET\\","2004-10-27-104000\\KNET\\","2005-07-23-163500\\KNET\\","2008-06-14-084300\\KNET\\","2008-07-24-002600\\KNET\\","2011-03-12-035900\\KNET\\","2011-03-15-223100\\KNET\\","2011-04-11-171600\\KNET\\","2011-04-12-140700\\KNET\\","2013-02-02-231700\\KNET\\","2013-02-25-162300\\KNET\\","2013-04-13-053300\\KNET\\","2014-11-22-220800\\KNET\\","2016-10-21-140700\\KNET\\","2018-09-06-030800\\KNET\\"]

# define list of files to process 
for suf in suffixes:
    folpath = folder_prefix+str(suf)
    os.chdir(folpath)
    all_files = os.listdir()
    regex = re.compile("(.*EW$)|(.*NS$)|(.*UD$)")
    match_files = []
    for file in all_files:
        if regex.match(file):
        #print(file)
            match_files.append(file)
        print(folpath, len(match_files))

    earthquake_data = []
    for file in match_files:
        file_path = folpath+str(file)
        data = read_extract_data(file_path, pwave_duration=5)
        earthquake_data.append(data)

    # saves P-wave and PGA of S-waves as a csv file
    df_data = pd.DataFrame(earthquake_data)
    df_data.to_csv("earthquake_data.csv")  