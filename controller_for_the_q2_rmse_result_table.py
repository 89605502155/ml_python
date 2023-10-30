from training_algorithm import Training
import numpy as np
import json
from open import Open_file
from open import Open_Synthetic_theoretical_loadings
from theory_practice_loadings import Theory_practice_loadings
import pandas as pd
from npls import npls

class Controller_for_the_resoult_table:
    def __init__(self,file_name:str='syn',number_of_column:int=0) -> None:
        self.file_name=file_name
        self.number_of_column=number_of_column
        self.start_component={
            'syn':[4,4,4,4],
            'asmund':[7,5,7,6,7,7],
            'dorrit':[5,5,4,4],
            'marat':[3,3,4]
        }
        self.names={
            'syn':['first','second','third','fourth'],
            'asmund':['catechol','hydroquinone','indole','resorcinol','tryptophane','tyrosine'],
            'dorrit':['hydroquinone','tryptophane','phenylalanine','DOPA'],
            'marat':['humic','tyrosine','tryptophane']
        }
        self.data_set_names={
            'syn':'synthetic',
            'asmund':'asmund',
            'dorrit':'dorrit',
            'marat':'marat'
        }

    def get_best_param_for_traing(self,data_set_name,fluor_name):
        with open('results_json/rmse_'+data_set_name+'_'+fluor_name+'.json',"r") as file:
            data_dict = json.loads(file.read())
        data_dict['rmse_l2']
        index_l2= data_dict['rmse_l2'].index(min(data_dict['rmse_l2']))
        index_n_comp= data_dict['rmse_ncomp'].index(min(data_dict['rmse_ncomp']))
        # print(data_set_name,fluor_name,data_dict['l2'][index_l2],data_dict["n_comp"][index_n_comp],
        #       data_dict['rmse_l2'][index_l2],data_dict['rmse_ncomp'][index_n_comp])
        return data_dict['l2'][index_l2],data_dict["n_comp"][index_n_comp]
    
    def set_best_param_from_Train_algorithm_response(self,response):
        mse=np.array(response[1][ "mean_test_mse" ])
        rmse=np.sqrt(mse)
        nrmse=np.array(rmse/response[-2])
        min_index=np.argmin(nrmse)
        return nrmse[min_index],response[1][ "mean_test_r2" ][min_index],min_index
    
    def results(self,data_set_name,fluor_name):
        l2,n_comp=self.get_best_param_for_traing(data_set_name,fluor_name)
        mm=Training(file_name=self.file_name,number_of_column=self.number_of_column,
                        number_of_components=[n_comp],l2_coefs=np.array([l2]))
        response=mm.main()
        nrmse,q2,index=self.set_best_param_from_Train_algorithm_response(response=response)
        print(data_set_name,fluor_name,n_comp,np.log10(l2),nrmse,q2,index,l2)

    def main(self):
        self.results(data_set_name=self.data_set_names[self.file_name],
                    fluor_name=self.names[self.file_name][self.number_of_column])
        



