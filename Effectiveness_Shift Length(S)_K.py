# -*- coding: utf-8 -*-
"""
Created on Fri Apr  7 08:43:57 2023

@author: Win10
"""
#Calculate number of operations and savings for linear, pane, and pair
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.spatial import distance
import math
import collections

#Pane Window Technique
L = [500]  #Time series data length
R = [20]
#SHIFT = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
#SHIFT = [1, 2]
SHIFT = [2, 6, 8, 12]
#SHIFT = [1, 2, 3]
K = [1, 2, 3, 4, 5, 6, 7]
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


data = pd.read_csv('E:\\PHD\\Thesis\\UAE_US_residential_ALL_DATASET.csv')
#print(data)
UAE_ACTUALL = data['UAE_residential'].iloc[ : L[0]]
US_ACTUALL = data['US_residential'].iloc[ : L[0]]

UAE_ACTUAL = data['UAE_residential'].iloc[ : L[0]]
US_ACTUAL = data['US_residential'].iloc[ : L[0]]
# print("type of ",type(US_ACTUALL))
# UAE_ACTUAL = pd.DataFrame({'A' : []})
# US_ACTUAL = pd.DataFrame({'A' : []})
#df = pd.concat([UAE_ACTUAL, US_ACTUAL])
#min_1 = df.min()
#max_1 = df.max()

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
        UAE_ACTUALL = data['UAE_residential'].iloc[ : n]
        US_ACTUALL = data['US_residential'].iloc[ : n]
                
        #Data after normalization
        #UAE_ACTUAL = (UAE_ACTUAL-min_1)/(max_1-min_1)
        #US_ACTUAL = (US_ACTUAL-min_1)/(max_1-min_1)
        #print(UAE_ACTUAL, US_ACTUAL)
        #print(len(UAE_ACTUAL))
        #print(len(US_ACTUAL))

        for l in R:
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
                    if (min_1 == max_1):
                        UAE_ACTUAL[i*sh:l+i*sh] = UAE_ACTUALL[i*sh:l+i*sh]
                    else:
                        UAE_ACTUAL[i*sh:l+i*sh] = (UAE_ACTUALL[i*sh:l+i*sh]-min_1)/(max_1-min_1)

                    #Second subsequence
                    min_2 = US_ACTUALL[i*sh:l+i*sh].min()
                    max_2 = US_ACTUALL[i*sh:l+i*sh].max()
                    #print("min_2 ",min_2)
                    #print("max_2 ",max_2)
                    if (min_2 == max_2):
                        UAE_ACTUAL[i*sh:l+i*sh] = UAE_ACTUALL[i*sh:l+i*sh]
                    else:                    
                        US_ACTUAL[i*sh:l+i*sh] = (US_ACTUALL[i*sh:l+i*sh]-min_2)/(max_2-min_2)
                    
                    
                    DEV_REF = distance.euclidean(UAE_ACTUAL[i*sh:l+i*sh], US_ACTUAL[i*sh:l+i*sh])
                    #print("DEV_REF ",DEV_REF)
                    #print("UAE_ACTUAL[i*sh:l+i*sh] ",UAE_ACTUAL[i*sh:l+i*sh])
                    #print("US_ACTUAL[i*sh:l+i*sh] ",US_ACTUAL[i*sh:l+i*sh])
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
                
                #Percentage calculation
                per_linear_list.append(oper_linear/(oper_linear))
                per_save_linear_list.append(0/(oper_linear))
                per_oper_pane_list.append(oper_pane/(oper_linear))
                per_save_pane_list.append(save_pane/(oper_linear))
                per_oper_pair_list.append(oper_pair/(oper_linear))
                per_save_pair_list.append(save_pair/(oper_linear))             
                

# if len(DEV_REF_list) == len(DEV_list):
#     print("The lists of linear have the same length")               
# if DEV_REF_list == DEV_list:
#     print("The lists of linear are identical")  
 
print("oper_linear ",oper_linear_list)    #We need to plot it
print("save_linear ",save_linear_list)    #We need to plot it
#print("DEV_REF_dict ",DEV_REF_dict)  
#print("DEV_dict ",DEV_dict)   
# if DEV_REF_dict == DEV_dict:
#     print("The dicts of linear are identical") 
    
# if DEV_pane_list == DEV_list:
#     print("The lists of pane and linear are identical") 
    
print("oper_pane ",oper_pane_list)    #We need to plot it
print("save_pane ",save_pane_list)    #We need to plot it
#print("DEV_pane_dict ",DEV_pane_dict)
# if DEV_pane_dict == DEV_dict:
#      print("The dicts of pane and linear are identical")     


