# -*- coding: utf-8 -*-
import numpy as np
import random
import math
import copy
import matplotlib.pyplot as plt
import config as cfg
import datetime
import os
import sys
sys.path.append('../code')
from load_data import prepare_data

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

def intial_pheromone_graph(cost_time_graph):
    pheromone_graph = np.zeros((city_num, city_num), dtype=float)
    for i in range(city_num):
        for j in range(city_num):
            if cost_time_graph[i,j] >=tsc and \
            cost_time_graph[i,j] != float('inf') :
                pheromone_graph[i,j] = 1.0/(city_num*tsc)
    return pheromone_graph


running_lines, start_stations, start_prepared,end_prepared, \
cost_time_graph, repair_qualify = prepare_data(cfg.case1_path)

"""parameter"""
city_num = len(running_lines)

(p_max, iterNum_max, ALPHA, BETA, RHO, Q, b) = cfg.aco_param
(tsc, tsp_1) = cfg.total_param

"""main part"""
emu_data_initial = emu_info(city_num)
pheromone_graph = intial_pheromone_graph(cost_time_graph)
#emu_data_initial = np.loadtxt("emu_data.txt")

best_num_plot = []
best_time_iternum = []
best_time_plot = []
best_emu_lines_total = []
best_num_total = city_num
best_repair_total = 50
best_time_total = 3000


iterNum = 0
while iterNum < iterNum_max:
    y = np.zeros((city_num, city_num), dtype=int)
    #one iteration of ACO
    p = 0
    valid_tp = []
    ant_path_total = []
    best_time = float("inf")
    best_repair  = 50
    best_num = city_num
    best_emu_data = copy.deepcopy(emu_data_initial)
    best_emu_lines = []
    while p < p_max:
    #step two
        emu_data = copy.deepcopy(emu_data_initial)
        lines_have_front = []
        lines_have_back = []
        nl=0
        p = p+1
        ant_path = []
        emu_lines_total = []
        stop_or_not = 0
        running_in_stations = copy.deepcopy(start_prepared)
        test_stations = copy.deepcopy(start_stations)
        A_allow_total = []
        for c1 in range(len(cost_time_graph)):
            A_allow_c1 = []
            for c2 in range(len(cost_time_graph)):
                if pheromone_graph[c1,c2] != 0:
                    A_allow_c1.append(c2)
            A_allow_total.append(A_allow_c1)
        repair = 0
        total_lines = []
        for i in range(len(running_lines)):
            total_lines.append(i)
        selected_index = random.randint(0,len(test_stations)-1)
        #yici xunhuan 
        while stop_or_not == 0:
            emu_lines=[]
            A_allow = []
            if len(running_in_stations[selected_index]) != 0:
                line1_index = running_in_stations[selected_index][0]
                    #compute A_allow of i
                A_allow = []
                for j in range(len(cost_time_graph)):
                    if pheromone_graph[line1_index,j] != 0:
                        if j not in lines_have_front:
                            if j in total_lines:
                                A_allow.append(j)
                find_blank_line = 0
                emu_data[nl][1] += float(running_lines[line1_index][5])
                emu_data[nl][2] += (int(running_lines[line1_index][4])\
                        -int(running_lines[line1_index][3]))
                
                emu_lines.append(line1_index)
                running_in_stations[selected_index].remove(line1_index)
                ant_path.append(line1_index)
                if line1_index in total_lines:
                        total_lines.remove(line1_index)
                A_allow_total[line1_index] = A_allow
                if len(A_allow) : 
                    current_index = line1_index
                    while find_blank_line == 0:  #find a line without any allow
                        # update repair data
                        for index in A_allow_total[current_index]:
                            if emu_data[nl][1] >= 4000 or emu_data[nl][2] >= 2880:
                                repair += 1
                                emu_data[nl][1] = 0
                                emu_data[nl][2] = 0
                                if repair_qualify[current_index,index] == 1:
                                    y[current_index,index]=1
                                else: y[current_index,index]=2
                        b_allow = []
                        for station in A_allow_total[current_index]:
                            if station in total_lines:
                                b_allow.append(station)
                        A_allow_total[current_index] = b_allow[:]
                        if len(A_allow_total[current_index]) == 1:
                            if A_allow_total[current_index][0] not in total_lines:
                                A_allow_total[current_index] = []
                        # step four: compute probability
                        if len(A_allow_total[current_index])>= 1:
                            probability = np.zeros((len(A_allow_total[current_index]), 1), dtype=float)
                            sum_pro = 0 
                            for j in range(len(A_allow_total[current_index])):
                                if y[current_index,index] == 2:
                                    probability[j] = 0
                                else:
                                    probability[j] =(math.pow(pheromone_graph[current_index,A_allow_total\
                                               [current_index][j]], ALPHA))*(math.pow(round(1.0/cost_time_graph\
                                               [current_index,A_allow_total[current_index][j]],8),BETA))
                                sum_pro += probability[j]
                            if sum_pro != 0:
                                probability = probability/sum_pro
                                use_index = np.random.choice(np.arange(0, len(A_allow_total\
                                            [current_index]), 1), p = probability.ravel())
                                line2_index =A_allow_total[current_index][use_index]
                                lines_have_front.append(line2_index)
                                lines_have_back.append(line1_index)
                                emu_lines.append(line2_index)
                                ant_path.append(line2_index)
                                for k in range(len(running_in_stations)):
                                    if line2_index in running_in_stations[k]:
                                        running_in_stations[k].remove(line2_index)
                                        break
                                if line2_index in total_lines:
                                    total_lines.remove(line2_index)
                                #to updata emu data
                                emu_data[nl][1] += float(running_lines[line2_index][5])
                                emu_data[nl][2] += (float(running_lines[line2_index][4])-float(running_lines[line2_index][3]))
                                emu_data[nl][1] *=(1-y[line1_index,line2_index])
                                emu_data[nl][2] *=(1-y[line1_index,line2_index])
                                current_index = line2_index
                        #update
                            else: find_blank_line = 1
                        else:find_blank_line = 1
                emu_lines_total.append(emu_lines)
                nl = nl+1
            # to clear blank stations
            if not running_in_stations[selected_index]:
                del test_stations[selected_index]
                running_in_stations.remove([])
            if not test_stations:
                stop_or_not = 1
            if len(test_stations) >1:
                selected_index = random.randint(0,len(test_stations)-1)
            else: selected_index = 0
        connect_time = 0
        for i in range(1,city_num):
            start, end = ant_path[i-1], ant_path[i]
            if cost_time_graph[start, end] != float("inf"):
                connect_time += cost_time_graph[start, end]
        if len(emu_lines_total) < best_num and emu_lines_total:
            best_emu_lines = copy.deepcopy(emu_lines_total)
            best_num = len(emu_lines_total)
            best_repair = repair
            best_time = connect_time
            best_emu_data = copy.deepcopy(emu_data)
        ant_path_total.append(ant_path)
    # update the lines that have been connected
        
    #compute_total_connect_time:
    total_connect_time  =  np.zeros((p_max, 1), dtype=float)
    for ant in range(p_max):
        for i in range(1,city_num):
            start, end = ant_path_total[ant][i-1], ant_path_total[ant][i]
            if cost_time_graph[start, end] != float("inf"):
                total_connect_time[ant] += cost_time_graph[start, end]

    
    temp_pheromone = [[0.0 for col in range(city_num)] for raw in range(city_num)]
    for ant in range(p_max):
        for i in range(1,city_num):
            start, end = ant_path_total[ant][i-1], ant_path_total[ant][i]
            temp_pheromone[start][end] += Q*1.0 / total_connect_time[ant]
            temp_pheromone[end][start] = temp_pheromone[start][end]
    for i in range(city_num):
        for j in range(city_num):
            pheromone_graph[i][j] = pheromone_graph[i][j] *(1-RHO) + temp_pheromone[i][j]
    
    #for A_allow_total
    for i in range(city_num):
        for j in range(city_num):
            if cost_time_graph[i,j] >=tsc and cost_time_graph[i,j] != float('inf') :
                pheromone_graph[i][j] = (1-b)*pheromone_graph[i][j] + b*1.0/(city_num*tsc)
    
    
    if len(best_emu_lines) <= best_num_total:
        #if best_time < best_time_total:
        #if best_repair < best_repair_total:
            best_emu_lines_total = best_emu_lines
            best_num_total = best_num
            best_repair_total = best_repair
            best_time_total = best_time
            best_time_plot.append(best_time_total)
            best_time_iternum.append(iterNum)
            best_num_plot.append(best_num_total)
    

    iterNum += 1

