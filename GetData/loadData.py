# -*- coding: utf-8 -*-
"""
Created on Fri Dec  4 14:43:53 2020

@author: Evan Hu (Yi Fan Hu)

"""

import os
import pandas as pd

from Tool import globalVars
from Tool.GeneralData import GeneralData
from Tool.Factor import Factor
#%%


materialDataFileDict = {
        'close':'S_DQ_ADJCLOSE.csv',
        'high':'S_DQ_ADJHIGH.csv',
        'low':'S_DQ_ADJLOW.csv',
        'open':'S_DQ_ADJOPEN.csv',
        'preclose':'S_DQ_ADJPRECLOSE.csv',
        'amount':'S_DQ_AMOUNT.csv',
        'volume':'S_DQ_VOLUME.csv',
        'pctChange':'S_DQ_PCTCHANGE.csv'
    }

barraDataFileDict = {
        'beta':'beta.csv',
        'blev':'BLEV.csv'
    }

#%%
PROJ_ROOT = 'C:/Users/eiahb/Documents/MyFiles/WorkThing/tf/01task/GeneticProgrammingProject/AlphaSignalFromMachineLearning'
DATA_PATH = os.path.join(PROJ_ROOT, 'GetData/tables/')

def load_all():
    globalVars.initialize()
    load_material_data() 
    load_barra_data()
    align_barra()
#%% load data functions

def load_data(dataFileDict, DATA_PATH, dictName = None):
    toReturnList = []
    if dictName is not None:
        # add dictionary to globalVars
        if dictName not in globalVars.varList:
            globalVars.register(dictName, {})
            
        for k, v in dataFileDict.items():
            if k not in globalVars.__getattribute__(dictName):
                data = GeneralData(name = k, filePath = os.path.join(DATA_PATH,v))
                globalVars.__getattribute__(dictName)[k] = data
                # print('==================================================================\n\
                #       {} is now in globalVars.{}\n'.format(k, dictName), data)
                globalVars.logger.info('{} is now in globalVars.{}'.format(k, dictName))
                toReturnList.append(k)
            else:
                # print('==================================================================\n\
                #       {} is already in globalVars.{}\n'.format(k, dictName))
                globalVars.logger.info('{} is already in globalVars.{}'.format(k, dictName))
    else:
        for k, v in dataFileDict.items():
            data = GeneralData(name = k, filePath = os.path.join(DATA_PATH,v))
            globalVars.register(k, data)
            toReturnList.append(k)
    return(toReturnList)

def load_material_data(dataFileDict = materialDataFileDict, DATA_PATH = DATA_PATH+'materialData'):
    return(load_data(dataFileDict = dataFileDict, DATA_PATH = DATA_PATH, dictName='materialData'))


def simple_load_factor(factorName):
    if 'factors' not in globalVars.varList:
        globalVars.register('factors', {})
    globalVars.factors['{}_factor'.format(factorName)] = Factor('{}_factor'.format(factorName), globalVars.materialData[factorName])
    print(factorName, 'is now in globalVars.factors')
    
    
    
def load_barra_data(dataFileDict = barraDataFileDict, DATA_PATH = DATA_PATH+'barra'):
    return(load_data(dataFileDict = dataFileDict, DATA_PATH = DATA_PATH, dictName='barra'))



#%%
    

def align_data(data, alignTo):
    data_df = pd.DataFrame(data.generalData, index=data.timestamp, columns=data.columnNames)
    reindexed = data_df.reindex(index=alignTo.timestamp, columns=alignTo.columnNames)
    toReturn = GeneralData(data.name, generalData=reindexed)
    return(toReturn)

def align_barra():
    try:
        for k, v in globalVars.barra.items():
            globalVars.barra[k] = align_data(v, globalVars.materialData['close'])
        return(True)
    except :
        return(False)
        
    
    
    
#%% main
if __name__ == '__main__':
    try:
        DATA_PATH = os.path.join(PROJ_ROOT, 'GetData/tables/')
        load_material_data()
        load_barra_data()
    except :
        globalVars.initialize()
        load_material_data()
        load_barra_data()
    
#%% alignData
    aB = globalVars.barra['beta']
    aM = globalVars.materialData['open']
    data = aB
    alignTo = aM
    print(align_data(aM, aB))
    
    simple_load_factor('close')
    align_barra()




