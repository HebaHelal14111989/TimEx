import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.spatial import distance
import math

#For Global min-max normalization, we change lines 214, 215, 230, 231, 1044, 1045, 1060, 1061
#Horizontal Paned Pruning + Sharing + Integration  (_R)
N = [600]  #Time series data length
#N = [100, 200, 300, 400, 500, 600]  #Time series data length (Maximum size I have is 630)
#L = [20]   #Subsequence length
#L = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]   #Subsequence length
#L = list(range(10,100))
#L = range(5,30)
#L = range(10,100)
#L = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
L = range(5,61)
#L = [20]
#K = 1
#K = 1
#SHIFT = [1, 2, 3, 4, 5]
SHIFT = [6]
#SHIFT = [5, 10, 15, 20]
K = 4  #Default K = 4
DEV_SUB_MAX = []

Pane_Prune_list = []
Pane_Prune_savings_list = []
Pane_no_prune_list = []
Pane_per_prune_list = []
Pane_per_prune_savings_list = []

Pane_L_list = []
Pane_L_dict = {}

Pane_S_list = []
Pane_S_dict = {}

Pane_Prune_dict = {}
Pane_no_prune_dict = {}
Pane_per_prune_dict = {}
Pane_per_prune_savings_dict = {}
Pane_Prune_savings_dict = {}

#Sharing with pane
Pane_share_list = []
Pane_share_savings_list = []
Pane_per_share_list = []
Pane_per_share_savings_list = []

Pane_share_dict = {}
Pane_share_savings_dict = {}
Pane_per_share_dict = {}
Pane_per_share_savings_dict = {}

#Sharing alone
share_pane_list = []
share_pane_savings_list = []
per_share_pane_list = []
per_share_pane_savings_list = []

share_pane_dict = {}
share_pane_savings_dict = {}
per_share_pane_dict = {}
per_share_pane_savings_dict = {}

#seq_list = []
ind_seq_list = 0
vall = []
total_operations = 0
oper_prune = 0
seq_list = []

#Integration
oper_list = []
combine_prune_paned_savings_list = []
combine_prune_paned_savings_dict = {}
per_combine_prune_paned_savings_list = []
per_combine_prune_paned_savings_dict = {}

combine_prune_paned_actual_list = []
combine_prune_paned_actual_dict = {}
per_combine_prune_paned_actual_list = []
per_combine_prune_paned_actual_dict = {}

no_prune_list = []
per_no_prune_list = []
no_prune_dict = {}
per_no_prune_dict = {}

no_prune_savings_list = []
per_no_prune_savings_list = []
no_prune_savings_dict = {}
per_no_prune_savings_dict = {}

data = pd.read_csv('E:\\PHD\\Thesis\\Spring2024\\Dataset\\AE.csv')  #E:\\PHD\\Thesis\\UAE_US_Parks_ALL_DATASET.csv
data1 = pd.read_csv('E:\\PHD\\Thesis\\Spring2024\\Dataset\\AE.csv')


#print(data)
UAE_ACTUAL = data['workplaces'].iloc[ : N[0]]   #UAE_parks  UAE_workplaces
US_ACTUAL = data['residential'].iloc[ : N[0]]    #US_parks   UAE_residential
df = pd.concat([UAE_ACTUAL, US_ACTUAL])
min_1 = df.min()
max_1 = df.max()
#print(min_1, max_1)

#DevList and Dev_ref
length = K
DevList = [-999] * length
Dev_ref = DevList[-1]  #Minimum of the largest deviations
Dev_ref_ind = -1

length = K
initial_value = -999  

Dev_dict = {i+1: initial_value for i in range(length)}
Dev_ref_dict = list(Dev_dict.values())[-1]
print("Dev_dict ",Dev_dict)
print("Dev_ref_dict ",Dev_ref_dict)

def get_value_before_key(dictionary, target_key):
    previous_value = None
    for key in dictionary:
        if key == target_key:
            return previous_value
        previous_value = dictionary[key]
    return None

def get_key_before_key(dictionary, target_key):
    previous_key = None
    for key in dictionary:
        if key == target_key:
            return previous_key
        previous_key = key
    return None

def swap_keys(dictionary, key1, key2):
    if key1 not in dictionary or key2 not in dictionary:
        return dictionary  # Return the original dictionary if either key is not present

    new_dict = dictionary.copy()  # Create a copy of the original dictionary

    # Swap the values associated with key1 and key2
    new_dict[key1], new_dict[key2] = new_dict[key2], new_dict[key1]

    return new_dict

