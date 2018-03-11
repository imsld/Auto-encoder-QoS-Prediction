'''
Created on 21 janv. 2018

@author: N'TIC
'''

import sys
import os.path
import numpy as np
import time

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from pretreatments import neighborhooding as voisinage
from autoencoders import autoencoder as ae
from validation import operations as op
from pretreatments import io_operations as io

import logging

logging.getLogger("tensorflow").setLevel(logging.WARNING)
logging.getLogger('tensorflow').disabled = True

import tensorflow as tf

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

#***********************************************************************************
# RT/TP data set:                                                                  *  
#    initially missing values     ---->    10609313 (25.94%) --> density 74.06%    *
#    after updated missing value  ---->     9442660 (23.08%) --> density 76.02%    *
#***********************************************************************************

#***********************************************************************************
# Cross validation on 64 slots where :                                             *
#    08 slots for testing base (size_window = 8)                                   *
#    56 slots for testing base                                                     *
#***********************************************************************************
params = {
        'seuil_best_min':0.01,
        'dataDensity' : 76,  # 76% select rtMatrix_max_density_slot_n_.txt #74% select rtMatrix_update_slot_n.txt
        'qosMetric': 0,  # 0 for rt Qos et 1 for tp Qos
        'size_window' : 8,
        'learning_rate':0.01,  # [0.001, 0.01],
        'n_epoch' : 5000,  # 5000, 2500
        'users' : 142,
        'services' : 4500,
        'layer_sizes': [20],  # [120, 100], #[80, 60]
        'k_fold' : 8,
        'Neighborhood_user' : 'All',  # other values 'Provider' 'Country', 'All'
        'Neighborhood_service' : 'Country'  # other values 'Provider' 'Country', 'All'        
    }

def get_slots_matrix(qosMetric, list_service_same_country):
    slot_list = list(range(64))
    items = []
    if list_service_same_country is not None:
        for i in list_service_same_country :
            items.append(str(i))
                    
    filtred_slot_matrix = []
    for slot in slot_list:
        
        if (params['dataDensity'] == 76):
            data = io.read_max_density_MatrixBySlot(qosMetric, slot)
        else:    
            data = io.read_updated_MatrixBySlot(qosMetric, slot)
            
        if list_service_same_country is not None:
            data = data.filter(items)
        
        data = data.fillna(0)

        matrix = data.as_matrix()
        filtred_slot_matrix.append(matrix)
        
    return filtred_slot_matrix

def Validation(liste, qosMetric, size_service, list_service_same, file):
    slot_list = list(range(64))
    try:
        all_matrix = get_slots_matrix(qosMetric, list_service_same)
    except:
        file.write("\n"+"error 1")
    else:
        x = tf.placeholder("float", [None, size_service])    
        sess = tf.Session()
                
        for dim in liste:
            
            global_moy_rmse, global_moy_mae, total_time = 0, 0, 0
            
            for i in range(params['k_fold']):
                            
                _start_time = time.time()
                
                slot_training_list, slot_testing_list = op.folds_cross_validation(i, params['size_window'],params['k_fold'], slot_list)
                
                autoencoder = ae.create(x, [dim])
                
                init = tf.global_variables_initializer()               
                sess.run(init)
                
                train_step = tf.train.GradientDescentOptimizer(params['learning_rate']).minimize(autoencoder['RMSE'])
                
                min_rmse = 100

                for _nepoch in range(params['n_epoch']):  
                    
                    if min_rmse < params['seuil_best_min']:
                        break              
                    
                    for lot in (slot_training_list):
                        
                        one_matrix = all_matrix[lot]                                                                                                  
                        
                        sess.run(train_step, feed_dict={x: one_matrix})                    
                        
                        result_run = sess.run(autoencoder, feed_dict={x: one_matrix})
                        
                        rmse = result_run['RMSE']
                        
                        if min_rmse > rmse:
                            min_rmse = rmse
                            best_model = result_run                            
                        
                        del one_matrix
                        
                        if min_rmse < params['seuil_best_min']:
                            break
                                       
                moy_rmse, moy_mae = get_rmse(sess, list_service_same, qosMetric, slot_testing_list, best_model)
                
                writer = tf.summary.FileWriter('./mygraph_', sess.graph)
                writer.close()
                
                global_moy_rmse += moy_rmse
                global_moy_mae += moy_mae
                
                _interval = time.time() - _start_time
                total_time += _interval 
                
                str_1 = str(dim) + '\t' + str(i) + '\t' + str(moy_rmse) + '\t' + str(moy_mae) + '\t' + str(_interval / 60)  
                print(str_1)
                file.write('\n' + str_1)
            
            str_2 = op.messages['msg_4']
            str_3 = '\t' + '\t' + str(global_moy_rmse / params['k_fold']) + '\t' + str(global_moy_mae / params['k_fold']) + '\t' + str(total_time / 60) 
            print(str_2)
            print(str_3)
            file.write('\n' + str_2)
            file.write('\n' + str_3)
            
