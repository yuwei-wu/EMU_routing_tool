#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: wuyuwei

input: info of map and needed data

output: the feasible solutions for the problems
"""
import numpy as np
import copy

def greedy_creation(cost_time_graph,running_lines):
    total_lines = []
    for i in range(len(running_lines)):
        total_lines.append(i)
    city_num = len(running_lines)
    probability_total = np.zeros((city_num, 1), dtype=float)
    sum_pro = 0
    for i in range(city_num):
        for j in range(city_num):
            if cost_time_graph[i,j] != float('inf') :
                probability_total[i]=1
        sum_pro += probability_total[i]
    probability_total = probability_total/sum_pro
    start_line_index = np.random.choice(np.arange(0, city_num, 1), p = probability_total .ravel())
    emu_lines_total = []
    cost_compute = copy.deepcopy(cost_time_graph)
    total_stop_or_not = 1
    while total_stop_or_not:
        index1 = start_line_index
        total_lines.remove(index1)
        emu_lines = []
        emu_lines.append(index1)
        stop_or_not = 1
        while stop_or_not:
            index2 = np.argmin(cost_compute[index1,:], axis=None)
            if cost_compute[index1,index2] != float('inf'):
                cost_compute[index1,:] = float('inf')
                cost_compute[:,index1] = float('inf')
                total_lines.remove(index2)
                emu_lines.append(index2)
                index1 = index2
            else: 
                stop_or_not = 0
                cost_compute[index1,:] = float('inf')
                cost_compute[:,index1] = float('inf')
        emu_lines_total.append(emu_lines)
        start_line_index = np.where(cost_compute==np.min(cost_compute))[0][0]
        if np.min(cost_compute) == float('inf'):
            total_stop_or_not = 0
    for line in total_lines:
        emu_lines_total.append(line)
    return emu_lines_total
    
    
    
    
    
    
    
    
    
    
    
    
    
    