'''
Created on 19 janv. 2018

@author: N'TIC
'''

import pandas as pd
import time
import pretreatments.io_operations as io
from cmath import nan

slot_count = 64

#*******************************************************************#

#*******************************************************************#        

def set_new_dataMatrixBySlot():
    start_time = time.time()
    
    new_dataMatrixBySlot(0)
    new_dataMatrixBySlot(1)
        
    interval = time.time() - start_time  
    print ("Total time in seconds for complete missing values:", interval)
    # Total time in seconds: 929.210842370986

# add only missing user for create 142*4500 matrix
def new_dataMatrixBySlot(qosMetric):
    
    
    count_nan_after = 0
    count_nan_before = 0
    count_missing_service = 0
    count_missing_user = 0
    for slot in range(slot_count):
        
        df_Matrix_slot = io.read_MatrixBySlot(qosMetric, slot)
        
        count_nan_before = count_nan_before + df_Matrix_slot.isnull().values.sum()
        
        df_Matrix_slot, missing_user, missing_service = add_missing_users(df_Matrix_slot, slot)
        
        count_missing_service = count_missing_service + missing_service
        count_missing_user = count_missing_user + missing_user
        
        # print('0/1-->rt/tp \t',qosMetric, '\t slot : ',slot, '\t missing user : ', missing_user, '\t count_service : ',count_service)
        
        # remplace all nan value with 0
        count_nan_after = count_nan_after + df_Matrix_slot.isnull().values.sum()
        
        
        io.write_updated_MatrixBySlot(qosMetric, df_Matrix_slot, slot)
    print("avant: ", count_nan_before)
    print("apres" , count_nan_after)
    print("missing user: ", count_missing_user)
    print("missing service " , count_missing_service)
        
def add_missing_users(df_Matrix_slot, slot):

    
    
    count_index = df_Matrix_slot.index.values
    count_service = len(df_Matrix_slot.columns)
    missing_service = 4500 - count_service
    
    

    missing_user = 0
    line = 0;
    for index in range(len(count_index)):
        num_index = count_index[index]
        if line == num_index:
            line = line + 1
        else: 
            for k in range(line, num_index):
                df_Matrix_slot.loc[k] = [nan for n in range(count_service)]
                missing_user = missing_user + 1
            line = num_index + 1    
            df_Matrix_slot.sort_index(inplace=True)
    
    if count_service != 4500 :
        exist_service = df_Matrix_slot.columns.tolist()
        all_service = [str(n) for n in range(4500)]
        missing_servicelist = list(set(all_service) - set(exist_service))
        for val in missing_servicelist :
            values = pd.Series(nan for n in range(142))
            df_Matrix_slot.insert(int(val), val, values)            
            
    return df_Matrix_slot, missing_user, missing_service
    
#*******************************************************************#

#*******************************************************************#        

def set_dataMatrixBySlot():
    
    start_time = time.time()
    
    dataMatrixBySlot(0)
    dataMatrixBySlot(1)
    
    interval = time.time() - start_time  
    print ("Total time in seconds for deviding  data set by slot:", interval)
    # Total time in seconds: 929.210842370986

# create rtMatrix (0) /tpMatrix (1) by slot
def dataMatrixBySlot(qosMetric):
    df_data = io.read_big_data(qosMetric)
    
    
    for slot in range(slot_count):
        _df_data = df_data[df_data.slot == slot].sort_values(by=['user_ID', 'service_ID'])
        qos_saves(_df_data, slot, qosMetric)
        df_data = df_data[df_data.slot != slot]

def qos_saves(_df_data, slot, qosMetric):
    io.write_DataBySlot(qosMetric, _df_data, slot)
    _df_data = _df_data[['user_ID', 'service_ID', 'rate']]
    Matrix = pd.pivot_table(_df_data, index='user_ID', columns='service_ID', values='rate')
    io.write_MatrixBySlot(qosMetric, Matrix, slot)


#*******************************************************************#

#*******************************************************************#        

def set_max_density_dataMatrixBySlot():
    start_time = time.time()
    
    max_density_dataMatrixBySlot(0)
    max_density_dataMatrixBySlot(1)
        
    interval = time.time() - start_time  
    print ("Total time in seconds for complete missing values:", interval)

def max_density_dataMatrixBySlot(qosMetric):
    df_data_all = io.read_big_data(qosMetric)
    
    count_nan_after = 0
    count_nan_before = 0
    for slot in range(63, 0, -1):
        df_data = df_data_all[df_data_all.slot < slot]
        df_data.reset_index(drop=True, inplace=True)
        start_time = time.time()
        print("slot : ", slot)
        df_Matrix_slot = io.read_updated_MatrixBySlot(qosMetric, slot)
        nan_count = df_Matrix_slot.isnull().values.sum()

        count_nan_before = count_nan_before + nan_count
        print("nan count : ", nan_count)
        
        somme = 0
        for line, row in df_Matrix_slot.iterrows():
            mask = row.isnull()
            columns = row[mask].index.tolist()
            df = df_data[(df_data.user_ID == line)]
            df = df[df['service_ID'].isin(columns)] 
            #df.reset_index(inplace=True) 
            df.reset_index(drop=True, inplace=True)
            for _, col in enumerate(columns):
                df__ = df[(df.service_ID == int(col))]                
                if len(df__) != 0:
                    val = df__[['rate']].mean()
                    df_Matrix_slot.loc[line][col] = val
                    somme += 1
                del df__
                 
            del df
            df_data = df_data[df_data.user_ID != line]
            df_data.reset_index(drop=True, inplace=True)
        
        print(somme)    
        nan_count = df_Matrix_slot.isnull().values.sum()
        print("new nan count : ", nan_count)        
        count_nan_after = count_nan_after + nan_count
        io.write_max_density_MatrixBySlot(qosMetric, df_Matrix_slot, slot)
        interval = time.time() - start_time  
        print ("Total time in seconds for complete missing values:", interval)
    print("avant: ", count_nan_before)
    print("apres" , count_nan_after)
    
def getStat():
    somme_nan_updated_rt = 0
    somme_nan_max_rt = 0
    somme_nan_updated_tp = 0
    somme_nan_max_tp = 0
    for slot in range(64):
        print(slot)
        df_Matrix_slot = io.read_updated_MatrixBySlot(0, slot)
        somme_nan_updated_rt += df_Matrix_slot.isnull().values.sum()
        print("somme_nan_updated_rt : ", somme_nan_updated_rt)
        
        df_Matrix_slot = io.read_max_density_MatrixBySlot(0, slot)
        somme_nan_max_rt += df_Matrix_slot.isnull().values.sum()
        print("somme_nan_max_rt : ", somme_nan_max_rt)
        
        df_Matrix_slot = io.read_updated_MatrixBySlot(1, slot)
        somme_nan_updated_tp += df_Matrix_slot.isnull().values.sum()
        print("somme_nan_updated_tp : ", somme_nan_updated_tp)
        
        df_Matrix_slot = io.read_max_density_MatrixBySlot(1, slot)
        somme_nan_max_tp += df_Matrix_slot.isnull().values.sum()
        print("somme_nan_max_tp : ", somme_nan_max_tp)
    
    print("somme_nan_updated RT: ", somme_nan_updated_rt)
    print("somme_nan_max RT : ", somme_nan_max_rt)

    print("somme_nan_updated TP: ", somme_nan_updated_tp)
    print("somme_nan_max TP : ", somme_nan_max_tp)

set_dataMatrixBySlot()
set_new_dataMatrixBySlot()
set_max_density_dataMatrixBySlot()
getStat()