best_time_plot.append(best_time_total)
best_time_iternum.append(iterNum)
best_num_plot.append(best_num_total)

aaa_emu_line_total = []
for lines in best_emu_lines_total:
    aaa_emu_line = []
    for line in lines:
        aaa_emu_line.append(running_lines[line][0])
    aaa_emu_line_total.append(aaa_emu_line)



"""results"""
now_time = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')

if not os.path.exists('../result/'+str(now_time)):
    os.makedirs('../result/'+str(now_time)) 



with open('../result/'+str(now_time)+'/routing_sets.txt', 'w') as file:
    for line in aaa_emu_line_total:
        for tst in line:
            file.write(str(tst))
            file.write(" ")
        file.write('\n')
file.close()


plot_data = np.c_[np.array(best_time_iternum),np.array(best_time_plot)]
fig = plt.figure()
fig.set_size_inches(10, 8)
plt.plot(plot_data[:,0], plot_data[:,1], color = 'b')
plt.ylim((min(best_time_plot)-100,max(best_time_plot)+100))
plt.xlim(0,iterNum)
plt.xlabel('Iteration_Num',fontsize = 15)
plt.ylabel('EMU_time',fontsize = 15)
plt.xticks(fontsize = 15)
plt.yticks(fontsize = 15)
fig.savefig('../result/'+str(now_time)+'/best_time_fig.png', dpi=200)


num_data = np.c_[np.array(best_time_iternum),np.array(best_num_plot)]   
fig = plt.figure()
fig.set_size_inches(10, 8)
plt.plot(num_data[:,0], num_data[:,1], color = 'g')
plt.ylim((min(best_num_plot)-2,max(best_num_plot)+2))
plt.xlim(0,iterNum)
plt.xlabel('Iteration_Num',fontsize = 15)
plt.ylabel('EMU_num',fontsize = 15)
plt.xticks(fontsize = 15)
plt.yticks(fontsize = 15)
fig.savefig('../result/'+str(now_time)+'/best_num_fig.png', dpi=200)
