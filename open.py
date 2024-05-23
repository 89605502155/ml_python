import numpy as np
from dataset_model import Dataset_model
from dataset_model import Dataset_model_with_theoretical_loadings_only_for_synthetic
import pickle as pkl
import pandas as pd
from gzip import open

class Open_file:
    def __init__(self):
        self.number_fields={
            'syn':4,
            'asmund':6,
            'dorrit':4,
            'marat':3
        }

    def syn_open(self)-> Dataset_model:
        d=np.load('data/2021-11-17.npz')
        names=['first','second','third','fourth']
        resoult = Dataset_model(Sectrun=d['X']*1e7,Consentration=d['Y']*1e1,Exitation_wale=d['Ex'],
                                Emission_wale=d['Em'],Name_of_column_list=names)
        return resoult
    
    def asmund_open(self)-> Dataset_model:
        d=np.load('data/fluordata_2021-11-18.npz')
        names=['catechol','hydroquinone','indole','resorcinol','tryptophane','tyrosine']
        resoult = Dataset_model(Sectrun=d['EEM2'],Consentration=d['Y']*1e6,Exitation_wale=d['Ex'],
                                Emission_wale=d['Em'],Name_of_column_list=names)
        return resoult
    
    def dorrit_open(self)-> Dataset_model:
        d1=np.load('data/dorrit2_2021-11-18.npz')
        d2=np.load('data/Dorrit.npz')
        names=['hydroquinone','tryptophane','phenylalanine','DOPA']
        y=list()
        # y[:,0]=d1['Y'][:,0]
        # y[:,1]=d1['Y'][:,1]
        # y[:,2]=d1['Y'][:,2]*0.02
        # y[:,3]=d1['Y'][:,3]
        resoult = Dataset_model(Sectrun=d1['EEM'][:,:,10:],Consentration=d1['Y'],
                                Exitation_wale=d2['Ex'][10:],Emission_wale=d2['Em'],
                                Name_of_column_list=names)
        resoult.Consentration[:,2]*=0.02
        return resoult
    
    def dorrit_open_all(self)-> Dataset_model:
        d1=np.load('data/dorrit2_2021-11-18.npz')
        d2=np.load('data/Dorrit.npz')
        names=['hydroquinone','tryptophane','phenylalanine','DOPA']
        y=list()
        # y[:,0]=d1['Y'][:,0]
        # y[:,1]=d1['Y'][:,1]
        # y[:,2]=d1['Y'][:,2]*0.02
        # y[:,3]=d1['Y'][:,3]
        resoult = Dataset_model(Sectrun=d1['EEM'][:,:,:],Consentration=d1['Y'],
                                Exitation_wale=d2['Ex'][:],Emission_wale=d2['Em'],
                                Name_of_column_list=names)
        resoult.Consentration[:,2]*=0.02
        return resoult
    
    def marat_open(self)-> Dataset_model:
        Xdata = pkl.load(open('data/X_new.pkl.gz', 'rb'))
        Ydata = pkl.load(open('data/y.pkl.gz', 'rb'))
        names=['humic','tyrosine','tryptophane']
        resoult = Dataset_model(Sectrun=np.array(Xdata['X']),Consentration=np.array(Ydata),
                                Exitation_wale=np.array(Xdata['excitation']),
                                Emission_wale=np.array(Xdata['emission']),
                                Name_of_column_list=names)
        resoult.Consentration[:,1]*=10
        resoult.Consentration[:,2]*=10
        return resoult
    
    def marat_open_96(self)-> Dataset_model:
        d1=np.load('data/marat_095.npz')
        names=['humic','tyrosine','tryptophane']
        resoult = Dataset_model(Sectrun=d1['Spectrum'][:,:,:],Consentration=d1['Concentration'],
                                Exitation_wale=d1['Excitation'],Emission_wale=d1['Emission'],
                                Name_of_column_list=names)
        return resoult
    
    def marat_open_60(self)-> Dataset_model:
        d1=np.load('data/marat_06.npz')
        names=['humic','tyrosine','tryptophane']
        resoult = Dataset_model(Sectrun=d1['Spectrum'][:,:,:],Consentration=d1['Concentration'],
                                Exitation_wale=d1['Excitation'],Emission_wale=d1['Emission'],
                                Name_of_column_list=names)
        return resoult

    def help(self):
        print("For work call main function and put 'syn','asmund' or 'dorrit','marat'")

    def getNeedFilesNamesFromDataFolder(self)->list:
        return ['2021-11-17.npz','fluordata_2021-11-18.npz','dorrit2_2021-11-18.npz','Dorrit.npz','X_new.pkl.gz','y.pkl.gz']
    
    def get_number_column_concentration(self):
        return self.number_fields
        
    def main(self,file_name:str)-> Dataset_model:
        if file_name=='syn':
            return self.syn_open()
        elif file_name=='asmund':
            return self.asmund_open()
        elif file_name=='dorrit':
            return self.dorrit_open()
        elif file_name=='dorrit_all':
            return self.dorrit_open_all()
        elif file_name=='marat':
            return self.marat_open()
        elif file_name=='marat96':
            return self.marat_open_96()
        elif file_name=='marat60':
            return self.marat_open_60()
        else:
            raise NameError('Нет такого datasets. Выбери из syn asmund dorrit marat.'+
                            'Или перейди в файл open.py своего проекта.')
        
class Open_Synthetic_theoretical_loadings(Open_file):
    def __init__(self):
        super().__init__()

    def syn_open(self)-> Dataset_model_with_theoretical_loadings_only_for_synthetic:
        d=np.load('data/2021-11-17.npz')
        names=['first','second','third','fourth']
        # resoult = Dataset_model(Sectrun=d['X']*1e7,Consentration=d['Y']*1e1,Exitation_wale=d['Ex'],
        #                         Emission_wale=d['Em'],Name_of_column_list=names)
        resoult2 = Dataset_model_with_theoretical_loadings_only_for_synthetic(Sectrun=d['X']*1e7,Consentration=d['Y']*1e1,Exitation_wale=d['Ex'],
                                Emission_wale=d['Em'],Name_of_column_list=names,
                                emission_theoretical_loadings=d['B0'],
                                excitation_theoretical_loadings=d['C0'])
        return resoult2
    
    def main(self,file_name:str)-> Dataset_model_with_theoretical_loadings_only_for_synthetic:
        if file_name=='syn':
            return self.syn_open()