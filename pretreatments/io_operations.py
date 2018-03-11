'''
Created on 19 janv. 2018

@author: N'TIC
'''
import numpy as np
import pandas as pd
import os

user_listFile = os.path.join(os.path.dirname(__file__), '../dataset/dataset1/userlist.txt')
service_listFile = os.path.join(os.path.dirname(__file__), '../dataset/dataset1/wslist.txt')

user_colnames = ['user_ID', 'ip_Address', 'country', 'ip_No.', 'asn', 'latitude', 'longitude']
user_datatype = {'user_ID': int, 'ip_Address' :str, 'country':str, 'ip_No.':str, 'asn':str, 'latitude': np.float, 'longitude': np.float}

service_colnames = ['service_ID', 'wsdl_address','service_provider','ip_Address', 'country', 'ip_No.', 'asn', 'latitude', 'longitude']
service_datatype = {'service_ID': int, 'wsdl_address':str,'service_provider' : str,'ip_Address' :str, 'country':str, 'ip_No.':str, 'asn':str, 'latitude': np.float, 'longitude': np.float}



small_rtMatrixFile = os.path.join(os.path.dirname(__file__), '../dataset/dataset1/rtMatrix.txt')
small_tpMatrixFile = os.path.join(os.path.dirname(__file__), '../dataset/dataset1/rtMatrix.txt')

big_rtDataFile = os.path.join(os.path.dirname(__file__), '../dataset/dataset2/rtdata.txt')
big_tpDataFile = os.path.join(os.path.dirname(__file__), '../dataset/dataset2/tpdata.txt')

slot_rtDataFile = os.path.join(os.path.dirname(__file__), '../dataset/dataset2/slots/rtdata/rtdata_slot_')
slot_tpDataFile = os.path.join(os.path.dirname(__file__), '../dataset/dataset2/slots/tpdata/tpdata_slot_')

slot_rtMatrixFile = os.path.join(os.path.dirname(__file__), '../dataset/dataset2/slots/rtdata/rtMatrix_slot_')
slot_tpMatrixFile = os.path.join(os.path.dirname(__file__), '../dataset/dataset2/slots/tpdata/tpMatrix_slot_')

slot_updated_rtMatrixFile = os.path.join(os.path.dirname(__file__), '../dataset/dataset2/slots/rtdata/rtMatrix_updated_slot_')
slot_updated_tpMatrixFile = os.path.join(os.path.dirname(__file__), '../dataset/dataset2/slots/tpdata/tpMatrix_updated_slot_')

slot_max_density_rtMatrixFile = os.path.join(os.path.dirname(__file__), '../dataset/dataset2/slots/rtdata/rtMatrix_max_density_slot_')
slot_max_density_tpMatrixFile = os.path.join(os.path.dirname(__file__), '../dataset/dataset2/slots/tpdata/tpMatrix_max_density_slot_')


slot_updated_ByCountry_rtMatrixFile = os.path.join(os.path.dirname(__file__), '../dataset/dataset2/slots/rtdata/country/rtMatrix_updated_slot_')
slot_updated_ByCountry_tpMatrixFile = os.path.join(os.path.dirname(__file__), '../dataset/dataset2/slots/tpdata/country/tpMatrix_updated_slot_')

slot_updated_ByAsn_rtMatrixFile = os.path.join(os.path.dirname(__file__), '../dataset/dataset2/slots/rtdata/asn/rtMatrix_updated_slot_')
slot_updated_ByAsn_tpMatrixFile = os.path.join(os.path.dirname(__file__), '../dataset/dataset2/slots/tpdata/asn/tpMatrix_updated_slot_')


Data_colnames = ['user_ID', 'service_ID', 'slot', 'rate']
Data_datatype = {'user_ID': int, 'service_ID': int, 'slot': int, 'rate': np.float}



## save updated matrix with mean of latest slot
def write_max_density_MatrixBySlot(qosMetric, df_matrix, slot):
    if qosMetric == 0 :
        slot_max_density_MatrixFile = slot_max_density_rtMatrixFile + str(slot).zfill(2) + '.txt'
    else :
        slot_max_density_MatrixFile = slot_max_density_tpMatrixFile + str(slot).zfill(2) + '.txt'
        
    df_matrix.to_csv(slot_max_density_MatrixFile, sep='\t', encoding="utf-8", header=True, index=True, float_format='%.3f')
    
