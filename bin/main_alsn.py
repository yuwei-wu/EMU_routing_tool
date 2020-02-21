# -*- coding: utf-8 -*-
import numpy as np
import random
import math
import copy
import matplotlib.pyplot as plt
import sys
sys.path.append('../code')
from create_initial import greedy_creation
from load_data import prepare_data
import config as cfg

# EMU info random generation
def emu_order(b):
    return b[1]

def emu_info(num):
    emu_data  = np.zeros((num, 3), dtype=float)
    for i in range(len(emu_data)):
        emu_data[i,0] = i
        emu_data[i,1] = random.randint(0,4000)
    #emu_data = np.array(sorted(emu_data, key = emu_order))
    return emu_data


running_lines, start_stations, start_prepared,end_prepared,\
cost_time_graph, repair_qualify = prepare_data(cfg.case1_path)


"""parameter"""
city_num = len(running_lines)
(tsc, tsp_1) = cfg.total_param

"""main part"""
emu_data_initial = emu_info(city_num)
#emu_data_initial = np.loadtxt("emu_data.txt")


best_num_plot = []
best_tim_iternum = []
best_time_plot = []
best_emu_lines_total = []
best_num_total = city_num
best_repair_total = 50
best_time_total = 3000

#intial solutions
emu_lines_total = greedy_creation(cost_time_graph,running_lines)