for sh in SHIFT:
    for n in N:
        #n=200
        #Select Data from the begining
        UAE_ACTUALL = data1['workplaces'].iloc[ : n]  #UAE_parks   UAE_workplaces
        US_ACTUALL = data1['residential'].iloc[ : n]  #US_parks    UAE_residential
        df = pd.concat([UAE_ACTUAL, US_ACTUAL])
        #min_1 = df.min()
        #max_1 = df.max()
        #print(min_1, max_1)
        
        
        #Data after normalization
        #UAE_ACTUAL = (UAE_ACTUAL-min_1)/(max_1-min_1)
        #US_ACTUAL = (US_ACTUAL-min_1)/(max_1-min_1)
        #print(UAE_ACTUAL, US_ACTUAL)

        #Core of Pruning with overlap
        for l in L:
            comm = [0] * n
            if((n-l)%sh != 0):
                prune_share = 0
                actual_share = 0
                prune = 0
                prune1 = 0
                oper_prune = 0
                prune_actual = 0
                actual_share = 0
                share_share = 0
                interest = 0
                combine_prune_paned_savings = 0
                combine_prune_paned_actual = 0
            if((n-l)%sh==0 and (n-l)!=0):
                oper_list = []
                combine_prune_paned_savings = 0
                combine_prune_paned_actual = 0
                share_share = 0
                actual_share = 0
                prune = 0
                oper_prune = 0
                Pane_L_list.append(l)
                Pane_S_list.append(sh)
                V = int((n-l)/sh)+1 #Number of views
                print("VIEWSSSSSSSS ",V)
                
                #Calculate size of g
                g = math.gcd(l,sh)
                #Number of panes window
                P = int(l/g)
                print("g is ",g)
                print("P is ",P)
                
                DevList = [-999] * length
                Dev_ref = DevList[-1]  #Minimum of the largest deviations
                Dev_ref_ind = -1

                Dev_dict = {i+1: initial_value for i in range(length)}
                Dev_ref_dict = list(Dev_dict.values())[-1]
                                
                for i in range(1,P+1,1):
                    seq_list.append(g)
                print("seq_listtttttttttttttttttttttt ",seq_list)

                #Data after normalization individually for each subsequence
                #First subsequence
                #min_1 = UAE_ACTUALL[:l].min()
                #max_1 = UAE_ACTUALL[:l].max()
                
                min_1 = UAE_ACTUALL.min()
                max_1 = UAE_ACTUALL.max()
                
                #print("min_1 ",min_1)
                #print("max_1 ",max_1)
                #print("UAE_ACTUALL[:l] b  ",UAE_ACTUALL[:l])
                if (min_1 == max_1):
                    UAE_ACTUAL[:l] = UAE_ACTUALL[:l]
                else:
                    UAE_ACTUAL[:l] = (UAE_ACTUALL[:l]-min_1)/(max_1-min_1)
                #print("UAE_ACTUAL[:l] ",UAE_ACTUAL[:l])

                #Second subsequence
                #min_2 = US_ACTUALL[:l].min()
                #max_2 = US_ACTUALL[:l].max()
                
                min_2 = US_ACTUALL.min()
                max_2 = US_ACTUALL.max()
                
                #print("min_2 ",min_2)
                #print("max_2 ",max_2)
                if (min_2 == max_2):
                    US_ACTUAL[:l] = US_ACTUALL[:l]
                else:                    
                    US_ACTUAL[:l] = (US_ACTUALL[:l]-min_2)/(max_2-min_2)
                #print("US_ACTUAL[:l] ",US_ACTUAL[:l])


                #Deviation of the first subsequence as the reference deviation
                DEV_REF = distance.euclidean(UAE_ACTUAL[:l], US_ACTUAL[:l])
                #DEV_SUB_MAX.append(DEV_REF)
                #print(" DEV_REF ", DEV_REF)
                #oper_list = [seq_list[i]-1 for i in range(len(seq_list))]
                #total_operations+=sum(oper_list)+(len(oper_list)-1)
                #print("111111111111111111111111111111111 ",total_operations)
                
                #Add first deviation to the DevList
                ind_DevList = 0
                DevList[ind_DevList] = DEV_REF                
                print("DevListttt11 ",DevList)
                
                Dev_ref = DevList[-1]
                print("Dev_ref11 ",Dev_ref)
                
                Dev_dict[1] = DEV_REF
                print("Dev_dict11 ",Dev_dict)
                Dev_ref_dict = list(Dev_dict.values())[-1]
                print("Dev_ref_dict11 ",Dev_ref_dict)
                
                
                oper_prune += 2*l-1
                #print("oper_prune ",oper_prune)
                
                actual_share += 2*l-1
                print("actual_share ",actual_share)

                combine_prune_paned_actual+= 2*l-1
                print("combine_prune_paned_actual11 ",combine_prune_paned_actual)


                for x, res in enumerate(comm): 
                    if x in range (0,l):
                        comm[x]=1
                #print("commmmmmm ",comm)
                #pos = 0
                #count_ones = 0
                #Increase ones by the size of g1
                #for j in range(pos, n, sh):
                    #print("jjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj ",j)
                #    count_ones+=1
                #    for c in range(1,seq_list[ind_seq_list]+1, 1):
                #        if(count_ones<=V):
                #            comm[j]=1
                #            j+=1
                #print("commmmmmm ",comm)
                print("-------------------------------------------------------")
                print("commmmmmm ",comm)
                val_reserve = 0
                chh = False
                
                oper_list.append(l-1)
                
                for i in range(1 , V , 1):   #V
                
                    if ind_DevList < K-1:
                        ind_DevList += 1
                    
                
                    print("viewwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww ",i+1)
                    
                    #print("seq_listtttttttttttttttttttttt of each view from the second view ",seq_list)
                    ind_seq_list = 0
                    val = []

                    #Data after normalization individually for each subsequence
                    #First subsequence
                    min_1 = UAE_ACTUALL[i*sh:l+i*sh].min()
                    max_1 = UAE_ACTUALL[i*sh:l+i*sh].max()
                    #print("min_1 ",min_1)
                    #print("max_1 ",max_1)
                    #print("UAE_ACTUALL[i*sh:l+i*sh] b  ",UAE_ACTUALL[i*sh:l+i*sh])
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
                        US_ACTUAL[i*sh:l+i*sh] = US_ACTUALL[i*sh:l+i*sh]
                    else:                    
                        US_ACTUAL[i*sh:l+i*sh] = (US_ACTUALL[i*sh:l+i*sh]-min_2)/(max_2-min_2)
                    #print("US_ACTUAL[i*sh:l+i*sh] ",US_ACTUAL[i*sh:l+i*sh])                    
                    
                    
                    #print("iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii", i)
                    #print("DEV_REF ",DEV_REF)
                    #j = [i*SHIFT:l+1+i*SHIFT]
                    #print(j)
                    #print(type(j))
                    #if comm[j]==1:
                    #    print("YESSSS")
                    
                    ###################################################
                    #Change seq_list
                    seq_list = []
                    #print("commmmmzzzz ",comm)
                    #print("seq_listzzz ",seq_list)
                    for j in range(i*sh,l+i*sh,g):
                        
                        if comm[j]==1:
                            #print("jjjjj ",j)
                            seq_list.append(g)
                        else:
                            seq_list.append(0)
                    
                    #print("seq_listbbbbbbb ",seq_list)
                    
                    #####################################################
                    
                    for j in range(i*sh,l+i*sh,1):
                        #print(j)
                        
                        if comm[j]==1:
                            val.append(j)
                            #print("YESSSS")
                            
                    print(val)
                    #print("seq_listcccccccc ",seq_list)
                    #Special case if val = []
                    if (len(val)==0):
                        for u in range(i*sh,seq_list[0]+i*sh,1):
                            comm[u]=1
                            val.append(u)
                    print("valllllllll ",val)        
                    #print("oper_listtttt ",oper_list)
                    
                    #Calculate sharing
                    if (len(val)==0):
                        chh = True
                        share_share += 0
                        actual_share += 0
                    else:
                        chh = False
                        sha = val[-1] - val[0] + 1
                        # if sha == g:
                        #     share_share += sha 
                        #     print("share_share11aa ", share_share)
                        #     #actual_share += 1
                        #     #print("actual_share11 aa  ",actual_share)
                        # else:    
                        share_share += sha + (sha/g)*(g-1)
                        #print("share_share11 ", share_share)
                        
                        if (sha/g)>=1:
                            actual_share += (sha/g)-1
                        #print("actual_share11bbb ",actual_share)
                    print("share_sharerrrrr ",share_share)
                    print("actual_sharerrrr ",actual_share)
                    #print(val[-1])
                    #print(UAE_ACTUAL[val[0]:val[-1]+1])
                    #print(US_ACTUAL[val[0]:val[-1]+1])
                    #print(l-len(val))
                    #print("viewwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwzzzz ",i+1)
                    print("chhhhhhhhhhhhhhhhhhhhhhhh ",chh)
                    print("(l-(l-len(val))) + ((l-(l-len(val)))-1) ",(l-(l-len(val))) + ((l-(l-len(val)))-1))
                    #oper_prune += (l-(l-len(val))) + ((l-(l-len(val)))-1)
                    while ((l-len(val))>=0):
                        # if (len(val)==0):
                        #     break
                        #     DEV_SUB = np.sqrt(l)
                        #     print("DEV_SUB1 ",DEV_SUB)
                        #     val.append(i*sh)
                        #     #comm[i*sh]=1
                            
                        if (len(val) > 0):
                            #print("UAE_ACTUAL[val[0]:val[-1]+1] ",UAE_ACTUAL[val[0]:val[-1]+1])
                            DEV_SUB = np.sqrt(np.sum(np.square(UAE_ACTUAL[val[0]:val[-1]+1]-US_ACTUAL[val[0]:val[-1]+1]))+(l-len(val)))
                            #print("DEV_SUB2222 ",DEV_SUB)
                            #oper_prune += len(vall)
                            if (len(UAE_ACTUAL[val[0]:val[-1]+1])!=l and DEV_SUB >= Dev_ref):

                                # if i == 1:
                                #     Dev_ref = DevList[ind_DevList-1]
                                #     print("Dev_ref22aa ",Dev_ref)
                                    
                                #     if K == 1:
                                #         #Dev_dict[i+1] = DEV_SUB
                                #         print("Dev_dict22aa ",Dev_dict)
                                #         Dev_ref_dict = list(Dev_dict.values())[-1]
                                #         print("Dev_ref_dict22aa ",Dev_ref_dict) 
                                #     else:
                                #         #Dev_dict[i+1] = DEV_SUB
                                #         print("Dev_dict22bb ",Dev_dict)
                                #         Dev_ref_dict = list(Dev_dict.values())[-2]
                                #         print("Dev_ref_dict22bb ",Dev_ref_dict)   
                                # else:
                                    
                                #DevList[ind_DevList] = DEV_SUB
                                #print("DevListttt22 ",DevList)
                                    
                                Dev_ref = DevList[ind_DevList]
                                #print("Dev_ref22bb ",Dev_ref)
                                
                                #Dev_dict[i+1] = DEV_SUB
                                #print("Dev_dict22 ",Dev_dict)
                                
                                Dev_ref_dict = list(Dev_dict.values())[-1]
                                #print("Dev_ref_dict22 ",Dev_ref_dict)                                
                            
                                
                                                                
                            if (len(UAE_ACTUAL[val[0]:val[-1]+1])==l and DEV_SUB >= Dev_ref):
        
                                Dev_ref = DEV_SUB
                                DevList[ind_DevList] = DEV_SUB
                                print("DevListttt33 ",DevList)
                                print("Dev_ref33 ",Dev_ref)
                                
                                #Swapping
                                # if DevList[ind_DevList-1] < DevList[ind_DevList]:
                                #     temp = DevList[ind_DevList-1]
                                #     DevList[ind_DevList-1] = DEV_SUB
                                #     DevList[ind_DevList] = temp
                                #     print("DevListttt33 ",DevList)
                                DevList.sort(reverse=True)
                                print("DevListttt33 ",DevList)
                                
                                if (i+1) > K:
                                    Dev_dict.popitem()
                                Dev_dict[i+1] = DEV_SUB
                                print("Dev_dict33aa ",Dev_dict)
                                
                                #Swapping
                                Dev_dict = dict(sorted(Dev_dict.items(), key=lambda item: item[1], reverse=True))
                                print("DevListttt33bb ",DevList)
                                # value_before = get_value_before_key(Dev_dict, i+1)
                                # print("value_before ",value_before)
                                # key_before = get_key_before_key(Dev_dict, i+1)
                                # print("key_before ",key_before)
                                
                                # if Dev_dict[i+1] > value_before:
                                #     Dev_dict = swap_keys(Dev_dict, key_before, i+1)
                                #     print("Dev_dict33bb ",Dev_dict)
                                #     temp1 = Dev_dict[i+1]
                                #     Dev_dict[i+1] = DEV_SUB
                                #     Dev_dict[key_before] = temp1
                                #     print("DevListttt33bb ",DevList)
                                
                                Dev_ref_dict = list(Dev_dict.values())[-1]
                                print("Dev_ref_dict33 ",Dev_ref_dict)
                                
                                
                                #print("subsequence {} saves {}".format(i+1,0))
                                oper_prune +=  2*l-1
                                #print("oper_prune ",oper_prune)
                                #max_value = max(DEV_SUB_MAX)
                                #max_index = DEV_SUB_MAX.index(max_value)
                                #interest = max_index+1

                                if ((oper_list[i-1]-val[0]+1)+(((oper_list[i-1]-val[0]+1)/g)*(g-1)))>=0:
                                    combine_prune_paned_savings+= ((oper_list[i-1]-val[0]+1)+(((oper_list[i-1]-val[0]+1)/g)*(g-1)))
                                #combine_prune_paned_savings+=1
                                print("combine_prune_paned_savings22 ",combine_prune_paned_savings)  
                                #print("((oper_list[i-1]-val[0]+1)/g)-1 ",(((abs(oper_list[i-1]-val[0])+1)/g)-1))
                                if ((oper_list[i-1]-val[0]+1)/g) >= 1:
                                    combine_prune_paned_actual += (((oper_list[i-1]-val[0]+1)/g)-1)
                                    combine_prune_paned_actual+= 1
                                # else:
                                #     combine_prune_paned_savings += (2*((oper_list[i-1]-val[0]+1)/g)-1)
                                #combine_prune_paned_actual+= 1
                                
                                combine_prune_paned_actual+=(val[-1]-oper_list[i-1])+((val[-1]-oper_list[i-1])-1)
                                #if chh == True:
                                
                                print("combine_prune_paned_actual22 ",combine_prune_paned_actual)
                                
                                break
                                
                                    
                            if (DEV_SUB < Dev_ref):
                                # DEV_SUB_MAX.append(DEV_SUB)
                                # if (max(DEV_SUB_MAX) >DEV_SUB):
                                #     max_index = DEV_SUB_MAX.index(max(DEV_SUB_MAX))
                                #     interest = max_index+1
                                # else:
                                #     interest = 1
                                if(l-len(val)==0):
                                    #DevList[ind_DevList] = DEV_SUB
                                    print("DevListttt44 ",DevList)
                                    
                                    Dev_ref = DevList[ind_DevList]
                                    print("Dev_ref44 ",Dev_ref)
                                    
                                    #Dev_dict[i+1] = DEV_SUB
                                    print("Dev_dicttt44 ",Dev_dict)
                                    
                                    Dev_ref_dict = list(Dev_dict.values())[-1]
                                    print("Dev_ref_dict44 ",Dev_ref_dict)
                                    
                                    #print("subsequence {} saves {} vvvvv".format(i+1,(l-len(val))))
                                    prune +=(l-len(val))
                                    oper_prune += 2*l-1
                                    #print("oper_prune ",oper_prune)

                                    combine_prune_paned_savings+=(l-len(val))
                                    if ((oper_list[i-1]-val[0]+1)+(((oper_list[i-1]-val[0]+1)/g)*(g-1)))>=0:
                                        combine_prune_paned_savings+= ((oper_list[i-1]-val[0]+1)+(((oper_list[i-1]-val[0]+1)/g)*(g-1)))
                                    #combine_prune_paned_savings+= 1
                                    
                                    #combine_prune_paned_actual+=(l-((l-sh)+(l-len(val))))+((l-((l-sh)+(l-len(val))))-1)
                                    
                                    combine_prune_paned_actual += (val[-1]-oper_list[i-1])+((val[-1]-oper_list[i-1])-1)
                                    #if (val[-1]-oper_list[i-1]) > 0:
                                    
                                    #print("(((oper_list[i-1]-val[0]+1)/g)-1)22 ",(((abs(oper_list[i-1]-val[0])+1)/g)-1))
                                    if ((oper_list[i-1]-val[0]+1)/g) >= 1:
                                        combine_prune_paned_actual += (((oper_list[i-1]-val[0]+1)/g)-1)
                                        combine_prune_paned_actual += 1
                                    # else:
                                    #     combine_prune_paned_savings += (2*((oper_list[i-1]-val[0]+1)/g)-1)
                                    #combine_prune_paned_actual += 1
                                    print("combine_prune_paned_actual33 ",combine_prune_paned_actual)
                                    print("combine_prune_paned_savings33 ",combine_prune_paned_savings)

                                    # actual_share += 1
                                    # print("actual_share2222aa ",actual_share)
                                    break
                                else:
                                    #print("subsequence {} saves {} xxxxxxx".format(i+1,(l-len(val))+((l-len(val))-1)))
                                    #if chh == True :
                                    prune +=(l-len(val))+((l-len(val))-1)
                                    prune +=1
                                    print("prune ",prune)
                                    print("prune points ",(l-len(val)))
                                    #prune +=(l-len(val))
                                    #oper_prune += (l-(l-len(val))) + (l-((l-len(val))-1))-1
                                    oper_prune += (l-(l-len(val))) + ((l-(l-len(val)))-1)
                                    #print("oper_prune ",oper_prune)
                                    
                                    actual_share += (l-len(val))+((l-len(val))-1)
                                    #print("actual_share2222bbzzzzzzzzz ",actual_share)
                                    # if (len(val)==0):
                                    #     print("noooooooooooooooooooooooo")
                                    if chh == False : 
                                        actual_share += 1
                                    print("actual_share2222bb ",actual_share)
                                    #ind_comm_one = {x:i for i,x in enumerate(comm)}
                                    # d = collections.OrderedDict()
                                    # for z,v in enumerate(comm):
                                    #     if (v==1):
                                    #         d[v] = z
                                    # print("index of last one in commmm ",list(d.values()))
                                    # ind_comm_one = list(d.values())
                                    # for x in range(ind_comm_one[0],l+i*sh,1):
                                    #     #print("xxxxxxxxxxxxxxxxxxxxxx ",x)
                                    #     if (comm[x]!=1):
                                    #         comm[x]=1
                                    # print("commmmnnnnnnxx 0",comm)
                                    
                                    
                                    #print("oper_list[i-1] ",oper_list[i-1])
                                    print("val[0] ",val[0])
                                    #print("((oper_list[i-1]-val[0]+1)+(((oper_list[i-1]-val[0]+1)/g)*(g-1))) ",((oper_list[i-1]-val[0]+1)+(((oper_list[i-1]-val[0]+1)/g)*(g-1))))
                                    combine_prune_paned_savings+=(l-len(val))+((l-len(val))-1)
                                    #if chh == True :
                                    combine_prune_paned_savings+=1
                                    if ((oper_list[i-1]-val[0]+1)+(((oper_list[i-1]-val[0]+1)/g)*(g-1)))>=0:
                                        combine_prune_paned_savings+= ((oper_list[i-1]-val[0]+1)+(((oper_list[i-1]-val[0]+1)/g)*(g-1)))      
                                    #combine_prune_paned_savings+=1
                                    #if (val[-1]-oper_list[-1])>0:
                                    #print("oper_list@@@ ",oper_list[-1])
                                    #print("vall@@@ ",val[-1])
                                    print("(val[-1]-oper_list[-1])ffff ",(val[-1]-oper_list[-1]))
                                    print("(i-1)*sh ",i*sh)
                                    if oper_list[-1] < i*sh-1:
                                       oper_list[-1] = i*sh-1
                                    combine_prune_paned_actual += (val[-1]-oper_list[-1])+((val[-1]-oper_list[-1])-1)
                                    #if chh == False:
                                    #if (val[-1]-oper_list[i-1]) > 0:
                                    
                                    #if (((oper_list[i-1]-val[0]+1)/g)-1) > 0:
                                    print("(oper_list[i-1]-val[0])xxxxxx ",(oper_list[i-1]-val[0]))
                                    if ((oper_list[i-1]-val[0]+1)/g) >= 1:
                                        combine_prune_paned_actual += (((oper_list[i-1]-val[0]+1)/g)-1)
                                        combine_prune_paned_actual += 1
                                    # elif (oper_list[i-1]-val[0]) < 0:
                                    #     combine_prune_paned_savings += (2*((oper_list[i-1]-val[0]+1)/g)-1)
                                    #if (((oper_list[i-1]-val[0]+1)/g)-1) == 0:
                                    #    combine_prune_paned_actual += 1
                                    # if chh == False : 
                                    #     combine_prune_paned_actual += 1
                                    print("combine_prune_paned_actual44b ",combine_prune_paned_actual)
                                    print("combine_prune_paned_savings44b ",combine_prune_paned_savings) 

                                    
                                    break
                                #print("subsequence {} saves {}".format(i+1,(l-len(val))))
                                #prune +=(l-len(val))
                                #break

                        # if (len(val)==0):
                        #     #DEV_SUB = np.sqrt(l)
                        #     #print("DEV_SUB ",DEV_SUB)
                        #     val.append(i*sh)
                        #     comm[i*sh]=1
                        


                        #We have to put this here
                        if 0 in seq_list:
                            # Find the index of the first zero in the list
                            ind_zero = seq_list.index(0)
                            
                        #print("ind_zero ",ind_zero)    
                        
                        seq_list[ind_zero] = g
                        ########################################
                        
                        if (len(val)==0):
                            #chh = True
                            cc = i*sh-1
                            for m in range(1,g+1,1):
                                cc+=1
                                vall.append(cc)
                                
                        else:
                            cc = val[-1]
                            for m in range(1,seq_list[ind_seq_list]+1,1): 
                                cc+=1
                                vall.append(cc)
                                #cc+=1

                        #print("vall ", vall)
                                                

                        # if 0 in seq_list:
                        #     # Find the index of the first zero in the list
                        #     ind_zero = seq_list.index(0)
                            
                        # print("ind_zero ",ind_zero)    
                        
                        # seq_list[ind_zero] = g                        
                        
                        total_operations +=seq_list[ind_seq_list]-1
                        val.extend(vall)
                        #print("seq_list after increase ",seq_list)
                        #print("val after increase", val)
                        #print(comm[vall])
                        for x in range(0,len(vall),1): 
                            if (comm[vall[x]]!=1):
                                comm[vall[x]]=1
                            
                        #print("comm ",comm)
                        
                        val_reserve = val[-1]
                        #print("val_reserve ",val_reserve)
                        
                        vall = []
                        ind_seq_list+=1
                        print("vallllllllllllllll ",val)
                        if (len(val) > 0): 
                            #if (DEV_SUB<DEV_REF):
                                actual_share += 2*g-1 
                                #if(l-len(val)!=0):
                                    
                                if chh == False:
                                    actual_share += 1
                                    
                            
                                    #print("actual_share333cccc11 ",actual_share)
                                if (chh == True and l-len(val)!=0):
                                    actual_share += 1
                        print("actual_share333cccc22 ",actual_share)  
                    print("combine_prune_paned_savingsffffff ",combine_prune_paned_savings)
                    print("combine_prune_paned_actualfffffffff ",combine_prune_paned_actual)
                                    
                    total_operations +=len(seq_list)-2
                    #print("222222222222222222222222222222222222222222222222 ",total_operations)
                    #chh = False
                    #Change seq_list
                    seq_list = []
                    #print("commmmmzzzz ",comm)
                    #print("seq_listzzz ",seq_list)
                    for j in range(i*sh,l+i*sh,g):
                        
                        if comm[j]==1:
                            #print("jjjjj ",j)
                            seq_list.append(g)
                        else:
                            seq_list.append(0)
                    
                    #print("seq_listafterrrrrrrrrr ",seq_list)
                    #print("commm ",comm)
                    
                    oper_list.append(val[-1])
                    print("oper_list ",oper_list)
                    
                    #print("seq_listttttttttttttttttttttttendddddddddd ",seq_list)
                    print("-------------------------------------------------------------------------------------") 
                    
                print("DevListtttttttttttttttttttt ",DevList)
                print("Dev_dicttttttttttttttttttttt ",Dev_dict)
                #print("DEV_SUB_MAX ",DEV_SUB_MAX)
                print("DevList_Final ",DevList)
                #DEV_SUB_MAX.clear()
                DevList.clear()
                Dev_dict.clear()
                #print("DEV_SUB_MAX afterrrrrrrrrrrrrrr ",DEV_SUB_MAX)
                print("Total number of pruning ,",prune)
                Pane_Prune_savings_list.append(prune)  #Saved
                print("Total number of operation pruning ,",oper_prune)
                Pane_Prune_list.append(oper_prune)   #Operations
                no_prune = (l+(l-1))*V
                Pane_no_prune_list.append(no_prune)
                Pane_per_prune_savings_list.append(prune/(no_prune)*100)  #Per_Saved
                Pane_per_prune_list.append(oper_prune/(no_prune)*100)     #Per_Operations                 
                Pane_share_list.append(actual_share)
                Pane_share_savings_list.append(share_share)
                Pane_per_share_list.append(actual_share/(no_prune)*100)
                Pane_per_share_savings_list.append(share_share/(no_prune)*100)

                combine_prune_paned_savings_list.append(combine_prune_paned_savings)
                combine_prune_paned_actual_list.append(combine_prune_paned_actual)

                no_prune = (l+(l-1))*V
                no_prune_list.append(no_prune)
                per_no_prune_list.append((no_prune/no_prune)*100)
                no_prune_savings_list.append(0)
                per_no_prune_savings_list.append((0/no_prune)*100)
                
                
                #Code of sharing Number of operations using Paned Window
                g = math.gcd(l,sh)
                P = l/g
                share_pane_list.append((l+(l-1))+((2*sh-1+(l/g)-(sh/g))*(V-1)))
                per_share_pane_list.append(((l+(l-1))+((2*sh-1+(l/g)-(sh/g))*(V-1)))/(no_prune)*100)


                #Code of sharing Number of savings using Paned Window
                g = math.gcd(l,sh)
                P = l/g 
                #print("VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV ",V)
                #print("((l-sh)+(((l-sh)/g)*(g-1))+(((l-sh)/g)-1)*(V-1))  ",((l-sh)+(((l-sh)/g)*(g-1))+(((l-sh)/g)-1)))
                share = ((l-sh)+((l-sh)/g)*(g-1))
                tot_share = share*(V-1)
                #print(tot_share)
                share_pane_savings_list.append(tot_share)
                per_share_pane_savings_list.append(tot_share/(no_prune)*100)
                                      
        per_combine_prune_paned_actual_list = [combine_prune_paned_actual_list[i] / Pane_no_prune_list[i] for i in range(len(Pane_no_prune_list))]
        per_combine_prune_paned_actual_list = [per_combine_prune_paned_actual_list[i] *100 for i in range(len(per_combine_prune_paned_actual_list))]

        #Combine savings Pruning with sharing
        # add two list 
        #combine_prune_paired_savings_list = [Prune_savings_list[i] + share_pair_savings_list[i] for i in range(len(share_pair_savings_list))]
        #Percentage of combining
        per_combine_prune_paned_savings_list = [combine_prune_paned_savings_list[i] / Pane_no_prune_list[i] for i in range(len(Pane_no_prune_list))]
        per_combine_prune_paned_savings_list = [per_combine_prune_paned_savings_list[i] *100 for i in range(len(per_combine_prune_paned_savings_list))]
    
        Pane_Prune_dict[sh] = Pane_Prune_list
        Pane_Prune_savings_dict[sh] = Pane_Prune_savings_list
        Pane_no_prune_dict[sh] = Pane_no_prune_list
        Pane_per_prune_dict[sh] = Pane_per_prune_list
        Pane_per_prune_savings_dict[sh] = Pane_per_prune_savings_list
        Pane_L_dict[sh] = Pane_L_list
        Pane_S_dict[sh] = Pane_S_list
        
        Pane_share_dict[sh] = Pane_share_list
        Pane_share_savings_dict[sh] = Pane_share_savings_list
        Pane_per_share_dict[sh] = Pane_per_share_list
        Pane_per_share_savings_dict[sh] = Pane_per_share_savings_list
        
        share_pane_dict[sh] = share_pane_list
        share_pane_savings_dict[sh] = share_pane_savings_list
        per_share_pane_dict[sh] = per_share_pane_list
        per_share_pane_savings_dict[sh] = per_share_pane_savings_list
        
        
        combine_prune_paned_savings_dict[sh] = combine_prune_paned_savings_list
        per_combine_prune_paned_savings_dict[sh] = per_combine_prune_paned_savings_list
        combine_prune_paned_actual_dict[sh] = combine_prune_paned_actual_list
        per_combine_prune_paned_actual_dict[sh] = per_combine_prune_paned_actual_list 

        no_prune_dict[sh] = no_prune_list
        no_prune_savings_dict[sh] = no_prune_savings_list
        per_no_prune_dict[sh] = per_no_prune_list
        per_no_prune_savings_dict[sh] = per_no_prune_savings_list
        
        #print("Top-1 interesting view is subsequence ",interest) 
        print("Subsequence Length ",L,"\n")
        print("Percentage number of savings pruning ")
        print(Pane_per_prune_savings_dict) 
        print("Total number of pruning ",Pane_Prune_savings_dict)
        print("Total number of operations ",Pane_Prune_dict)
        print("Total number of no pruning ",Pane_no_prune_dict)
        print("Percentage number of operations pruning ")
        print(Pane_per_prune_dict) 
        #print("Total number of operations ",total_operations) 
        
        #print("actual_shareeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee ",actual_share)
        #print("share_shareeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee ",share_share)
        print("sharinggggggggggggggggggggggggggggggg")
        print("Pane_share_dict ",Pane_share_dict)
        print("Pane_share_savings_dict ",Pane_share_savings_dict)
        print("Pane_per_share_dict ",Pane_per_share_dict)
        print("Pane_per_share_savings_dict ",Pane_per_share_savings_dict)
        
        print("Cost of Combining savings pruning and sharing ", combine_prune_paned_savings_dict)
        print("Cost of Combining actual pruning and sharing ", combine_prune_paned_actual_dict)
        print("Percentage of combining savings pruning and sharing ", per_combine_prune_paned_savings_dict)
        print("Percentage of combining actual pruning and sharing ", per_combine_prune_paned_actual_dict) 

        print("Total number of savings no pruning ",no_prune_savings_dict)

        Pane_share_pair_list = []
        Pane_combine_prune_paired_list =[]
        Pane_per_combine_prune_paired_list = []
        Pane_per_share_pair_list = []
        Pane_per_no_prune_list = []
        
        Pane_share_list = []
        Pane_share_savings_list = []
        Pane_per_share_list = []
        Pane_per_share_savings_list = [] 
             
    
        Pane_Prune_list = []
        Pane_Prune_savings_list = []
        Pane_no_prune_list = []
        Pane_per_prune_list = []
        Pane_per_prune_savings_list = []
        Pane_L_list = []  
        Pane_S_list = [] 
        actual_operations = 0
        oper_list = []
        
        combine_prune_paned_savings_list = []
        combine_prune_paned_actual_list = []
        per_combine_prune_paned_savings_list = []
        per_combine_prune_paned_actual_list = []
        
        no_prune_list = []
        no_prune_savings_list = []
        per_no_prune_list = []
        per_no_prune_savings_list = []
        
        share_pane_list = []
        share_pane_savings_list = []
        per_share_pane_list = []
        per_share_pane_savings_list = []
        
        print("Total number of pane savings pruning ", Pane_Prune_savings_dict)
        print("Total number of pane actual pruning ", Pane_Prune_dict)

        print("Cost of sharing savings using paned window technique ",Pane_share_savings_dict)
        print("Cost of sharing using paned window technique ",Pane_share_dict)

        print("Cost of Combining savings pruning and sharing ", combine_prune_paned_savings_dict)
        print("Cost of Combining actual pruning and sharing ", combine_prune_paned_actual_dict)

        print("L_dict ",Pane_L_dict)
        print("DevListtttttttttttttttttttt ",DevList)
        print("Dev_dictttttttttttttttttt ",Dev_dict)
        
        
