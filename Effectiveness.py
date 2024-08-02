# -*- coding: utf-8 -*-
"""
Created on Fri Apr  7 08:43:57 2023

@author: Win10
"""
#YOU CAN CHANGE SUBSEQUENCE LENGTH, SHIFT LENGTH AND K VALUES
#Calculate number of operations and savings for linear, pane, and pair
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.spatial import distance
import math
import collections

#Pane Window Technique
L = [600]  #Time series data length
R = [12, 24, 36, 48, 54, 60]  #Subsequence length
SHIFT = [1, 6]  #Shift length
K = [1, 2, 3, 4, 5, 6, 7]
#K = [1, 2]
sh_list = []
linear_oper_count = 0
summ_linear = 0
agg_linear = 0
oper_linear = 0
oper_linear_list = []
save_linear = 0
save_linear_list = []
DEV_REF_list = []
DEV_REF_dict = {}
DEV_list = []
DEV_dict = {}


summ_pane = 0
oper_pane = 0
save_pane = 0
agg_pane = 0
DEV_pane_list = []
DEV_pane_dict = {}
oper_pane_list = []
save_pane_list = []

summ_pair = 0
oper_pair = 0
save_pair = 0
agg_pair = 0
DEV_pair_list = []
DEV_pair_dict = {}
oper_pair_list = []
save_pair_list = []

per_linear_list = []
per_save_linear_list = []
per_oper_pane_list = []
per_save_pane_list = []
per_oper_pair_list = []
per_save_pair_list = []

views_dict = {}
p = 0.9
merge = {}
RBO_list = []
RBO_dict = {}
SHIFT_list = []


data = pd.read_csv('AE.csv')  #AU.csv, BR.csv, KR.csv and US.csv
data1 = pd.read_csv('AE.csv') #AU.csv, BR.csv, KR.csv and US.csv

UAE_ACTUALL = data['workplaces'].iloc[ : L[0]] #workplace series
US_ACTUALL = data['residential'].iloc[ : L[0]] #residential series

UAE_ACTUAL = data['workplaces'].iloc[ : L[0]]  #workplace series
US_ACTUAL = data['residential'].iloc[ : L[0]]  #residential series
# print("type of ",type(US_ACTUALL))
# UAE_ACTUAL = pd.DataFrame({'A' : []})
# US_ACTUAL = pd.DataFrame({'A' : []})
#df = pd.concat([UAE_ACTUAL, US_ACTUAL])
#min_1 = df.min()
#max_1 = df.max()

