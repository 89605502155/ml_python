from dataset_model import Dataset_model_with_theoretical_loadings_only_for_synthetic as dm
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib as mpl

class paint_theoretical_loadings_for_syn:
    def __init__(self, dataset_model:dm):
        self.dataset_model = dataset_model

    def __generate_string_from_number_of_component(self,num)->str:
        match num:
            case 1: return "1-ая"
            case 2: return "2-ая"
            case 3: return "3-я"
            case 4: return "4-ая"

    def __directory_maker(self):
        return 'plots14'
    
    def __paint_loadings(self,loading,wave_lenghts,name,col):
        self.ax = self.fig.add_subplot(self.spec[0, col])
        colors=['#445cce','#84fe4f','#f7c03a','#790403']
        lab=[self.__generate_string_from_number_of_component(i) for i in range(1,5)]
        for i in range(4):
            self.ax.plot(wave_lenghts,loading[:,i],label=lab[i],color=colors[i],lw=3)
        # self.ax.plot(d['Em'],d['B0'][:,0],"-",lw=3,label="1-st",color='#445cce')
        # self.ax.plot(d['Em'],d['B0'][:,1],"-",lw=3,label="2-nd",color='#84fe4f')
        # self.ax.plot(d['Em'],d['B0'][:,2],"-",lw=3,label="3-rd",color='#f7c03a')
        # self.ax.plot(d['Em'],d['B0'][:,3],"-",lw=3,label="4-th",color='#790403')
        self.ax.grid(color="black", drawstyle="default", linewidth=0.7)
        self.ax.set_xlabel("длины волны \n"+name+", нм",  {'fontname':'Times New Roman'},  fontsize=35,labelpad=15,loc="center")
        self.ax.set_title("нагрузки "+name,  {'fontname':'Times New Roman'}, fontsize=40,loc="center" ,pad=15)
        self.ax.tick_params(which='major', length=10, width=2)
        self.ax.legend(loc='best',fontsize=25)

        # self.ax.set_yticks([0.005*i for i in range(5)])
        self.ax.locator_params(nbins=6,axis='y')
        self.ax.locator_params(nbins=5,axis='x')

        self.ax.get_xaxis().set_tick_params(direction='in')
        self.ax.get_yaxis().set_tick_params(direction='in')
        self.ax.set_xticklabels(self.ax.get_xticklabels(),fontsize=30)
        self.ax.set_yticklabels(self.ax.get_yticklabels(),fontsize=30)

    def __painter(self,zaz:float=1.0,direct:str='ff', save:bool=False):
        mpl.rc('font',family='Times New Roman')
        self.fig = plt.figure(figsize=(12, 8),constrained_layout=True)
        self.spec = self.fig.add_gridspec(ncols=2, nrows=1)
        for i in range(2):
            if i==0:
                self.__paint_loadings(loading=self.dataset_model.emission_theoretical_loadings,
                                        wave_lenghts=self.dataset_model.Emission_wale,
                                        name="регистрации",col=i)
            elif i==1:
                self.__paint_loadings(loading=self.dataset_model.excitation_theoretical_loadings,
                                        wave_lenghts=self.dataset_model.Exitation_wale,
                                        name="возбуждения",col=i)
        plt.tight_layout(w_pad=zaz)
        if save:
            Path(direct).mkdir(parents=True, exist_ok=True)
            plt.savefig(direct+'.pdf', format='pdf', dpi=300,bbox_inches='tight')
            plt.savefig(direct+'.jpg', format='jpg', dpi=300,bbox_inches='tight')
            plt.savefig(direct+'.tif', format='tif', dpi=300,bbox_inches='tight')
            plt.savefig(direct+'.tiff', format='tiff', dpi=300,bbox_inches='tight')
            plt.savefig(direct+".svg", format="svg",bbox_inches='tight')

        plt.show();

               

    def paint(self,zaz,save:bool=False):
        direct=self.__directory_maker()
        self.__painter(direct=direct, save=save,zaz=zaz) 
        