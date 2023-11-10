from training_algorithm import Training
import numpy as np
from paint_scripts.rmse_plot import Rmse_Plot
import json

class Controller_for_the_rmse_plot:
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

    def l2(self,n_comp:int):
        mm=Training(file_name=self.file_name,number_of_column=self.number_of_column,
                    number_of_components=[n_comp],l2_coefs=np.logspace(-3,8,12))
        response=mm.main()
        response.append(np.logspace(-3,8,12))
        return response
    
    def comp(self,l2:np.ndarray,n_comp:int):
        mm=Training(file_name=self.file_name,number_of_column=self.number_of_column,
                    number_of_components=[i for i in range(1,n_comp+1)],l2_coefs=np.array([l2]))
        response=mm.main()
        response.append([i for i in range(1,n_comp+1)])
        return response
    
    def main(self):
        resp=self.l2(self.start_component[self.file_name][self.number_of_column])
        l2_best=resp[3].a
        self.resp2=self.comp(l2=l2_best,n_comp=self.start_component[self.file_name][self.number_of_column])
        n_comp_best=self.resp2[3].n_components
        self.resp3=self.l2(n_comp_best)


        # a=Rmse_Plot()
        # a.main(rmse_l2=np.sqrt(resp3[1]['mean_test_mse'])/resp3[4],l2=resp3[-1],
        #        rmse_ncomp=np.sqrt(resp2[1]['mean_test_mse'])/resp2[4],n_comp=resp2[-1],
        #        data_set_name=self.data_set_names[self.file_name],
        #        fluorophore_name=self.names[self.file_name][self.number_of_column],
        #        save=True
        #        )
        param={
            'rmse_l2':list(np.sqrt(self.resp3[1]['mean_test_mse'])/self.resp3[4]),
            'l2':list(self.resp3[-1]),
            'rmse_ncomp':list(np.sqrt(self.resp2[1]['mean_test_mse'])/self.resp2[4]),
            'n_comp':list(self.resp2[-1]),
            'data_set_name':self.data_set_names[self.file_name],
            'fluorophore_name':self.names[self.file_name][self.number_of_column],
        }
        print(param)
        with open('rmse_'+self.data_set_names[self.file_name]+'_'+self.names[self.file_name][self.number_of_column]+'.json', 'w') as fp:
            json.dump(param, fp)
        return [l2_best,n_comp_best,np.sqrt(self.resp2[1]['mean_test_mse'][n_comp_best-1])/self.resp2[-2],
                self.resp2[1]['mean_test_r2'][n_comp_best-1]]
    
    def paint(self):
        a=Rmse_Plot()
        a.main(rmse_l2=np.sqrt(self.resp3[1]['mean_test_mse'])/self.resp3[4],l2=self.resp3[-1],
               rmse_ncomp=np.sqrt(self.resp2[1]['mean_test_mse'])/self.resp2[4],n_comp=self.resp2[-1],
               data_set_name=self.data_set_names[self.file_name],
               fluorophore_name=self.names[self.file_name][self.number_of_column],
               save=True
               )
        
    