print("*********************************************************************************************************")
#Code for Base2 pruning only using point by point pruning (Done)
Prune_point_list = []
Prune_point_dict = {}
no_prune_point_list = []
no_prune_point_dict = {}
per_prune_point_list = []
per_prune_point_dict = {}

Prune_point_actual_list = []
Prune_point_actual_dict = {}
per_prune_point_actual_list = []
per_prune_point_actual_dict = {}

L_point_dict = {}
L_point_list = []
L_list = []
L_dict = {}
S_list = []
S_dict = {}

#DevList and Dev_ref
length = K
DevList_p = [-999] * length
Dev_ref_p = DevList_p[-1]  #Minimum of the largest deviations
Dev_ref_ind_p = -1

length = K
initial_value = -999  

Dev_dict_p = {i+1: initial_value for i in range(length)}
Dev_ref_dict_p = list(Dev_dict_p.values())[-1]
print("Dev_dict_p ",Dev_dict_p)
print("Dev_ref_dict_p ",Dev_ref_dict_p)

for sh in SHIFT:
    
    for n in N:
        #n=200
        #Select Data from the begining
        UAE_ACTUALL = data1['workplaces'].iloc[ : n]   #UAE_parks  UAE_workplaces
        US_ACTUALL = data1['residential'].iloc[ : n]    #US_parks   UAE_residential
        
        
        #Data after normalization
        #UAE_ACTUAL = (UAE_ACTUAL-min_1)/(max_1-min_1)
        #US_ACTUAL = (US_ACTUAL-min_1)/(max_1-min_1)
        #print(UAE_ACTUAL, US_ACTUAL)
        
        
        
        #Core of Pruning with overlap
        for l in L:
            
            if((n-l)%sh==0):
                comm = [0] * n
                prune = 0
                oper_prune = 0
                L_list.append(l)
                S_list.append(sh)
                V = int((n-l)/sh)+1 #Number of views
                
                print("VIEWSSSSSSSS ",V)
                
                DevList_p = [-999] * length
                Dev_ref_p = DevList_p[-1]  #Minimum of the largest deviations
                Dev_ref_ind_p = -1
                
                Dev_dict_p = {i+1: initial_value for i in range(length)}
                Dev_ref_dict_p = list(Dev_dict_p.values())[-1]
                
                #Data after normalization individually for each subsequence
                #First subsequence
                min_1 = UAE_ACTUALL[:l].min()
                max_1 = UAE_ACTUALL[:l].max()
                #print("min_1 ",min_1)
                #print("max_1 ",max_1)
                #print("UAE_ACTUALL[:l] b  ",UAE_ACTUALL[:l])
                if (min_1 == max_1):
                    UAE_ACTUAL[:l] = UAE_ACTUALL[:l]
                else:
                    UAE_ACTUAL[:l] = (UAE_ACTUALL[:l]-min_1)/(max_1-min_1)
                #print("UAE_ACTUAL[:l] ",UAE_ACTUAL[:l])

                #Second subsequence
                min_2 = US_ACTUALL[:l].min()
                max_2 = US_ACTUALL[:l].max()
                #print("min_2 ",min_2)
                #print("max_2 ",max_2)
                if (min_2 == max_2):
                    US_ACTUAL[:l] = US_ACTUALL[:l]
                else:                    
                    US_ACTUAL[:l] = (US_ACTUALL[:l]-min_2)/(max_2-min_2)
                #print("US_ACTUAL[:l] ",US_ACTUAL[:l])

                
                #Deviation of the first subsequence as the reference deviation
                DEV_REF = distance.euclidean(UAE_ACTUAL[:l], US_ACTUAL[:l])
                #DEV_SUB_MAX.append(DEV_REF)
                #print(" DEV_REF ", DEV_REF)
                #print(comm)
                #[comm[i] == 1 for i in [0:l]] 
                
                
                #Add first deviation to the DevList
                ind_DevList_p = 0
                DevList_p[ind_DevList_p] = DEV_REF                
                print("DevListttt11_p ",DevList_p)
                
                Dev_ref_p = DevList_p[-1]
                print("Dev_ref11_p ",Dev_ref_p)
                
                Dev_dict_p[1] = DEV_REF
                print("Dev_dict11_p ",Dev_dict_p)
                Dev_ref_dict_p = list(Dev_dict_p.values())[-1]
                print("Dev_ref_dict11_p ",Dev_ref_dict_p)
                
                oper_prune +=2*l-1
                print("oper_prune ",oper_prune)
                
                for x, res in enumerate(comm): 
                    if x in range (0,l):
                        comm[x]=1
                print("commmmmmm ",comm)
                
                for i in range(1,V,1):   #V
                
                    if ind_DevList_p < K-1:
                        ind_DevList_p += 1    
                
                    print("viewwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww ",i+1)
                    #print("seq_listseq_listseq_list ",seq_list)
                    
                    val = []

                    #Data after normalization individually for each subsequence
                    #First subsequence
                    #min_1 = UAE_ACTUALL[i*sh:l+i*sh].min()
                    #max_1 = UAE_ACTUALL[i*sh:l+i*sh].max()
                    
                    min_1 = UAE_ACTUALL.min()
                    max_1 = UAE_ACTUALL.max()
                    
                    #print("min_1 ",min_1)
                    #print("max_1 ",max_1)
                    #print("UAE_ACTUALL[i*sh:l+i*sh] b  ",UAE_ACTUALL[i*sh:l+i*sh])
                    if (min_1 == max_1):
                        UAE_ACTUAL[i*sh:l+i*sh] = UAE_ACTUALL[i*sh:l+i*sh]
                    else:
                        UAE_ACTUAL[i*sh:l+i*sh] = (UAE_ACTUALL[i*sh:l+i*sh]-min_1)/(max_1-min_1)
                    #print("UAE_ACTUAL[i*sh:l+i*sh] ",UAE_ACTUAL[i*sh:l+i*sh])

                    #Second subsequence
                    #min_2 = US_ACTUALL[i*sh:l+i*sh].min()
                    #max_2 = US_ACTUALL[i*sh:l+i*sh].max()
                    
                    min_2 = US_ACTUALL.min()
                    max_2 = US_ACTUALL.max()
                    
                    #print("min_2 ",min_2)
                    #print("max_2 ",max_2)
                    if (min_2 == max_2):
                        US_ACTUAL[i*sh:l+i*sh] = US_ACTUALL[i*sh:l+i*sh]
                    else:                    
                        US_ACTUAL[i*sh:l+i*sh] = (US_ACTUALL[i*sh:l+i*sh]-min_2)/(max_2-min_2)
                    #print("US_ACTUAL[i*sh:l+i*sh] ",US_ACTUAL[i*sh:l+i*sh])                    
                    
                    #print("iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii", i)
                    #print("DEV_REF ",DEV_REF)
                    #j = [i*SHIFT:l+1+i*SHIFT]
                    #print(j)
                    #print(type(j))
                    #if comm[j]==1:
                    #    print("YESSSS")
                    for j in range(i*sh,l+i*sh,1):
                        #print(j)
                        
                        if comm[j]==1:
                            val.append(j)
                            #print("YESSSS")
                            
                    print(val)
                    #Special case if val = []
                    # if (len(val)==0):
                    #     #for u in range(i*sh,seq_list[0]+i*sh,1):
                    #     for u in range(i*sh,seq_list[0]+i*sh,1):
                    #         comm[u]=1
                    #         val.append(u)
                    # print(val)      

                    #print(val[-1])
                    #print(UAE_ACTUAL[val[0]:val[-1]+1])
                    #print(US_ACTUAL[val[0]:val[-1]+1])
                    #print(l-len(val))
                    while ((l-len(val))>=0):
                        if (len(val)==0):
                            DEV_SUB = np.sqrt(l)
                            #print("DEV_SUB ",DEV_SUB)
                            val.append(i*sh)
                            
                        if (len(val)>0):
                            DEV_SUB = np.sqrt(np.sum(np.square(UAE_ACTUAL[val[0]:val[-1]+1]-US_ACTUAL[val[0]:val[-1]+1]))+(l-len(val)))
                            print("DEV_SUB22 ",DEV_SUB)
                            
                            if (len(UAE_ACTUAL[val[0]:val[-1]+1])!=l and DEV_SUB >= Dev_ref_p):

                                # if i == 1:
                                #     Dev_ref = DevList[ind_DevList-1]
                                #     print("Dev_ref22aa ",Dev_ref)
                                    
                                #     if K == 1:
                                #         #Dev_dict[i+1] = DEV_SUB
                                #         print("Dev_dict22aa ",Dev_dict)
                                #         Dev_ref_dict = list(Dev_dict.values())[-1]
                                #         print("Dev_ref_dict22aa ",Dev_ref_dict) 
                                #     else:
                                #         #Dev_dict[i+1] = DEV_SUB
                                #         print("Dev_dict22bb ",Dev_dict)
                                #         Dev_ref_dict = list(Dev_dict.values())[-2]
                                #         print("Dev_ref_dict22bb ",Dev_ref_dict)   
                                # else:
                                    
                                #DevList[ind_DevList] = DEV_SUB
                                print("DevListttt22_p ",DevList_p)
                                    
                                Dev_ref_p = DevList_p[ind_DevList_p]
                                print("Dev_ref22bb_p ",Dev_ref_p)
                                
                                #Dev_dict[i+1] = DEV_SUB
                                print("Dev_dict22_p ",Dev_dict_p)
                                
                                Dev_ref_dict_p = list(Dev_dict_p.values())[-1]
                                print("Dev_ref_dict22_p ",Dev_ref_dict_p)  
                            
                            
                            if (len(UAE_ACTUAL[val[0]:val[-1]+1])==l and DEV_SUB>Dev_ref_p):
                                Dev_ref_p = DEV_SUB
                                DevList_p[ind_DevList_p] = DEV_SUB
                                print("DevListttt33_p ",DevList_p)
                                print("Dev_ref33_p ",Dev_ref_p)
                                
                                #Swapping
                                # if DevList[ind_DevList-1] < DevList[ind_DevList]:
                                #     temp = DevList[ind_DevList-1]
                                #     DevList[ind_DevList-1] = DEV_SUB
                                #     DevList[ind_DevList] = temp
                                #     print("DevListttt33 ",DevList)
                                DevList_p.sort(reverse=True)
                                print("DevListttt33_p ",DevList_p)
                                
                                if (i+1) > K:
                                    Dev_dict_p.popitem()
                                Dev_dict_p[i+1] = DEV_SUB
                                print("Dev_dict33aa_p ",Dev_dict_p)
                                
                                #Swapping
                                Dev_dict_p = dict(sorted(Dev_dict_p.items(), key=lambda item: item[1], reverse=True))
                                print("DevListttt33bb_p ",DevList_p)
                                # value_before = get_value_before_key(Dev_dict, i+1)
                                # print("value_before ",value_before)
                                # key_before = get_key_before_key(Dev_dict, i+1)
                                # print("key_before ",key_before)
                                
                                # if Dev_dict[i+1] > value_before:
                                #     Dev_dict = swap_keys(Dev_dict, key_before, i+1)
                                #     print("Dev_dict33bb ",Dev_dict)
                                #     temp1 = Dev_dict[i+1]
                                #     Dev_dict[i+1] = DEV_SUB
                                #     Dev_dict[key_before] = temp1
                                #     print("DevListttt33bb ",DevList)
                                
                                Dev_ref_dict_p = list(Dev_dict_p.values())[-1]
                                print("Dev_ref_dict33_p ",Dev_ref_dict_p)



                                print("subsequence {} saves {}".format(i+1,0))
                                oper_prune +=  2*l-1
                                print("oper_prune ",oper_prune)
                                #max_value = max(DEV_SUB_MAX)
                                #max_index = DEV_SUB_MAX.index(max_value)
                                #interest = max_index+1
                                break
                                
                                    
                            if (DEV_SUB < Dev_ref_p):
                                # DEV_SUB_MAX.append(DEV_SUB)
                                # if (max(DEV_SUB_MAX) >DEV_SUB):
                                #     max_index = DEV_SUB_MAX.index(max(DEV_SUB_MAX))
                                #     interest = max_index+1
                                # else:
                                #     interest = 1
                                if(l-len(val)==0):
                                    
                                    #DevList[ind_DevList] = DEV_SUB
                                    print("DevListttt44_p ",DevList_p)
                                    
                                    Dev_ref_p = DevList_p[ind_DevList_p]
                                    print("Dev_ref44_p ",Dev_ref_p)
                                    
                                    #Dev_dict[i+1] = DEV_SUB
                                    print("Dev_dicttt44_p ",Dev_dict_p)
                                    
                                    Dev_ref_dict_p = list(Dev_dict_p.values())[-1]
                                    print("Dev_ref_dict44_p ",Dev_ref_dict_p)

                                    
                                    print("subsequence {} saves {}".format(i+1,(l-len(val))))
                                    prune +=(l-len(val))
                                    oper_prune += 2*l-1
                                    print("oper_prune ",oper_prune)
                                    break
                                else:
                                    print("subsequence {} saves {}".format(i+1,(l-len(val))+((l-len(val))-1)))
                                    prune +=(l-len(val))+((l-len(val))-1)
                                    prune +=1
                                    print("prune ",prune)
                                    oper_prune += (l-(l-len(val))) + (l-(l-len(val)))-1
                                    print("oper_prune ",oper_prune)
                                    break
                                #print("subsequence {} saves {}".format(i+1,(l-len(val))))
                                #prune +=(l-len(val))
                                #break
                        
                        
                        vall = val[-1]+1
                        #print(val[-1])
                        #print(vall)
                        val.append(vall)
                        #print(val)
                        #print(comm[vall])
                        if (comm[vall]!=1):
                            #print("INNN")
                            comm[vall]=1
                            
                            #print(comm)
                        #print(comm)
                    #print("-------------------------------------------------------------------------------------")                  
    
                print("DevListtttttttttttttttttttt_p ",DevList_p)
                print("Dev_dicttttttttttttttttttttt_p ",Dev_dict_p)
                #print("DEV_SUB_MAX ",DEV_SUB_MAX)
                print("DevList_Final_p ",DevList_p)
                #DEV_SUB_MAX.clear()
                DevList_p.clear()
                Dev_dict_p.clear()
                #print("Top-1 interesting view is subsequence ",interest) 
                #print("Total number of pruning ,",prune)
                Prune_point_list.append(prune)  #Saved
                Prune_point_actual_list.append(oper_prune)  #Operations
                no_prune = (l+(l-1))*V
                no_prune_point_list.append(no_prune)
                per_prune_point_list.append(prune/(no_prune)*100) #Per_Saved
                per_prune_point_actual_list.append(oper_prune/(no_prune)*100)  #Per_Operations                    
    
                                      
        Prune_point_actual_dict[sh] = Prune_point_actual_list
        Prune_point_dict[sh] = Prune_point_list
        no_prune_point_dict[sh] = no_prune_point_list
        per_prune_point_dict[sh] = per_prune_point_list
        per_prune_point_actual_dict[sh] = per_prune_point_actual_list
        L_point_dict[sh] = L_point_list
        L_dict[sh] = L_list
        S_dict[sh] = S_list
        print("Subsequence Length ",L,"\n","Pruning is ",Prune_point_list)
        print("Total number of pruning by point ", Prune_point_dict)
        print("Total number of operations by point ", Prune_point_actual_dict)
        print("Total number of no pruning by point ",no_prune_point_dict)
        print("Percentage number of pruning by point ",per_prune_point_dict)
        print("Percentage number of operations by point ",per_prune_point_actual_dict)
        
        print("DevListtttttttttttttttttttt_p ",DevList_p)
        print("Dev_dictttttttttttttttttt_p ",Dev_dict_p)
 
        Point_Prune_list = []
        Prune_point_list = []
        no_prune_point_list = []
        per_prune_point_list = []
        Point_per_prune_list = []
        L_point_list = []   
        L_list =[]
        S_list = [] 
