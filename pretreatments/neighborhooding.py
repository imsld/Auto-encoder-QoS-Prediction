'''
Created on 26 janv. 2018

@author: N'TIC
'''
import pretreatments.io_operations as io
import numpy as np

def get_service_country_list(service_max):
    df_service_list = io.read_service_list()
    df_service_list= df_service_list[df_service_list.service_ID < service_max]
    return np.unique(np.array(df_service_list['country'])), df_service_list 

def get_list_service_same_country(df_service, country):
    df = df_service[df_service.country == country]
    return np.array(df['service_ID'])

def get_service_provider_list(service_max):
    df_service_list = io.read_service_list()
    df_service_list= df_service_list[df_service_list.service_ID < service_max]
    return np.unique(np.array(df_service_list['service_provider'])), df_service_list 

def get_list_service_same_provider(df_service, provider):
    df = df_service[df_service.service_provider == provider]
    return np.array(df['service_ID'])

def get_service_asn_list(service_max):
    df_service_list = io.read_service_list()
    df_service_list= df_service_list[df_service_list.service_ID < service_max]
    df = df_service_list['asn']
    df = df.dropna()
    df = df.drop_duplicates()
    #
    return np.unique(np.array(df)), df_service_list 

def get_list_service_same_asn(df_service, asn):
    df = df_service[df_service.asn == asn]
    return np.array(df['service_ID'])