def get_rmse(sess,list_service_same, qosMetric, slot_testing_list, best_model):
    
    somme_rmse_nan = 0;
    somme_mae_nan = 0;
    
    nb_slot = params['size_window']
    
    items = []
    if list_service_same is not None:
        for i in list_service_same :
            items.append(str(i))
            
    for slot in slot_testing_list:
        data = io.read_updated_MatrixBySlot(qosMetric, slot)
        if list_service_same is not None:
            data = data.filter(items)
                
        if (data.size != data.isnull().values.sum()):
        
            data_ = data.fillna(0)
            matrix = data_.as_matrix()
        
            result_new_rmse_nan, result_new_mae_nan = ae.get_rmse_mae_Vlaues(sess,matrix, best_model, data)
        
            somme_rmse_nan += result_new_rmse_nan
            somme_mae_nan += result_new_mae_nan
        else:
            nb_slot -=1

    local_moy_rmse_nan = somme_rmse_nan / nb_slot
    local_moy_mae_nan = somme_mae_nan / nb_slot
    
    return local_moy_rmse_nan, local_moy_mae_nan  
            
def crossValidation(debut, fin, id_):
    
    start_time = time.time()
    liste = np.array(params['layer_sizes'])
    qosMetric = params['qosMetric']
    
    file_name = '_'+str(id_)+'new_result_density=' + str(params['dataDensity']) + '%_qos=' + str(params['qosMetric']) + '_layersize=' + str(params['layer_sizes']) + '_neigh=' + str(params['Neighborhood_service'])
    
    try:
        # without neighborhood 
        if (params['Neighborhood_user'] == 'All') and (params['Neighborhood_service'] == 'All'):    
            
            Validation(liste, qosMetric, params['services'], None)
        
        else:
            # with neighborhood on Country for services
            if (params['Neighborhood_user'] == 'All') and (params['Neighborhood_service'] == 'Country'):
                liste_cluster, df_service = voisinage.get_service_country_list(params['services'])
            
            if (params['Neighborhood_user'] == 'All') and (params['Neighborhood_service'] == 'Provider'):
                liste_cluster, df_service = voisinage.get_service_provider_list(params['services'])
                
            if (params['Neighborhood_user'] == 'All') and (params['Neighborhood_service'] == 'asn'):
                liste_cluster, df_service = voisinage.get_service_asn_list(params['services'])
        
            count = len(liste_cluster)
            step = 0        
        
            for value in liste_cluster:
                
                step+=1
                
                if (step<int(debut)):
                    continue
                
                if (step>int(fin)):
                    continue
                
                
                if (params['Neighborhood_user'] == 'All') and (params['Neighborhood_service'] == 'Country'):
                    list_service_same = voisinage.get_list_service_same_country(df_service, value)
                    
                if (params['Neighborhood_user'] == 'All') and (params['Neighborhood_service'] == 'Provider'):
                    list_service_same = voisinage.get_list_service_same_provider(df_service, value)
                
                if (params['Neighborhood_user'] == 'All') and (params['Neighborhood_service'] == 'asn'):
                    list_service_same = voisinage.get_list_service_same_asn(df_service, value)
                
                total_ser = len(list_service_same)
                
                if total_ser == 0:
                    step-=1
                    continue
                
                str_1 = op.messages['msg_1'] + str(value) + '\t(' + str(step) + '/' + str(count) + ')\t-->\t services :\t' + str(total_ser)
                str_2 = op.messages['msg_2'] 
    
                print(str_1)
                print(str_2)
                
                file = op.getFile(file_name)
                file.write('\n' + str_1)
                file.write('\n' + str_2)
            
                Validation(liste, qosMetric, total_ser, list_service_same,file)
            
                file.close
    except:
        file = op.getFile(file_name)
        file.write('\n' + 'Error 2')
    finally:
        interval = time.time() - start_time
        str_3 = op.messages['msg_2'] + str(interval / 60)
        print (str_3)
        file = op.getFile(file_name)
        file.write('\n' + str_3)
        file.close


local = 1
if (local==1):
    params['qosMetric']=0
    params['layer_sizes']=[40] 
    debut = 4
    fin = 4
    id_ = 1
else:
    params['layer_sizes']=[int(sys.argv[1])] 
    debut = sys.argv[2]
    fin = sys.argv[3]
    id_ = sys.argv[4]

crossValidation(debut, fin,id_)