print("**************************************************************************************")                                  

print("Total number of savings pane pruning ", Pane_Prune_savings_dict)
print("Total number of actual pane pruning ", Pane_Prune_dict)

print("Total number of savings point pruning ", Prune_point_dict)
print("Total number of actual point pruning ", Prune_point_actual_dict)
print("per_prune_point_dict ",per_prune_point_dict)
print("per_prune_point_actual_dict ",per_prune_point_actual_dict)

print("Cost of Combining savings pruning and sharing ", combine_prune_paned_savings_dict)
print("Cost of Combining actual pruning and sharing ", combine_prune_paned_actual_dict)
print("per_combine_prune_paned_savings_dict ",per_combine_prune_paned_savings_dict)
print("per_combine_prune_paned_actual_dict ",per_combine_prune_paned_actual_dict)

print("Cost of sharing savings alone ",share_pane_savings_dict)
print("Cost of sharing alone ",share_pane_dict)
print("per_share_pane_savings_dict ",per_share_pane_savings_dict)
print("per_share_pane_dict ",per_share_pane_dict)

print("Cost of sharing savings using paned window technique ",Pane_share_savings_dict)
print("Cost of sharing using paned window technique ",Pane_share_dict)
print("Total number of no pruning ",no_prune_dict)
print("Total number of savings no pruning ",no_prune_savings_dict)
print("L_dict ",L_dict)
        