# if DEV_pane_list == DEV_pair_list:
#      print("The lists of pane and pair are identical")        
            
print("oper_pair ",oper_pair_list)    #We need to plot it
print("save_pair ",save_pair_list)    #We need to plot it
#print("DEV_pair_dict ",DEV_pair_dict)
# if DEV_pane_dict == DEV_pair_dict:
#      print("The dicts of pane and pair are identical") 

print("per_linear_list ", per_linear_list)
print("per_save_linear_list ", per_save_linear_list) 
print("per_oper_pane_list ", per_oper_pane_list)
print("per_save_pane_list ", per_save_pane_list) 
print("per_oper_pair_list ", per_oper_pair_list)  
print("per_save_pair_list ", per_save_pair_list)  


#Plotting
plt.figure(figsize=(10, 10))
#Total Number of operations
ticks = list(range(0,1300,200))

plt.plot(SHIFT_list, oper_linear_list, label='Linear Search', marker = 'o',color = 'r')
plt.plot(SHIFT_list, oper_pane_list, label='OptVRPane Technique', marker = 's',color = 'b')
#plt.plot(SHIFT_list, oper_pair_list, label='OptVRPair Technique', marker = '^',color = 'g')

#add x-axis values to plot
plt.xticks(ticks=SHIFT_list, labels=SHIFT_list, rotation=45)
plt.yticks( rotation=45)


plt.xlabel("Shift Length (S)", fontsize = 13)
plt.ylabel("Number of operations", fontsize = 13)
#plt.title("Time series data length N = 500 and subsequence length (L = 20)")
plt.ylim(bottom=0)
plt.legend()
plt.show()

print("_-------------------------------------------------------------------------------")
plt.figure(figsize=(10, 10))
#Total Number of savings
plt.plot(SHIFT_list, save_linear_list, label='Linear Search', marker = 'o',color = 'r')
plt.plot(SHIFT_list, save_pane_list, label='OptVRPane Technique', marker = 's',color = 'b')
#plt.plot(SHIFT_list, save_pane_list, label='OptVRPair Technique', marker = '^',color = 'g')

#add x-axis values to plot
plt.xticks(ticks=SHIFT_list, labels=SHIFT_list, rotation=45)
plt.yticks(rotation=45)


plt.xlabel("Shift Length (S)", fontsize = 13)
plt.ylabel("Number of saved operations", fontsize = 13)
#plt.title("Time series data length N = 500 and subsequence length (L = 20)")
plt.legend()
plt.show()


plt.figure(figsize=(10, 10))
#Percentage Number of operations
plt.plot(SHIFT_list, per_linear_list, label='Linear Search', marker = 'o',color = 'r')
plt.plot(SHIFT_list, per_oper_pane_list, label='OptVRPane Technique', marker = 's',color = 'b')
#plt.plot(SHIFT_list, per_oper_pair_list, label='OptVRPair Technique', marker = '^',color = 'g')

#add x-axis values to plot
plt.xticks(ticks=SHIFT_list, labels=SHIFT_list, rotation=45)
plt.yticks(rotation=45)


plt.xlabel("Shift Length (S)", fontsize = 13)
plt.ylabel("Normalized Number of operations \n vs. Linear Search", fontsize = 13)
#plt.title("Time series data length N = 500 and subsequence length (L = 20)")
plt.xlim(left=0)
plt.ylim(bottom=0)
plt.legend()
plt.show()

plt.figure(figsize=(10, 10))
#Percentage Number of savings
plt.plot(SHIFT_list, per_save_linear_list, label='Linear Search', marker = 'o',color = 'r')
plt.plot(SHIFT_list, per_save_pane_list, label='OptVRPane Technique', marker = 's',color = 'b')
#plt.plot(SHIFT_list, per_save_pair_list, label='OptVRPair Technique', marker = '^',color = 'g')

#add x-axis values to plot
plt.xticks(ticks=SHIFT_list, labels=SHIFT_list, rotation=45)
plt.yticks(rotation=45)



plt.xlabel("Shift Length (S)", fontsize = 13)
plt.ylabel("Normalized Number of savings \n vs. Linear Search", fontsize = 13)
#plt.title("Time series data length N = 500 and subsequence length (L = 20)")
plt.legend()
plt.show() 

print("DEV_dict ",DEV_dict)   
print("DEV_pane_dict ",DEV_pane_dict)   
print("DEV_pair_dict ",DEV_pair_dict) 


