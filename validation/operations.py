'''
Created on 10 fevr. 2018

@author: N'TIC
'''
messages = {
        'msg_1' :  "*************************************\n",  
        'msg_2': "dim layer\tWindow Test\tRMSE\tMAE\tTime\t", 
        'msg_3' : "Total time in minutes for complete cross validation:",
        'msg_4' : "\t" + "\t" + "mean RMSE\t" + "mean MAE\t"+ "total time"
    }

import os

def window(pos_window, size_window, k_fold, slot_list):
    
    i = iter(slot_list)    
    for pas in range(k_fold):
        if pas == pos_window:
            for _ in range(size_window):
                next(i)
        else:
            win = []
            for _ in range(0, size_window):
                win.append(next(i))
            yield win

def get_training_slot(pos_window, size_window, k_fold, slot_list):
    liste = window(pos_window, size_window, k_fold, slot_list)
    training_slots_groups = []
    for i in liste:
        training_slots_groups.append(i)
    
    training_slots = []    
    for i in range(k_fold - 1):
        for j in range(size_window):
            training_slots.append(training_slots_groups[i][j])
        
    return training_slots

def folds_cross_validation(pos_window,size_window, k_flod, slot_list):   
    testing_slot = []    
    start_index = pos_window * size_window
    end_index = start_index + size_window   
    for i in range(start_index, end_index):
        testing_slot.append(i)  
    
    training_slots = get_training_slot(pos_window, size_window, k_flod, slot_list)
    return training_slots, testing_slot 


def getFile(file_name):
    path = '../results/'+file_name + '.txt'
    path = os.path.join(os.path.dirname(__file__), path)
    my_file = open(path, "a")
    return my_file