#Plot Amount of savings
for p in SHIFT:
    plt.plot(L_dict[p], no_prune_savings_dict[p], label='Linear Search', marker = 'o', color = 'b')
    plt.plot(L_dict[p], Prune_point_dict[p], label='TimEx-pruning', marker = 'x', color = 'orange')
    #plt.plot(L_dict[p], Prune_savings_dict[p], label='Aggregate Horizontal pruning', marker = 'o')
    plt.plot(L_dict[p], share_pane_savings_dict[p], label='TimEx-sharing', marker = '.', color = 'g')
    plt.plot(L_dict[p], combine_prune_paned_savings_dict[p], label='TimEx-hybrid', marker = 'D', color = 'r')
    plt.xticks(ticks=L_dict[p], labels=L_dict[p], rotation=45)


plt.xlabel("Subsequence Length (R)")
plt.ylabel("Number of saved operations")
#plt.title("Time series data length (N = 500) and shift length (S = 5)")
plt.xlim(left=0)
plt.ylim(bottom=0)
plt.legend()
plt.show()

#Plot Amount of operations
for p in SHIFT:
    plt.plot(L_dict[p], no_prune_dict[p], label='Linear Search', marker = 'o', color = 'b')
    plt.plot(L_dict[p], Prune_point_actual_dict[p], label='TimEx-pruning', marker = 'x', color = 'orange')
    #plt.plot(L_dict[p], Prune_actual_dict[p], label='Aggregate Horizontal pruning', marker = 'o')
    plt.plot(L_dict[p], share_pane_dict[p], label='TimEx-sharing', marker = '.', color = 'g')
    plt.plot(L_dict[p], combine_prune_paned_actual_dict[p], label='TimEx-hybrid', marker = 'D', color = 'r')
    plt.xticks(ticks=L_dict[p], labels=L_dict[p], rotation=45)