#Calculation For RBO with different shift length values R=20
#SHIFT = [1, 2, 3, 4, 5, 6]
print("views for different shift lengths ", views_dict) 

#How to get views when shift length S = 1
views_S1 = list(views_dict.values())[0]
print("For S=1 ",list(views_dict.values())[0])

#RBO of S=1 is 1.0
RR = []
for i in K:
    RR.append(1)
RBO_dict[1] = RR

#Get the views for other shift lengths
for sh in SHIFT[1:]:
    #print("shift length ",sh)  
    #print("for other shift lengths ",views_dict[sh])  

    #We need to focus on top-k views only        
    for i in K:
        #print("K========= ",i)
        #Transform values from views to subsequence (start, end)
        #print(views_S1[:i])
        views_S1_K = views_S1[:i]
        views_S1_transform = [[(i-1)*1+1,(i-1)*1+R[0]]for i in views_S1_K]
        #print("views_S1_transform ",views_S1_transform)
        #print(views_dict[sh][:i])
        views_dict_sh = views_dict[sh][:i]
        views_dict_transform = [[(i-1)*sh+1,(i-1)*sh+R[0]]for i in views_dict_sh]
        #print("views_dict_transform ",views_dict_transform)
    #print("---------------------------------------------------")        
            
        #Calculate RBO for views_S1_transform and views_dict_transform
        #print("lennnnn ",len(views_dict_transform))
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
        #print("merge ",merge) 
    
        #Ready to calculate RBO
        
        #For first term
        x_k = 0
        #print(len(merge.keys()))
        for i in range (1, len(merge.keys())+1, 1):  
            #print(merge[i])
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
        #print("first_term ",first_term)
        
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
            #print("second_term ",second_term)
            sum_term_k = 0
        #print("second_termxx ",second_term)
        second_term_final = ((1-p)/p)*second_term
        #print("second_term_final ",second_term_final)
        RBO = first_term + second_term_final
        #print("RBOOOOOOO ",RBO)
        
        RBO_list.append(RBO)
    RBO_dict[sh] = RBO_list
    #print("RBO_list ",RBO_list) 
    RBO_list = []
    merge = {}
                             
#print("RBO_dict ",RBO_dict)  

#Plotting
colors = ['r','g','b','c', 'm', 'y']
marker= ['o', 's', 'X', '^', '+', '8']
#print("SHIFT[1:] ",SHIFT[1:])
#6.4, 4.8
plt.figure(figsize=(10, 10))
for i in SHIFT:
      #print("K ",K)
      #print("RBO_dict[i] ",RBO_dict[i])
      #print("marker[i] ",marker[i-2])
      #print("colors[i] ",colors[i-2])
      plt.plot(K, RBO_dict[i], label = 'S = '+ str(i), marker = marker[i-2], markersize = 15, color=colors[i-2])    

#add x-axis values to plot
plt.xticks(ticks=K, rotation = 45, fontsize = 25)
plt.yticks(rotation = 45, fontsize = 25)



plt.xlabel("k", fontsize = 30)
plt.ylabel("Rank-biased overlap (RBO)", fontsize = 30)
plt.xlim(left=0)
plt.ylim(bottom=0)
plt.legend(prop={'size':20})
plt.show()

#x-axis is shift length S
k_top = 3
RBOO = []
for i in SHIFT:
    RBOO.append(RBO_dict[i][k_top-1])
print("RBOO ",RBOO)
plt.figure(figsize=(10, 10))
plt.plot(SHIFT, RBOO, label = 'k = '+ str(k_top), marker = marker[0], markersize = 15, color='dimgrey')
    
plt.xticks(ticks=SHIFT, rotation = 45, fontsize = 25)
plt.yticks(rotation = 45, fontsize = 25)
#plt.xlim(left=0)
#plt.ylim(bottom=0)

plt.xlabel("Shift length (S)", fontsize = 30)
plt.ylabel("Rank-biased overlap (RBO)", fontsize = 30)
plt.xlim(left=0)
plt.ylim(bottom=0)
plt.legend(labelcolor = 'k', fontsize = 30)
plt.show()



#Scatter Plot
ticks = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
print("##################################################################")
print("per_save_pane_list ", per_save_pane_list) 
print("RBO_dict ",RBO_dict) 