# # save brute rt_data or tp_data by slot
def write_updated_MatrixBySlot(qosMetric, df_matrix, slot):
    
    if qosMetric == 0 :
        slot_updated_MatrixFile = slot_updated_rtMatrixFile + str(slot).zfill(2) + '.txt'
    else :
        slot_updated_MatrixFile = slot_updated_tpMatrixFile + str(slot).zfill(2) + '.txt'
        
    df_matrix.to_csv(slot_updated_MatrixFile, sep='\t', encoding="utf-8", header=True, index=True, float_format='%.3f')

# # save brute rt_data or tp_data by slot
def write_MatrixBySlot(qosMetric, df_matrix, slot):
    
    if qosMetric == 0 :
        slot_MatrixFile = slot_rtMatrixFile + str(slot).zfill(2) + '.txt'
    else :
        slot_MatrixFile = slot_tpMatrixFile + str(slot).zfill(2) + '.txt'
        
    df_matrix.to_csv(slot_MatrixFile, sep='\t', encoding="utf-8", header=True, index=True, float_format='%.3f')


def write_DataBySlot(qosMetric, df_data, slot):
    
    if qosMetric == 0 :
        slot_DataFile = slot_rtDataFile + str(slot).zfill(2) + '.txt'
    else :
        slot_DataFile = slot_tpDataFile + str(slot).zfill(2) + '.txt'
        
    df_data.to_csv(slot_DataFile, sep='\t', encoding="utf-8", header=False, index=False, float_format='%.3f')

def read_max_density_MatrixBySlot(qosMetric, slot):
    if qosMetric == 0 :
        slot_max_densityMatrixFile = slot_max_density_rtMatrixFile + str(slot).zfill(2) + '.txt'
    else :
        slot_max_densityMatrixFile = slot_max_density_tpMatrixFile + str(slot).zfill(2) + '.txt'
        
    
    df_Data = pd.read_csv(slot_max_densityMatrixFile, sep='\t', index_col=0)
    
    return df_Data


def read_updated_MatrixBySlot(qosMetric, slot):
    if qosMetric == 0 :
        slot_updatedMatrixFile = slot_updated_rtMatrixFile + str(slot).zfill(2) + '.txt'
    else :
        slot_updatedMatrixFile = slot_updated_tpMatrixFile + str(slot).zfill(2) + '.txt'
        
    
    df_Data = pd.read_csv(slot_updatedMatrixFile, sep='\t', index_col=0)
    
    return df_Data

    
def read_MatrixBySlot(qosMetric, slot):

    if qosMetric == 0 :
        slot_MatrixFile = slot_rtMatrixFile + str(slot).zfill(2) + '.txt'
    else :
        slot_MatrixFile = slot_tpMatrixFile + str(slot).zfill(2) + '.txt'
        
    
    df_Data = pd.read_csv(slot_MatrixFile, sep='\t', index_col=0)
    
    return df_Data

# # get data frame of brute rt_data or tp_data from datatset2
def read_big_data(qosMetric):
   
    if qosMetric == 0 :
        dataFile = big_rtDataFile
    else :
        dataFile = big_tpDataFile
    
    df_data = pd.read_csv(dataFile, sep=' ', names=Data_colnames, header=None, dtype=Data_datatype)
    
    return df_data

# # get data frame of rtMatrix or tpMatrix from datatset1
def read_small_Matrix(qosMetric):
    
    if qosMetric == 0 :
        MatrixFile = small_rtMatrixFile    
    else : 
        MatrixFile = small_tpMatrixFile    

    df_Matrix = pd.read_csv(MatrixFile, sep='\t', header=None)
    
    return df_Matrix

def read_user_list():
    
    return  pd.read_csv(user_listFile, sep='\t', names=user_colnames, header=2, dtype=user_datatype, encoding = 'latin-1')
    

def read_service_list():
    
    return pd.read_csv(service_listFile, sep='\t', names=service_colnames, header=2, dtype=service_datatype, encoding = 'latin-1')
    

