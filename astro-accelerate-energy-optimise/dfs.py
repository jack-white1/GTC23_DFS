#Energy readings
import subprocess
import pandas as pd
import datetime
import time
import numpy as np
import csv
from io import StringIO
import json

def calculate_slice_energy(filename, start_time, end_time):		# Code from Emily Widjaja
    power_data = pd.read_csv(filename)
    power_data.columns = ['timestamp', 'power', 'gpu_clock', 'mem_clock', 'utilization.gpu', 'utilization.memory', 'temperature.gpu']

    """
    Multiply power consumption with the difference in time between readings 
    Time (s)   Power (W)
    time1      power1
    time2      power2

    Energy = power2 * (time1 - time2)   (J)
    """

    total_energy = 0
    time_format = '%Y/%m/%d %H:%M:%S.%f'
    prev = False
    for idx, row in power_data.iterrows():
        # Turn into timestamp
        curr = datetime.datetime.strptime(row['timestamp'], time_format)
        if prev != False:
            diff = curr-prev
            energy = power_data['power'][idx-1] * diff.microseconds * 1e-6
            if (curr < end_time) and (curr > start_time) :
                total_energy += energy
        prev = curr

    return total_energy



def energy_test(low_freq, high_freq, bfloat):
    filepath = '.'
    filename = 'powerfile'
    t = datetime.datetime.now()
    filename = filename + t.strftime('_%Y-%m-%d_%H-%M-%S')
    sampling_period = 15    #ms

    command_str = ["nvidia-smi", "--query-gpu=timestamp,power.draw,clocks.current.sm,clocks.current.memory,utilization.gpu,utilization.memory,temperature.gpu", "--format=csv,nounits,noheader", "-i", "0", "-f", "{}/{}.txt".format(filepath, filename), "-lms", "{}".format(sampling_period)]

    parent_directory = "/home/PATH/TO/PARENT/FOLDER/astro-accelerate-energy-optimise/"

    if (bfloat == True):
        print("FDAS core frequency range: " +str(low_freq)+ "MHz to " +str(high_freq)+ "Mhz, bfloat16")
        aa_str = [parent_directory + "/astro-accelerate-power-bfloat/astro-accelerate/astro-accelerate", parent_directory + "ska_input.txt", "23.23", "snr0.001", str(low_freq), str(high_freq)]
    else:
        print("FDAS core frequency range: " +str(low_freq)+ "MHz to " +str(high_freq)+ "Mhz, single-precision")
        aa_str = ["/astro-accelerate-power-single/astro-accelerate/astro-accelerate", parent_directory + "ska_input.txt", "23.23", "snr0.001", str(low_freq), str(high_freq)]

    proc = subprocess.Popen(command_str)    #Runs nvidia-smi in another terminal


    aa_start_time = datetime.datetime.now()
    aa_call_bytes = subprocess.run(aa_str,capture_output=True)		# Runs target process
    aa_end_time = datetime.datetime.now()
    aa_call_string = bytes.decode(aa_call_bytes.stdout)
    aa_call = aa_call_string.splitlines()

    fdas_start_time = datetime.datetime.now()
    fdas_end_time = datetime.datetime.now()


    for line in aa_call:
        line = csv.reader(StringIO(str(line)))
        for word in line:
            if word[0] == 'FDAS_START_TIME':
                fdas_start_time = datetime.datetime.strptime(word[1], '%Y/%m/%d %H:%M:%S.%f')
            if word[0] == 'FDAS_END_TIME':
                fdas_end_time = datetime.datetime.strptime(word[1], '%Y/%m/%d %H:%M:%S.%f')

    time.sleep(1)
    proc.terminate()                        #Stops the command in the other terminal

    time.sleep(1)

    aa_time = aa_end_time - aa_start_time
    aa_time = aa_time.total_seconds()

    fdas_time = fdas_end_time - fdas_start_time
    fdas_time = fdas_time.total_seconds()

    aa_energy = calculate_slice_energy(filename + '.txt',aa_start_time, aa_end_time)
    fdas_energy = calculate_slice_energy(filename + '.txt',fdas_start_time, fdas_end_time)

    print("AA took      " +str(aa_end_time-aa_start_time) +     "   from " +str(aa_start_time) + " -> " + str(aa_end_time))
    print("FDAS took    " +str(fdas_end_time-fdas_start_time) + "   from " +str(fdas_start_time) + " -> " + str(fdas_end_time))
    print("Overall during AA, the GPU used  " + str(round(aa_energy)) + " joules, avg " +str(round(aa_energy/aa_time))+ " W");
    print("During FDAS, the GPU used        " + str(round(fdas_energy)) + " joules, avg " +str(round(fdas_energy/fdas_time))+ " W\n");
    return fdas_energy,fdas_time



if __name__ == "__main__":
    bfloat_results_array = []
    single_results_array = []
    freq_array = np.asarray(np.linspace(500,2000,31))			# 500 to 2000Mhz range, e.g. 500, 550, ... 1950, 2000
    numrepeats = 5							# 5 repeats to average results
    for i in range(len(freq_array)-1):
        for j in range(numrepeats):
            results = energy_test(freq_array[i], freq_array[i+1], True)
            results_dict = {"results":results, "low_freq":freq_array[i], "high_freq":freq_array[i+1]}
            bfloat_results_array.append(results_dict)
            results = energy_test(freq_array[i], freq_array[i+1], False)
            results_dict = {"results":results, "low_freq":freq_array[i], "high_freq":freq_array[i+1]}
            single_results_array.append(results_dict)

    print("Single results output")
    with open("DFSresults.json","a") as fp:
	json.dump(bfloat_results_array,fp)

    print("Single results output")
    with open("DFSresults.json","a") as fp:
	json.dump(bfloat_results_array,fp)