for l in R:
    for sh in SHIFT:
        oper_linear = 0
        DEV_REF_list = []
        DEV_list = []
        DEV_list_sorted = []
        DEV_list_sorted_index = []
        
        oper_pane = 0
        save_pane = 0
        DEV_pane_list = []
        DEV_pane_list_sorted = []
        DEV_pane_list_sorted_index = []
        
        oper_pair = 0
        save_pair = 0
        DEV_pair_list = []
        DEV_pair_list_sorted = []
        DEV_pair_list_sorted_index = []
    
        
        for n in L:
        
            #Select Data from the begining
            UAE_ACTUALL = data['workplaces'].iloc[ : n]  #workplace series
            US_ACTUALL = data['residential'].iloc[ : n]  #residential series
            #print("UAE_ACTUALL ",UAE_ACTUALL)
                    
            #Data after normalization
            #UAE_ACTUAL = (UAE_ACTUAL-min_1)/(max_1-min_1)
            #US_ACTUAL = (US_ACTUAL-min_1)/(max_1-min_1)
            #print(UAE_ACTUAL, US_ACTUAL)
            #print(len(UAE_ACTUAL))
            #print(len(US_ACTUAL))
    
            
            print("(n-l)%sh(n-l)%sh ",(n-l)%sh)
            if((n-l)%sh==0):
                SHIFT_list.append(sh)
                print("sh          ",sh)
                sh_list.append(sh)
                V = int((n-l)/sh)+1 #Number of views
                print("VIEWSSSSSSSS ",V)
                
                for i in range(0,V,1):   #V+1
                    
                    summ_linear = 0
                    agg_linear = 0
                    
                    summ_pane = 0
                    agg_pane = 0
                    
                    summ_pair = 0
                    agg_pair = 0

                    #print("UAE_ACTUAL[i*sh:l+i*sh]b ",UAE_ACTUALL[i*sh:l+i*sh])
                    #print("US_ACTUAL[i*sh:l+i*sh]b ",US_ACTUALL[i*sh:l+i*sh]) 
                    
                    
                    #Data after normalization individually for each subsequence
                    #First subsequence
                    min_1 = UAE_ACTUALL[i*sh:l+i*sh].min()
                    max_1 = UAE_ACTUALL[i*sh:l+i*sh].max()
                    #print("min_1 ",min_1)
                    #print("max_1 ",max_1)
                    print("UAE_ACTUALL[i*sh:l+i*sh] b  ",UAE_ACTUALL[i*sh:l+i*sh])
                    if (min_1 == max_1):
                        UAE_ACTUAL[i*sh:l+i*sh] = UAE_ACTUALL[i*sh:l+i*sh]
                    else:
                        UAE_ACTUAL[i*sh:l+i*sh] = (UAE_ACTUALL[i*sh:l+i*sh]-min_1)/(max_1-min_1)
                    #print("UAE_ACTUAL[i*sh:l+i*sh] ",UAE_ACTUAL[i*sh:l+i*sh])

                    #Second subsequence
                    min_2 = US_ACTUALL[i*sh:l+i*sh].min()
                    max_2 = US_ACTUALL[i*sh:l+i*sh].max()
                    #print("min_2 ",min_2)
                    #print("max_2 ",max_2)
                    if (min_2 == max_2):
                        UAE_ACTUAL[i*sh:l+i*sh] = UAE_ACTUALL[i*sh:l+i*sh]
                    else:                    
                        US_ACTUAL[i*sh:l+i*sh] = (US_ACTUALL[i*sh:l+i*sh]-min_2)/(max_2-min_2)
                    #print("US_ACTUAL[i*sh:l+i*sh] ",US_ACTUAL[i*sh:l+i*sh])
                    
                    DEV_REF = distance.euclidean(UAE_ACTUAL[i*sh:l+i*sh], US_ACTUAL[i*sh:l+i*sh])
                    #print("DEV_REF ",DEV_REF)
                    DEV_REF_list.append('%.10f'%DEV_REF)
                    #print("DEV_REF_list ",DEV_REF_list)
                    #print(len(DEV_REF_list))
                
                    #Linear Calculation
                    for j in range(i*sh,l+i*sh,1):
                        
                        #Calculate the deviation of subsequence
                        summ_linear = (UAE_ACTUAL[j]-US_ACTUAL[j])**2
                        oper_linear+=1
                        agg_linear += summ_linear
                        
                        if (j != i*sh):
                            oper_linear+=1
    
                    DEV = math.sqrt(agg_linear)
                    #print("DEV ",DEV)
                    DEV_list.append('%.10f'%DEV)
                    #print("DEV_list ",DEV_list)
                    #print(len(DEV_list))
                    
                    #Pane Calculation
                    g = int(math.gcd(l,sh))
                    P = int(l/g)
                    if i == 0:   #First View
                        
                        for j in range(i*sh,l+i*sh,1):
                            
                            #Calculate the deviation of first subsequence
                            summ_pane = (UAE_ACTUAL[j]-US_ACTUAL[j])**2
                            oper_pane+=1
                            agg_pane += summ_pane
                            
                            if (j != 0):
                                oper_pane+=1
                                
                        DEV = math.sqrt(agg_pane)
                        #print("DEV ",DEV)
                        DEV_pane_list.append('%.10f'%DEV)
                        #print("DEV_pane_list ",DEV_pane_list)
                        #print(len(DEV_pane_list))
                        #print("oper_pane1 ",oper_pane)
    
                    else:   #Other Views
                        
                        for j in range(i*sh,l+i*sh,1):
                            
                            if j>=i*sh and j<i*sh+l-sh:
                                
                                #Calculate the deviation of subsequence
                                summ_pane = (UAE_ACTUAL[j]-US_ACTUAL[j])**2
                                save_pane+=1
                                agg_pane += summ_pane
                                
                                if j!=i*sh:
                                    save_pane+=1
    
                            else:
                                
                                #Calculate the deviation of subsequence
                                summ_pane = (UAE_ACTUAL[j]-US_ACTUAL[j])**2
                                oper_pane+=1
                                agg_pane += summ_pane
                                oper_pane+=1
                                
    
    
    
                        DEV = math.sqrt(agg_pane)
                        #print("DEV ",DEV)
                        DEV_pane_list.append('%.10f'%DEV)
                        #print("DEV_pane_list ",DEV_pane_list)
                        #print(len(DEV_pane_list))
                        #print("oper_pane2 ",oper_pane)
                        #save_pane+=1
                        #oper_pane+=sh-1
                        # for z in range(1,int(sh/g)+1,1):
                        #     print("zzzzz")
                        #     for a in range(1,g,1):
                        #         print("aaaaaaaaa")
                        #         oper_pane+=1
                        #     oper_pane+=1
                        
                        #print("oper_paneoper_paneoper_pane ",oper_pane)
    
                    #Pair Calculation
                    if (l%sh==0):  #Same as pane window
                    
                        #Pane Calculation
                        g = int(math.gcd(l,sh))
                        P = int(l/g)
                        if i == 0:   #First View
                            
                            for j in range(i*sh,l+i*sh,1):
                                
                                #Calculate the deviation of first subsequence
                                summ_pair = (UAE_ACTUAL[j]-US_ACTUAL[j])**2
                                oper_pair+=1
                                agg_pair += summ_pair
                                
                                if (j != 0):
                                    oper_pair+=1
                                    
                            DEV = math.sqrt(agg_pair)
                            #print("DEV ",DEV)
                            DEV_pair_list.append('%.10f'%DEV)
                            #print("DEV_pair_list ",DEV_pair_list)
                            #print(len(DEV_pair_list))
                            #print("oper_pair1 ",oper_pair)
    
                        else:   #Other Views
                            
                            for j in range(i*sh,l+i*sh,1):
                                
                                if j>=i*sh and j<i*sh+l-sh:
                                    
                                    #Calculate the deviation of subsequence
                                    summ_pair = (UAE_ACTUAL[j]-US_ACTUAL[j])**2
                                    save_pair+=1
                                    agg_pair += summ_pair
                                    
                                    if j!=i*sh:
                                        save_pair+=1
                                    
                                else:
                                    
                                    #Calculate the deviation of subsequence
                                    summ_pair = (UAE_ACTUAL[j]-US_ACTUAL[j])**2
                                    oper_pair+=1
                                    agg_pair += summ_pair
                                    oper_pair+=1
                                    
                            DEV = math.sqrt(agg_pair)
                            #print("DEV ",DEV)
                            DEV_pair_list.append('%.10f'%DEV)
                            #print("DEV_pane_list ",DEV_pane_list)
                            #print(len(DEV_pane_list))
                            #print("oper_pane2 ",oper_pane)
                            #save_pair+=1
                            #oper_pair+=sh-1
                            #oper_pair+=1
                            #print("iiiiiiiiiiiiii")
                    else:   #Pair calculation
                        #print("kkkkkkkkkkkkkkkkkkkkkkkkk")
                        g1 = l%sh
                        g2 = sh-g1
                        
                        if i == 0:   #First View
                            
                            for j in range(i*sh,l+i*sh,1):
                                
                                #Calculate the deviation of first subsequence
                                summ_pair = (UAE_ACTUAL[j]-US_ACTUAL[j])**2
                                oper_pair+=1
                                agg_pair += summ_pair
                                
                                if (j != 0):   #i*sh
                                    oper_pair+=1
                                    
                            DEV = math.sqrt(agg_pair)
                            #print("DEV ",DEV)
                            DEV_pair_list.append('%.10f'%DEV)
                            #print("DEV_pair_list ",DEV_pair_list)
                            #print(len(DEV_pair_list))
                            #print("oper_pair1 ",oper_pair)
    
                        else:   #Other Views
                            #print("othersssssssssss")
                            for j in range(i*sh,l+i*sh,1):
                                
                                if j>=i*sh and j<i*sh+l-sh:
                                    
                                    #Calculate the deviation of subsequence
                                    summ_pair = (UAE_ACTUAL[j]-US_ACTUAL[j])**2
                                    save_pair+=1
                                    agg_pair += summ_pair
                                    
                                    if j!=i*sh:
                                        save_pair+=1
                                    
                                else:
                                    
                                    #Calculate the deviation of subsequence
                                    summ_pair = (UAE_ACTUAL[j]-US_ACTUAL[j])**2
                                    oper_pair+=1
                                    agg_pair += summ_pair
                            #print("oper_pair1 ",oper_pair)       
                            for j in range(1, g1, 1):
                                oper_pair += 1
                                #oper_pair+=1
                            #print("oper_pair2 ",oper_pair)
                            for j in range(1, g2, 1):
                                oper_pair+=1
                                #oper_pair+=1
                            #print("oper_pair3 ",oper_pair)
                            oper_pair+=1
                            #save_pair+=1
                            #print("oper_pair4 ",oper_pair)
                            DEV = math.sqrt(agg_pair)
                            #print("DEV ",DEV)
                            DEV_pair_list.append('%.10f'%DEV)
                            #print("DEV_pane_list ",DEV_pane_list)
                            #print(len(DEV_pane_list))
                            #print("oper_pane2 ",oper_pane)
                            #save_pair+=1
                            oper_pair+=1
                            
                            
                    
                    
        print("shift length ",sh)            
        #Linear Search           
        DEV_REF_dict[sh]=DEV_REF_list
        DEV_dict[sh]=DEV_list
        oper_linear_list.append(oper_linear)
        save_linear_list.append(save_linear)
        
        #Sort the deviation with the index for linear
        DEV_list_sorted = sorted(DEV_list,reverse=True)
        print("DEV_list ",DEV_list)
        print("DEV_list_sorted ",DEV_list_sorted)
        DEV_list_sorted_index = sorted(range(len(DEV_list)), key=lambda k: DEV_list[k], reverse=True)
        print("DEV_list_sorted_index ",DEV_list_sorted_index)     
        DEV_list_sorted_index = [x+1 for x in DEV_list_sorted_index]   #Represents the views
        print("DEV_list_sorted_index2 ",DEV_list_sorted_index) 
        
        views_dict[sh] = DEV_list_sorted_index
        
        DEV_REF_list = []
        DEV_list = []
        print("###################################")
        #Pane Window
        #print("oper_pane ",oper_pane)
        #print("save_pane ",save_pane)
        # print("DEV_pane_list ",DEV_pane_list)
        DEV_pane_dict[sh] = DEV_pane_list
        oper_pane_list.append(oper_pane)
        save_pane_list.append(save_pane)   

        #Sort the deviation with the index for pane
        DEV_pane_list_sorted = sorted(DEV_pane_list, reverse=True)
        print("DEV_pane_list ",DEV_pane_list)
        print("DEV_pane_list_sorted ",DEV_pane_list_sorted)
        DEV_pane_list_sorted_index = sorted(range(len(DEV_pane_list)), key=lambda k: DEV_pane_list[k], reverse=True)
        print("DEV_pane_list_sorted_index ",DEV_pane_list_sorted_index)     
        DEV_pane_list_sorted_index = [x+1 for x in DEV_pane_list_sorted_index]   #Represents the views
        print("DEV_pane_list_sorted_index2 ",DEV_pane_list_sorted_index) 
                
        DEV_pane_list = []
        
        
        print("###################################")        
        #Pair Window
        #print("oper_pair ",oper_pair)
        #print("save_pair ",save_pair)
        #print("DEV_pair_list ",DEV_pair_list)
        DEV_pair_dict[sh] = DEV_pair_list
        oper_pair_list.append(oper_pair)
        save_pair_list.append(save_pair)   

        #Sort the deviation with the index for pane
        DEV_pair_list_sorted = sorted(DEV_pair_list, reverse=True)
        print("DEV_pair_list ",DEV_pair_list)
        print("DEV_pair_list_sorted ",DEV_pair_list_sorted)
        DEV_pair_list_sorted_index = sorted(range(len(DEV_pair_list)), key=lambda k: DEV_pair_list[k], reverse=True)
        print("DEV_pair_list_sorted_index ",DEV_pair_list_sorted_index)     
        DEV_pair_list_sorted_index = [x+1 for x in DEV_pair_list_sorted_index]   #Represents the views
        print("DEV_pair_list_sorted_index2 ",DEV_pair_list_sorted_index)
        
        DEV_pair_list = []
        
        #Percentage calculation
        per_linear_list.append(oper_linear/(oper_linear)*100)
        per_save_linear_list.append(0/(oper_linear)*100)
        per_oper_pane_list.append(oper_pane/(oper_linear)*100)
        per_save_pane_list.append(save_pane/(oper_linear)*100)
        per_oper_pair_list.append(oper_pair/(oper_linear)*100)
        per_save_pair_list.append(save_pair/(oper_linear)*100) 
        
        
    print("DEV_dict ",DEV_dict)   
    print("DEV_pane_dict ",DEV_pane_dict)   
    print("DEV_pair_dict ",DEV_pair_dict) 

    #Calculation For TiRBO (RBO for time series data)
    print("views for different shift lengths ", views_dict) 

    #How to get views when shift length S = 1
    views_S1 = list(views_dict.values())[0]
    print("For S=1 ",list(views_dict.values())[0])
    

    #Get the views for other shift lengths
    for sh in SHIFT[1:]:
        print("shift length ",sh)  
        print("for other shift lengths ",views_dict[sh])  

        #We need to focus on top-k views only        
        for i in K:
            print("K========= ",i)
            #Transform values from views to subsequence (start, end)
            print(views_S1[:i])
            views_S1_K = views_S1[:i]
            views_S1_transform = [[(i-1)*1+1,(i-1)*1+l]for i in views_S1_K]
            print("views_S1_transform ",views_S1_transform)
            print(views_dict[sh][:i])
            views_dict_sh = views_dict[sh][:i]
            views_dict_transform = [[(i-1)*sh+1,(i-1)*sh+l]for i in views_dict_sh]
            print("views_dict_transform ",views_dict_transform)
        #print("---------------------------------------------------")        
                
            #Calculate RBO for views_S1_transform and views_dict_transform
            print("lennnnn ",len(views_dict_transform))
            for k in range (1, len(views_dict_transform)+1, 1):
                #print(k)
                #merge = [if views_S1_transform[k][0]<= views_dict_transform[k][0]: a + b for (a, b) in zip(views_S1_transform[k], views_dict_transform[k])]
                # for (a, b) in zip(views_S1_transform[k], views_dict_transform[k]):
                #     print(a)
                #     print(b)
                if views_S1_transform[k-1][0]<= views_dict_transform[k-1][0]:
                    merge[k] = [views_S1_transform[k-1]]
                    merge[k].append(views_dict_transform[k-1])
                else:
                    merge[k] = [views_dict_transform[k-1]]
                    merge[k].append(views_S1_transform[k-1])
            print("merge ",merge) 
        
            #Ready to calculate RBO
            
            #For first term
            x_k = 0
            print(len(merge.keys()))
            for i in range (1, len(merge.keys())+1, 1):  
                print(merge[i])
                b1 = merge[i][0][0]
                e1 = merge[i][0][1]
                b2 = merge[i][1][0]
                e2 = merge[i][1][1]        
                #print("b1 ",b1)
                #print("e1 ",e1)
                #print("b2 ",b2)
                #print("e2 ",e2)
                if (e1 < b2):
                    x_k += 0
                else:
                    x_k += (e1 - b2 + 1)/(e2 - b1 + 1) 
                #print("x_k ",x_k)
            #print("x_k ",x_k)
            first_term = (x_k/len(merge.keys())) * math.pow(p,len(merge.keys()))
            print("first_term ",first_term)
            
            #For summation term
            sum_term_k = 0
            second_term = 0
            for j in range (1, len(merge.keys())+1, 1): 
                #print("jjjjjjjjj ",j)
                for k in range (1, j+1, 1): 
                    #print("kkkkkkkkkkkk ",k)  
                    b1 = merge[k][0][0]
                    e1 = merge[k][0][1]
                    b2 = merge[k][1][0]
                    e2 = merge[k][1][1]        
                    #print("b1 ",b1)
                    #print("e1 ",e1)
                    #print("b2 ",b2)
                    #print("e2 ",e2)
                    if (e1 < b2):
                        sum_term_k += 0
                    else:
                         sum_term_k += (e1 - b2 + 1)/(e2 - b1 + 1)
                    #print("sum_term_k ",sum_term_k)
                second_term += (sum_term_k/j) * math.pow(p, j) 
                print("second_term ",second_term)
                sum_term_k = 0
            print("second_termxx ",second_term)
            second_term_final = ((1-p)/p)*second_term
            print("second_term_final ",second_term_final)
            RBO = first_term + second_term_final
            print("RBOOOOOOO ",RBO)
            
            RBO_list.append(RBO)
    RBO_dict[l] = RBO_list
    print("RBO_list ",RBO_list) 
    RBO_list = []
    merge = {}
                                     
