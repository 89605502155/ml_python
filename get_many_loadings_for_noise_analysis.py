from open import Open_file, Open_Synthetic_theoretical_loadings
from npls import npls
import numpy as np
import pickle as pkl
from glob import glob
from gzip import open # NB: overrides standard open()
import os
from paint_scripts.paint_one_loading_and_her_snr import Plot_one_loading_and_her_snr
from signal_noise import signal_noise
from IPython.display import clear_output

class get_many_loadings_for_noise_analysis:
    def __init__(self) -> None:
        self.list_of_files=['syn','asmund','dorrit','marat']
        self.number_fields={
            'syn':4,
            'asmund':6,
            'dorrit':4,
            'marat':3
        }

    def one_itter(self,loading,wave_lenth,dataset_name,fluorophore,kind):
        s_i=signal_noise()
        res1=s_i.main(loading,wave_lenth)  #excitation
        
        pl=Plot_one_loading_and_her_snr()
        pl.painter(res1['evklid'],loading=loading,wave_lenghts=wave_lenth)
        sm_i=input("Введите 1, если нагрузка гладкая, и 0, если нет ")
        self.W_arr.append(loading)
        self.W_inf_arr.append(dataset_name+" "+str(fluorophore)+" "+kind+" evklid 2")
        self.W_noise.append(res1['evklid'])
        self.w_smooth.append(sm_i)

    def main(self):
        self.W_arr=list()
        self.W_inf_arr=list()
        self.W_noise=list()
        self.w_smooth=list()
        for dataset_name in self.list_of_files:
            op=Open_file()
            data=op.main(dataset_name)
            for fluorophore in range(self.number_fields[dataset_name]):
                reg_model=npls(n_components=20,a=1,excitation_wavelenth=data.Exitation_wale,
                               emission_wavelenth=data.Emission_wale)
                train_resp=reg_model.fit(data.Sectrun,data.Consentration[:,fluorophore])
                for i in range(20):
                    self.one_itter(loading=train_resp.w_i[i,:,0],wave_lenth=data.Exitation_wale,
                                   dataset_name=dataset_name,fluorophore=fluorophore,kind="Excitation")
                    clear_output(wait=True)
                    self.one_itter(loading=train_resp.w_k[i,:,0],wave_lenth=data.Emission_wale,
                                   dataset_name=dataset_name,fluorophore=fluorophore,kind="Emission")
                    clear_output(wait=True)
        op=Open_Synthetic_theoretical_loadings()
        data=op.main('syn')
        for i in range(4):
            self.one_itter(loading=data.emission_theoretical_loadings[:,i],wave_lenth=data.Emission_wale,
                           dataset_name="synthetic",fluorophore=i,kind="emission")
            clear_output(wait=True)
            self.one_itter(loading=data.excitation_theoretical_loadings[:,i],wave_lenth=data.Exitation_wale,
                           dataset_name="synthetic",fluorophore=i,kind="excitation")
            clear_output(wait=True)
        

        pkl.dump(
            {'loadings': self.W_arr, 'information_about_load': self.W_inf_arr,
              'snr_evklid_second': self.W_noise, 'is_smooth':self.w_smooth},
            open('smoother_of_loadings.pkl.gz', 'wb')
        )