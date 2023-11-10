import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib as mpl

class Rmse_Plot:
    def __init__(self,ax_name_label_fontsize:int=42,
                 title_label_name_fontsize:int=45, text_size_in_box:int=42,
                 ax_label_number_font:int=40) -> None:
        self.col=2
        self.row=1
        self.ax_name_label_fontsize=ax_name_label_fontsize
        self.title_label_name_fontsize=title_label_name_fontsize
        self.text_size_in_box=text_size_in_box
        self.ax_label_number_font=ax_label_number_font

    def create_save_name(self,data_set_name:str,fluorophore_name:str,save:bool=False):
        dir_name='plots/rmse/v2/'+data_set_name+fluorophore_name
        if save:
            Path(dir_name).mkdir(parents=True, exist_ok=True)
        return dir_name+'/'+fluorophore_name

    def paint_l2(self,row,col,rmse_l2:np.ndarray,l2:np.ndarray):
        self.ax = self.fig.add_subplot(self.spec[row, col])
        self.ax.plot(l2,rmse_l2,'.',color='red',ms=20)
        self.ax.set_xscale("log")
        self.ax.set_yscale("log")
        self.ax.grid(color="black", drawstyle="default", linewidth=0.7)
        self.ax.set_xlabel("L2-coefficient",  fontsize=self.ax_name_label_fontsize,
                    labelpad=15)
        self.ax.set_ylabel("$\\frac {RMSE}{concentration\ range}$",  fontsize=self.ax_name_label_fontsize,
                    labelpad=15)
        self.ax.tick_params(which='major', length=10, width=2)
        self.ax.set_xticklabels(self.ax.get_xticklabels(), fontsize=self.ax_label_number_font)
        self.ax.set_yticklabels(self.ax.get_yticklabels(), fontsize=self.ax_label_number_font)
        self.ax.tick_params(axis='x', pad=15)
        self.ax.get_xaxis().set_tick_params(direction='in')
        self.ax.get_yaxis().set_tick_params(direction='in')

    def paint_n_comp(self,row,col,rmse_ncomp:np.ndarray,n_comp:np.ndarray):
        self.ax = self.fig.add_subplot(self.spec[row, col])
        self.ax.plot(n_comp,rmse_ncomp,'.',color='red',ms=20)
        
        self.ax.set_xticks(range(1,n_comp[-1]+1))
    
        self.ax.grid(color="black", drawstyle="default", linewidth=0.7)
        self.ax.set_xlabel("Number of components",  fontsize=self.ax_name_label_fontsize,
                    labelpad=15)
        self.ax.set_ylabel("$\\frac {RMSE}{concentration\ range}$",  fontsize=self.ax_name_label_fontsize,
                    labelpad=15)
        self.ax.tick_params(which='major', length=10, width=2)
        self.ax.set_xticklabels(self.ax.get_xticklabels(), fontsize=self.ax_label_number_font)
        self.ax.set_yticklabels(self.ax.get_yticklabels(), fontsize=self.ax_label_number_font)
        self.ax.tick_params(axis='x', pad=15)
        self.ax.get_xaxis().set_tick_params(direction='in')
        self.ax.get_yaxis().set_tick_params(direction='in')

    def painter(self,rmse_l2:np.ndarray,l2:np.ndarray,rmse_ncomp:np.ndarray,n_comp:np.ndarray,
                 save_file_name:str,fluorophore_name:str,save:bool=False):
        mpl.rc('font',family='Times New Roman')
        self.fig = plt.figure(figsize=(9*self.col, 9.5*self.row),constrained_layout=True)
        self.spec = self.fig.add_gridspec(ncols=self.col, nrows=self.row)
        #plt.subplots_adjust(wspace=0.3, hspace=0.3)
        number=0
        for row in range(self.row):
            for col in range(self.col):
                if number==0:
                    self.paint_l2(row=row,col=col,rmse_l2=rmse_l2,l2=l2)
                # self.paint_block(row,col,[1,2,3],[3,2,3],0.0123,'String')
                elif number==1:
                    self.paint_n_comp(row=row,col=col,rmse_ncomp=rmse_ncomp,
                                      n_comp=n_comp)
                number+=1
        plt.tight_layout(h_pad=5,w_pad=5)
        
        if save:
            plt.savefig(save_file_name+'.pdf', format='pdf', dpi=300,bbox_inches='tight')
            plt.savefig(save_file_name+'.jpg', format='jpg', dpi=300,bbox_inches='tight')
            plt.savefig(save_file_name+".svg", format="svg",bbox_inches='tight')

        plt.show()

    def main(self,rmse_l2:np.ndarray,l2:np.ndarray,rmse_ncomp:np.ndarray,n_comp:np.ndarray, 
             data_set_name:str,fluorophore_name:str, save:bool=False):
        save_name=self.create_save_name(data_set_name=data_set_name,fluorophore_name=fluorophore_name,save=save)
        self.painter(rmse_l2=rmse_l2,l2=l2,rmse_ncomp=rmse_ncomp,n_comp=n_comp,
                     save_file_name=save_name,fluorophore_name=fluorophore_name,save=save)