print("RBO_dict ",RBO_dict)  

#Plotting
colors = ['r','g','b','c', 'm', 'y']
marker= ['o', 's', 'X', '^', '+', '8']
#print("SHIFT[1:] ",SHIFT[1:])
#6.4, 4.8
plt.figure(figsize=(10, 10))
x = 0
for i in R:
      #print("iiiiiiiiiiiiiiii ",i)
      #print("K ",K)
      #print("RBO_dict[i] ",RBO_dict[i])
      #print("marker[i] ",marker[i-2])
      #print("colors[i] ",colors[i-2])
      plt.plot(K, RBO_dict[i], label = 'R = '+ str(i), marker = marker[x], markersize = 15, color=colors[x])
      x+=1




#add x-axis values to plot
plt.xticks(ticks=K, rotation=45, fontsize=25)
plt.yticks(rotation=45, fontsize=25)



plt.xlabel("k", fontsize=30)
plt.ylabel("Rank-biased overlap (RBO)", fontsize=30)
plt.xlim(left=0)
plt.ylim(bottom=0)
plt.legend(prop={'size':20})
plt.show()


#x-axis is shift length S
print("RBO_dict  RBO_dict ",RBO_dict)
# k_top = 3
# RBOO = []
# for i in R:
#         RBOO.append(RBO_dict[i][k_top-1])
        
