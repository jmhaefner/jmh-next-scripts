import tables as tb
from tables import *
import numpy as np
import matplotlib.pyplot as plt
import invisible_cities.io.channel_param_io as pIO

# Runs without taking arguments. Eventually, should be made to take in the
# desired h5 file as an argument. Will show plots at the end, although
# create_sensor_plots can be used on its own to generate the plots without
# actually showing them.

def create_sensor_plots(h5in, tab_name):

    sens = [ sen for sen, (val, err) in pIO.generator_param_reader(h5in, tab_name) ]
    vals = [ val for sen, (val, err) in pIO.generator_param_reader(h5in, tab_name) ]
    errs = [ err for sen, (val, err) in pIO.generator_param_reader(h5in, tab_name) ]

    plot_names = list(vals[0].keys())

    for plot_name in plot_names:

        plot_vals = [ vals[sen_indx][plot_name] for sen_indx in range(len(sens)) ]
        plot_errs = [ errs[sen_indx][plot_name] for sen_indx in range(len(sens)) ]

        TestVal = plot_vals[0]

        if not isinstance(TestVal, np.ndarray):
            plt.figure()
            plt.errorbar(sens, plot_vals, yerr=plot_errs, fmt=',', capsize = 4)
            plt.xlabel('channel')
            plt.ylabel(plot_name)
            plt.title(tab_name)

def print_list(myList):
    for item in myList:
        print(item)

# h5in = tb.open_file('/Users/jmhaefner/Documents/NEXT_code/IC_current/IC/pmtCalParOut_R50ns_Fdfunc.h5', 'r') # pmt test file
h5in = tb.open_file('/Users/jmhaefner/Documents/NEXT_code/IC_current/IC/sipmCalParOut_R6254_Fdfunc.h5', 'r') # sipm test file

table_names, param_names, param_tables = pIO.basic_param_reader(h5in)

'''

# This block is helpful for understanding - it shows
# exactly how each piece of data is take from the
# param_tables tables
for table_index in range(len(table_names)):
    print('Examining table ' + table_names[table_index])
    for sns_index in range(len(param_tables[table_index])):
        print('\tExamining sensor ' + str(sns_index))
        for param_index in range(len(param_names[table_index])):
            ValErr = param_tables[table_index][sns_index][param_index]
            if isinstance(ValErr, np.ndarray):
                print('\t\t' + param_names[table_index][param_index] + ' = ' + str(ValErr[0]) + ' +- ' + str(ValErr[1]))
            else:
                print('\t\t' + param_names[table_index][param_index] + ' = ' + str(ValErr))

'''

for tab_name in table_names:
    create_sensor_plots(h5in, tab_name)

h5in.close()

plt.show()