plt.xlabel("Subsequence Length (R)")
plt.ylabel("Number of operations ")
#plt.title("Time series data length (N = 500) and shift length (S = 5)")
plt.xlim(left=0)
plt.ylim(bottom=0)
plt.legend()
plt.show()

#Plot Percentage Amount of savings
for p in SHIFT:
    #plt.plot(L_dict[p], per_no_prune_savings_dict[p], label='Linear Search', marker = 'o', color = 'b')
    plt.plot(L_dict[p], per_prune_point_dict[p], label='TimEx-pruning', marker = 'x', color = 'orange')
    #plt.plot(L_dict[p], per_prune_savings_dict[p], label='Aggregate Horizontal pruning', marker = 'o')
    plt.plot(L_dict[p], per_share_pane_savings_dict[p], label='TimEx-sharing', marker = '.', color = 'g')
    plt.plot(L_dict[p], per_combine_prune_paned_savings_dict[p], label='TimEx-hybrid', marker = 'D', color = 'r')
    plt.xticks(ticks=L_dict[p], labels=L_dict[p], rotation=45)
    
    
plt.xlabel("Subsequence Length (R)")
plt.ylabel("Normalized Number of saved operations \n vs. Linear Search %")
#plt.title("Time series data length (N = 500) and shift length (S = 5)")
plt.xlim(left=0)
plt.ylim(bottom=0)
plt.legend()
plt.show()

#Plot Percentage Amount of operations
for p in SHIFT:
    #plt.plot(L_dict[p], per_no_prune_dict[p], label='Linear Search', marker = 'o', color = 'b')
    plt.plot(L_dict[p], per_prune_point_actual_dict[p], label='TimEx-pruning', marker = 'x', color = 'orange')
    #plt.plot(L_dict[p], per_prune_actual_dict[p], label='Aggregate Horizontal pruning', marker = 'o')
    plt.plot(L_dict[p], per_share_pane_dict[p], label='TimEx-sharing', marker = '.', color = 'g')
    plt.plot(L_dict[p], per_combine_prune_paned_actual_dict[p], label='TimEx-hybrid', marker = 'D', color = 'r')
    plt.xticks(ticks=L_dict[p], labels=L_dict[p], rotation=45)
    
plt.xlabel("Subsequence Length (R)")
plt.ylabel("Normalized Number of operations \n vs. Linear Search %")
#plt.title("Time series data length (N = 500) and shift length (S = 5)")
plt.xlim(left=0)
plt.ylim(bottom=0)
plt.legend()
plt.show()

print("-----------------------------------------------------------------------------")


