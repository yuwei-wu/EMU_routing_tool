#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: wuyuwei

input: the dir of map and needed data

output: data
"""
import numpy as np
import sys
import random
sys.path.append('../bin')
import config as cfg


def time_order(a):
    return int(a[3])

def prepare_data(data_path):
    input_data = open(data_path)
    running_lines = []
    for line in input_data.readlines():
        line = line[:-1].split(" ")
        running_lines.append(line)
    #new_running_lines = sorted(running_lines, key =time_order, reverse=False)
    start_stations = []
    for i, running_line1 in enumerate(running_lines):
        if running_line1[1] not in start_stations:
            start_stations.append(running_line1[1])
    city_num = len(running_lines)
    # find train sequences in stations
    start_prepared= []
    end_prepared = []
    for i in start_stations:
        start_p= []
        end_p = []
        for j, running_line1 in enumerate(running_lines):
            if running_line1[1] == i:
                start_p.append(j)
            if running_line1[2] == i:
                end_p.append(j)
        start_prepared.append(start_p)
        end_prepared.append(end_p)

    #compute cost_time_graph
    cost_time_graph = np.zeros((city_num, city_num),dtype=float)
    for i, running_line1 in enumerate(running_lines):
        for j, running_line2 in enumerate(running_lines):
            if running_line2[1] == running_line1[2]:
                
                left_time = float(running_line2[3])-float(running_line1[4])
                if left_time >= cfg.total_param[0]:
                    cost_time_graph[i,j] = left_time
                #else:cost_time_graph[i,j] = left_time+1440
                else: cost_time_graph[i,j] = float('inf')
            else: cost_time_graph[i,j] = float('inf')

    num = len(cost_time_graph)
    repair_qualify = np.zeros((num, num), dtype=int)
    for i in range(num):
        for j in range(num):
            if cost_time_graph[i,j] >= cfg.total_param[1] and cost_time_graph[i,j] != float('inf'):
                    repair_qualify[i,j] = 1
            else: repair_qualify[i,j] = 0

    return running_lines, start_stations, start_prepared,end_prepared, cost_time_graph, repair_qualify