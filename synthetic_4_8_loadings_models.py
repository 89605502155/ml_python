from training_algorithm import Training
import numpy as np
from npls import npls
from paint_scripts.plot_list_of_loadings_and_nrmse import Plot_list_of_loadings_and_nrmse
from open import Open_file

class Synthetic_Four_Eight_Loadings:
    def __init__(self,number_of_column:int=0,number_of_components:int=8) -> None:
        self.number_of_column=number_of_column
        self.number_of_components=number_of_components
        self.fluorophore_name=['first','second','third','fourth'][self.number_of_column]

    def train(self,number_components):
        model=Training(file_name='syn',number_of_column=self.number_of_column,
                       regression_method=npls, number_of_components=number_components,
                       l2_coefs=np.array([100]))
        response=model.main()
        return response
    
    def main(self,save:bool=False):
        resp=self.train(number_components=[i for i in range(1,self.number_of_components+1)])
        nrmse:np.ndarray=np.sqrt(resp[1]["mean_test_mse"])/resp[4]
        resp2=self.train(number_components=[self.number_of_components])
        w_i=resp2[3].w_i
        w_k=resp2[3].w_k
        b=Open_file()
        a=b.main(file_name='syn')
        painter=Plot_list_of_loadings_and_nrmse()
        painter.main(w_i=w_i,w_k=w_k,nrmse=nrmse,emission_wave_lenth=a.Emission_wale,
                     excitation_wave_lenth=a.Exitation_wale,fluorophore_name=self.fluorophore_name,
                     save=save)
    
    
