from training_algorithm import Training
import numpy as np
import json
from open import Open_file
from open import Open_Synthetic_theoretical_loadings
from theory_practice_loadings import Theory_practice_loadings
import pandas as pd
from npls import npls
from centering_and_cross_validation import Cross_validation as cv

class Controller_for_loadings_plot:
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
        print(data_set_name,fluor_name,data_dict['l2'][index_l2],data_dict["n_comp"][index_n_comp],
              data_dict['rmse_l2'][index_l2],data_dict['rmse_ncomp'][index_n_comp])
        return data_dict['l2'][index_l2],data_dict["n_comp"][index_n_comp]
    
    def find_clean_spectrum(self,concentrations:np.ndarray):
        df1=pd.DataFrame(concentrations,columns=self.names[self.file_name])
        df1.loc[:,'sum']=df1.sum(numeric_only=True, axis=1)
        my=df1.loc[(df1.loc[:,'sum']==df1.loc[:,self.names[self.file_name][self.number_of_column]]) &
                   (df1.loc[:,'sum']>0)]
        count_row = my.shape[0]
        # print(df1)
        # print("my",my)
        # print("c",count_row," r",my.index,my.index[0])
        if count_row>0:
            return True, my.index[0]
        else:
            return False,0

    def practise_loadings(self,data_set_name,fluor_name,save):
        l2,n_comp=self.get_best_param_for_traing(data_set_name,fluor_name)
        b=Open_file()
        data=b.main(file_name=self.file_name)
        continue_,index=self.find_clean_spectrum(data.Consentration)
        if continue_:
            model=npls(n_components=n_comp,a=l2)
            aaa=data.Sectrun[index,:,:].reshape(1,data.Sectrun.shape[1],data.Sectrun.shape[2])
            # print(aaa.shape)
            model.fit(xtrain=aaa,ytrain=np.array([data.Consentration[:,self.number_of_column][index]]))
            w_i_th=model.w_i
            w_k_th=model.w_k
            mm=Training(file_name=self.file_name,number_of_column=self.number_of_column,
                        number_of_components=[n_comp],l2_coefs=np.array([l2]))
            response=mm.main()
            w_i=response[3].w_i #excitation
            w_k=response[3].w_k
            
            # print(w_i.shape,data.Emission_wale.shape)

            plot=Theory_practice_loadings(practice_emission_loadings=np.array(w_k[0,:,0]),
                            theory_emission_loadings=np.array(w_k_th[0,:,0]),
                            emission_wave_lenth=data.Emission_wale,
                            excitation_wave_lenth=data.Exitation_wale,
                            practice_excitation_loadings=np.array(w_i[0,:,0]),
                            theory_excitation_loadings=np.array(w_i_th[0,:,0]))
            plot.main(data_set_name=data_set_name,fluorophore_name=fluor_name,save=save)
    
    def main(self,save:bool=False):
        self.practise_loadings(data_set_name=self.data_set_names[self.file_name],
                               fluor_name=self.names[self.file_name][self.number_of_column],save=save)
        
class Controller_for_loadings_plot_for_synthetic_dataset(Controller_for_loadings_plot):
    def __init__(self,file_name:str='syn',number_of_column:int=0):
        super().__init__(file_name=file_name,number_of_column=number_of_column)

    def practise_loadings(self,data_set_name,fluor_name,save):
        l2,n_comp=self.get_best_param_for_traing(data_set_name,fluor_name)
        b=Open_Synthetic_theoretical_loadings()
        data=b.main(file_name=self.file_name)

        mm=Training(file_name=self.file_name,number_of_column=self.number_of_column,
                        number_of_components=[n_comp],l2_coefs=np.array([l2]))
        response=mm.main()
        w_i=response[3].w_i #excitation
        w_k=response[3].w_k

        plot=Theory_practice_loadings(practice_emission_loadings=np.array(w_k[0,:,0]),
                            theory_emission_loadings=data.emission_theoretical_loadings[:,self.number_of_column],
                            emission_wave_lenth=data.Emission_wale,
                            excitation_wave_lenth=data.Exitation_wale,
                            practice_excitation_loadings=np.array(w_i[0,:,0]),
                            theory_excitation_loadings=data.excitation_theoretical_loadings[:,self.number_of_column],
                            x_label_control=True)
        plot.main(data_set_name=data_set_name,fluorophore_name=fluor_name,save=save)