# print("RBOO[j]  ",RBOO)
# plt.figure(figsize=(10, 10))
# plt.plot(R, RBOO, label = 'k = '+ str(k_top), marker = marker[0], markersize = 15, color='dimgrey')

k_top = [1, 2, 3, 4, 5, 6]
RBOO = {}
RBO_temp = []
for j in k_top:
    #print("jjjjjjjjjjjjjj ",j)
    for i in R:
        RBO_temp.append(RBO_dict[i][j-1])
    RBOO[j] = RBO_temp
    RBO_temp = []
        
print("RBOO[j]  ",RBOO)
plt.figure(figsize=(10, 10))
x = 0
for j in k_top:
    plt.plot(R, RBOO[j], label = 'k = '+ str(j), marker = marker[x], markersize = 15, color=colors[x])
    x+=1
    
plt.xticks(ticks=R, rotation = 45, fontsize = 25)
plt.yticks(rotation = 45, fontsize = 25)
plt.xlim(left=0)
plt.ylim(bottom=0)

plt.xlabel("Subsequence length (R)", fontsize = 30)
plt.ylabel("Rank-biased overlap (RBO)", fontsize = 30)
plt.legend(labelcolor = 'k', fontsize = 30)
plt.show()

                
                
                    




      
        
            
            
            
            
            
        
        
        
        
        
        
        
        
        
    
