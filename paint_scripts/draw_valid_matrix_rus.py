import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
from dataset_model import Dataset_model as dm
# from dataset_model import Cross_validation_dataset_model as cvdm
from dataset_model import Centering_dataset_model as cdm
from pathlib import Path
from matplotlib.ticker import MultipleLocator

class Draw_valid_matrix_rus:
    def __init__(self,data:np.ndarray,l2:np.ndarray,n_comp:list,substanse_name:str,
                 metrics_name:str) -> None:
        self.data=data
        self.l2=np.log10(l2)
        self.n_comp=n_comp
        self.substance_name=substanse_name
        self.metrics_name=metrics_name



    
    def make_dir_name(self,name_dataset:str|None)->str:
        if name_dataset==None:
            return 'plots4/ru_metrics/none/'+self.substance_name
        else:
            return 'plots4/ru_metrics/'+str(name_dataset)+'/'+self.substance_name


    def make_full_name_file(self,name_dataset:str|None)->str:
        return self.make_dir_name(name_dataset=name_dataset)+'/'+'spectrum_'+str(self.metrics_name)

    def main(self,save:bool=False,name_of_dataset:str|None=None,label_x_number_size:int=30,
             label_y_number_size:int=30,pad:int=15, label_name_fontsize:int=40):
        self.plot(save=save,file_name=self.make_full_name_file(name_of_dataset),
                  label_x_number_size=label_x_number_size,
                  label_y_number_size=label_y_number_size,pad=pad,
                  label_name_fontsize=label_name_fontsize,
                  data_set_name=name_of_dataset)

    def plot(self,save,file_name:str,label_x_number_size:int,label_y_number_size:int,pad:int,
             label_name_fontsize:int,data_set_name:str|None=None):
        mpl.rc('font',family='Times New Roman')
        fg = plt.figure(figsize=(12,8),constrained_layout=False)
        gs = gridspec.GridSpec(ncols=1, nrows=1, figure=fg)
        #plt.title("Центрирование спектра образца 5",  {'fontname':'Times New Roman'}, fontsize=28,loc="center" ,pad=45)

        plt.subplots_adjust(wspace=0, hspace=0)

        fig_ax_1 = fg.add_subplot(gs[0])
        #plt.imshow(on+tw+th+fo+trtrt,aspect="auto", origin='lower')
        plt.imshow(self.data,aspect="auto", origin='lower',extent=[self.l2[0]-0.5,
                                                                     self.l2[-1]+0.5,
                                                                     self.n_comp[0]-0.5,
                                                                     self.n_comp[-1]+0.5])
        plt.ylabel("Количество компонент" , fontsize=label_name_fontsize,labelpad=pad)
        plt.xlabel("Коэффициент L$_{2}$ регуляризации",  fontsize=label_name_fontsize,labelpad=pad)
        
        cbar = plt.colorbar()
        cbar.ax.tick_params(labelsize=30)
        #plt.yticks(range(240,690,50),fontsize=20)
        # ax = plt.gca()  # Получаем текущие оси
        fig_ax_1.yaxis.set_major_locator(MultipleLocator(2))
        #fig_ax_1.xaxis.set_major_locator(MultipleLocator(1))

        fig_ax_1.set_yticklabels(fig_ax_1.get_yticklabels(), fontsize=label_y_number_size)

        x_lab=[]
        for i in fig_ax_1.get_xticklabels():
            x_lab.append(f'$10^{{{i.get_text()}}}$')
        fig_ax_1.set_xticklabels(x_lab, fontsize=label_x_number_size)
        fig_ax_1.tick_params('x',pad=20)
        fig_ax_1.get_xaxis().set_tick_params(direction='in')
        fig_ax_1.get_yaxis().set_tick_params(direction='in')
        #plt.xticks(indexx,lower,fontsize=20)
        if save:
            dir_name=self.make_dir_name(name_dataset=data_set_name)
            Path(dir_name).mkdir(parents=True, exist_ok=True)
            plt.savefig(file_name+'.pdf', format='pdf', dpi=300,bbox_inches='tight')
            plt.savefig(file_name+'.jpg', format='jpg', dpi=300,bbox_inches='tight')
            plt.savefig(file_name+'.tif', format='tif', dpi=300,bbox_inches='tight')
            plt.savefig(file_name+'.tiff', format='tiff', dpi=300,bbox_inches='tight')
            plt.savefig(file_name+".svg", format="svg",bbox_inches='tight')

        plt.show();
