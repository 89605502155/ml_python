from training_algorithm import Training
import asyncio 
import numpy as np
import json
from open import Open_file
import pandas as pd
from npls import npls
from centering_and_cross_validation import Cross_validation as cv
from paint_scripts.paint_snr_by_n_comp_for_different_l2_coefs import paint_snr_by_n_comp_for_different_l2_coefs


class signal_noise_for_all_components_from_l2:
    def __init__(self,file_name:str='syn',number_of_column:int=0,
                 l2:np.ndarray=np.array([0.1]),
                 number_components_list:list=[i for i in range(1,11)],
                 derivative_rang:list=[2],norm_func:list=['manhattan']) -> None:
        self.file_name=file_name
        self.number_of_column=number_of_column
        self.l2=l2
        self.result = None
        self.number_components_list=number_components_list
        self.derivative_rang=derivative_rang
        self.norm_func=norm_func
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

    async def process_item(self,j, params):
        file_name, number_of_column, number_components_list, derivative_rang, norm_func = params
        resoult = {}
        model = Training(
            file_name=file_name,
            number_of_column=number_of_column,
            number_of_components=[number_components_list[-1]],
            l2_coefs=np.array([j]),
            regression_method=npls,
            derivative_rang=derivative_rang,
            norm_func=norm_func
        )
        response = await asyncio.to_thread(model.main)
        snr_emission = response[3].snr_emission
        snr_excitation = response[3].snr_excitation
        resoult[j] = {'Emission': snr_emission, 'Excitation': snr_excitation}
        return resoult

    async def parallel_execution(self):
        tasks = []
        params = (self.file_name, self.number_of_column, self.number_components_list,
                self.derivative_rang, self.norm_func)
        for j in self.l2:
            tasks.append(self.process_item(j, params))

        results = await asyncio.gather(*tasks)
        return {j: result for r in results for j, result in r.items()}

    async def calculation_snr(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            self.result = await self.parallel_execution()
        finally:
            loop.close()


# После этого можно использовать self.resoult
  
    def calculation_snr_(self):
        self.result={}
        for j in self.l2:
            self.result[j]={}
            model=Training(file_name=self.file_name,number_of_column=self.number_of_column,
                    number_of_components=[self.number_components_list[-1]],l2_coefs=np.array([j]), 
                    regression_method=npls, derivative_rang=self.derivative_rang,
                    norm_func=self.norm_func)
            response=model.main()
            snr_emission=response[3].snr_emission
            snr_excitation=response[3].snr_excitation
            self.result[j]={'Emission':snr_emission, 'Excitation':snr_excitation}
    
    def paint(self,save):
        data_set_name=self.data_set_names[self.file_name]
        fluor_name=self.names[self.file_name][self.number_of_column]
        painter=paint_snr_by_n_comp_for_different_l2_coefs()
        painter.main(snr_data_dict=self.result,data_set_name=data_set_name,
                     fluorophore_name=fluor_name,save=save,metric_name=self.norm_func[0])
        
    

        
           