labels = []
plt.figure(figsize=(10, 10))
for i in SHIFT[1:]:
    k = 1
    
    #print("per_save_pane_list[i-1] ",per_save_pane_list[i-1])
    for Y in RBO_dict[i]:
        #print("Y[n] ",Y)
        scatter = plt.scatter(per_save_pane_list[i-1], Y, label = "S = "+str(i), color=colors[i-2], marker = marker[i-2], s = 300)
        plt.text(per_save_pane_list[i-1], Y, 'k = '+str(k), va='center', ha='center', fontsize = 10)
        k+=1
    labels.append("S = "+str(i))
        
    #plt.scatter(per_save_pane_list[i-1], RBO_dict[i], color=colors[i-2])
             
#add x-axis values to plot
plt.xticks(ticks=ticks, rotation=45, fontsize=20)
plt.yticks(ticks=ticks, rotation=45, fontsize=20)

plt.xlabel("Normalized Number of savings \n vs. Linear Search", fontsize=24)
plt.ylabel("Rank-biased overlap (RBO)", fontsize=24)
plt.xlim(left=0)
plt.ylim(bottom=0)
#legend = plt.legend(labelcolor = colors, labels = labels)
#plt.legend(prop={'size':20})
#plt.show()            
     

# leg = legend.legendHandles
# for i in range(0, len(colors)-1):
#     print("iiiiiiiiiiiiiiiiiii ",i)
#     leg[i].set_color(colors[i])
#     #leg.legendHandles[i].set_color(colors[i])

f = lambda m,c: plt.plot([],[],marker=m, color=c, ls="none")[0]

#handles = [f("s", colors[i]) for i in range(len(SHIFT))]
handles = [f(marker[i], colors[i]) for i in range(len(SHIFT))]

 
plt.legend(handles, labels, labelcolor = colors, fontsize = 20, markerscale = 2)
            
plt.show()

print("######################################################################")
#Combining Metric (normalized number of savings*RBO) (multiplying)
print("per_save_pane_list ", per_save_pane_list) 
print("RBO_dict ",RBO_dict) 

xticks = [0, 1, 2, 3, 4, 5, 6, 7]
plt.figure(figsize=(10, 10))
metric_dict = {}
for i in SHIFT[1:]:
    #print("iiiiiiiiiiiiiiiii ",i)   
    metric_dict[i] = [(value * per_save_pane_list[i-1]) for value in RBO_dict[i]]

            
print("metric_dict[i] ",metric_dict)        
        
#Plotting
for i in SHIFT[1:]:
    k = 1
    
    #print("per_save_pane_list[i-1] ",per_save_pane_list[i-1])
    for Y in metric_dict[i]:
        #print("Y[n] ",Y)
        scatter = plt.scatter(i, Y, color=colors[i-2], marker = marker[i-2], s = 300)
        plt.text(i, Y, 'k = '+str(k), va='center', ha='center', fontsize = 20)
        k+=1
        
#add x-axis values to plot
plt.xticks(ticks = xticks, rotation=45, fontsize=20)
plt.yticks(ticks=ticks, rotation=45, fontsize=20)

plt.xlabel("SHIFT (S)", fontsize=24)
plt.ylabel("Combine Metric (multiply)", fontsize=24)
plt.xlim(left=0)
plt.ylim(bottom=0)       
        
        
 
print("######################################################################")
ticks = [0, 0.25, 0.5, 0.75,  1, 1.25, 1.5, 1.75, 2]
#ticks = [0, 0.5, 1, 1.5, 2]

#Combining Metric (normalized number of savings+RBO) (addition)
print("per_save_pane_list ", per_save_pane_list) 
print("RBO_dict ",RBO_dict) 

plt.figure(figsize=(10, 10))
metric_dict = {}
for i in SHIFT[1:]:
    #print("iiiiiiiiiiiiiiiii ",i)   
    metric_dict[i] = [(value + per_save_pane_list[i-1]) for value in RBO_dict[i]]

            
print("metric_dict[i] ",metric_dict)        
        
#Plotting
for i in SHIFT[1:]:
    k = 1
    
    #print("per_save_pane_list[i-1] ",per_save_pane_list[i-1])
    for Y in metric_dict[i]:
        #print("Y[n] ",Y)
        scatter = plt.scatter(i, Y, color=colors[i-2], marker = marker[i-2], s = 300)
        plt.text(i, Y, 'k = '+str(k), va='center', ha='center', fontsize = 20)
        k+=1
        
#add x-axis values to plot
plt.xticks(ticks = xticks, rotation=45, fontsize=20)
plt.yticks(ticks = ticks, rotation=45, fontsize=20)

plt.xlabel("SHIFT (S)", fontsize=24)
plt.ylabel("Combine Metric (addition)", fontsize=24)
plt.xlim(left=0)
plt.ylim(bottom=0)       
        
        
    