from training_algorithm import Training
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

class Logic_of_training:
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
    
    def l2(self,n_comp:int):
        mm=Training(file_name=self.file_name,number_of_column=self.number_of_column,
                    number_of_components=[n_comp],l2_coefs=np.logspace(-3,15,19))
        response=mm.main()
        return response
    
    def comp(self,l2:np.ndarray,n_comp:int):
        mm=Training(file_name=self.file_name,number_of_column=self.number_of_column,
                    number_of_components=[i for i in range(1,n_comp+1)],l2_coefs=np.array([l2]))
        response=mm.main()
        return response
    
    def img_save_file_name(self):
        return 'loadings/'+self.file_name+'/'+self.names[self.file_name][self.number_of_column]
    
    def easy_plot(self,resp):
        fig = plt.figure(figsize=(17, 10.5),constrained_layout=True)
        plt.title(self.file_name+" "+self.names[self.file_name][self.number_of_column],loc='center')
        spec = fig.add_gridspec(ncols=2, nrows=1)
        row=0
        for col in range(2):
            ax = fig.add_subplot(spec[row, col])
            if col==0:
                for i in range(resp[2]['n_components']):
                    ax.plot(resp[3].w_i[i,:,0],label=str(i))
                ax.set_title('Excitation')
            elif col==1:
                for i in range(resp[2]['n_components']):
                    ax.plot(resp[3].w_k[i,:,0],label=str(i))
                ax.set_title('Emission')
            ax.legend()
        const_part_name:str=self.img_save_file_name()
        Path(const_part_name).mkdir(parents=True, exist_ok=True)
        # plt.savefig( 'loadings/syn/first.jpg')
        plt.savefig(const_part_name+'/'+self.names[self.file_name][self.number_of_column]+'.pdf', format='pdf', dpi=300,bbox_inches='tight')
        plt.savefig(const_part_name+'/'+self.names[self.file_name][self.number_of_column]+'.jpg', format='jpg', dpi=300,bbox_inches='tight')
        plt.savefig(const_part_name+'/'+self.names[self.file_name][self.number_of_column]+".svg", format="svg",bbox_inches='tight')
        plt.show()
    
    def main(self):
        resp=self.l2(self.start_component[self.file_name][self.number_of_column])
        l2_best=resp[3].a
        resp2=self.comp(l2=l2_best,n_comp=self.start_component[self.file_name][self.number_of_column])
        n_comp_best=resp2[3].n_components
        self.easy_plot(resp=resp2)
        return [l2_best,n_comp_best,np.sqrt(resp2[1]['mean_test_mse'][n_comp_best-1])/resp2[-2],
                resp2[1]['mean_test_r2'][n_comp_best-1]]
    



    