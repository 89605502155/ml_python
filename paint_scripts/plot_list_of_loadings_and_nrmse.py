import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib as mpl

class Plot_list_of_loadings_and_nrmse:
    def __init__(self,ax_name_label_fontsize:int=42,
                 title_label_name_fontsize:int=45, text_size_in_box:int=42,
                 ax_label_number_font:int=40, number_of_components_of_first_step:int=4,
                 x_label_control:bool=False) -> None:
        self.col=2
        self.row=4
        self.ax_name_label_fontsize=ax_name_label_fontsize
        self.title_label_name_fontsize=title_label_name_fontsize
        self.text_size_in_box=text_size_in_box
        self.ax_label_number_font=ax_label_number_font
        self.number_of_components_of_first_step=number_of_components_of_first_step
        self.x_label_control=x_label_control

    def create_save_name(self,data_set_name:str,fluorophore_name:str,save:bool=False):
        dir_name='plots/syn_rmse_loadings/'+data_set_name+fluorophore_name
        if save:
            Path(dir_name).mkdir(parents=True, exist_ok=True)
        return dir_name+'/'+fluorophore_name
    
    def generate_string_from_number_of_component(self,num)->str:
        match num:
            case 1: return "1-st"
            case 2: return "2-nd"
            case 3: return "3-rd"
            case 4: return "4-th"
            case 5: return "5-th"
            case 6: return "6-th"
            case 7: return "7-th"
            case 8: return "8-th"
            case 9: return "9-th"
            case 10: return "10-th"
    
    def paint_loadings(self,row,col,loadings:np.ndarray,wave_lenth:np.ndarray,
                       x_name:str,number_comp_from_we_start:int=0):
        self.ax = self.fig.add_subplot(self.spec[row, col])
        print(loadings.shape)
        for i in range(loadings.shape[0]):
            self.ax.plot(wave_lenth,loadings[i,:],lw=4,label=
                         self.generate_string_from_number_of_component(number_comp_from_we_start+i+1))
        
        # self.ax.set_xticks(range(1,n_comp[-1]+1))
        self.ax.locator_params(axis='x', nbins=6)
        if self.x_label_control:
            self.ax.locator_params(axis='x', nbins=6)
    
        self.ax.grid(color="black", drawstyle="default", linewidth=0.7)
        self.ax.set_xlabel(x_name,  fontsize=self.ax_name_label_fontsize,
                    labelpad=15)
        self.ax.tick_params(which='major', length=10, width=2)
        self.ax.set_xticklabels(self.ax.get_xticklabels(), fontsize=self.ax_label_number_font)
        self.ax.set_yticklabels(self.ax.get_yticklabels(), fontsize=self.ax_label_number_font)
        self.ax.tick_params(axis='x', pad=15)
        self.ax.legend(fontsize=30)
        self.ax.get_xaxis().set_tick_params(direction='in')
        self.ax.get_yaxis().set_tick_params(direction='in')

    def paint_n_comp(self,row,col,rmse_ncomp:np.ndarray,n_comp:np.ndarray):
        self.ax = self.fig.add_subplot(self.spec[row, col])
        self.ax.plot(n_comp,rmse_ncomp,'.',color='red',ms=20)
        
        self.ax.set_xticks(range(n_comp[0],n_comp[-1]+1))
        self.ax.set_yscale("log")
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
    
    def painter(self,w_i:np.ndarray,w_k:np.ndarray,nrmse:np.ndarray,
                emission_wave_lenth:np.ndarray,excitation_wave_lenth:np.ndarray,
                save_file_name:str,save:bool=False):
        mpl.rc('font',family='Times New Roman')
        self.fig = plt.figure(figsize=(9*self.col, 9.5*self.row),constrained_layout=True)
        self.spec = self.fig.add_gridspec(ncols=self.col, nrows=self.row)
        #plt.subplots_adjust(wspace=0.3, hspace=0.3)
        number=0
        for row in range(self.row):
            for col in range(self.col):
                if number==0:
                    print(w_i.shape)
                    self.paint_loadings(row=row,col=col,loadings=w_i[:self.number_of_components_of_first_step,:],
                                        number_comp_from_we_start=0,
                                        wave_lenth=excitation_wave_lenth,x_name="Excitation")
                elif number==1:
                    self.paint_loadings(row=row,col=col,loadings=w_k[:self.number_of_components_of_first_step,:],
                                        number_comp_from_we_start=0,
                                        wave_lenth=emission_wave_lenth,x_name="Emission")
                elif number==2:
                    self.paint_loadings(row=row,col=col,loadings=w_i[self.number_of_components_of_first_step:,:],
                                        number_comp_from_we_start=self.number_of_components_of_first_step,
                                        wave_lenth=excitation_wave_lenth,x_name="Excitation")
                elif number==3:
                    self.paint_loadings(row=row,col=col,loadings=w_k[self.number_of_components_of_first_step:,:],
                                        number_comp_from_we_start=self.number_of_components_of_first_step,
                                        wave_lenth=emission_wave_lenth,x_name="Emission")
                elif number==4:
                    list_of_n_comp=[i for i in range(1,self.number_of_components_of_first_step+1)]
                    self.paint_n_comp(row=row,col=col,rmse_ncomp=nrmse[:self.number_of_components_of_first_step],
                                      n_comp=np.array(list_of_n_comp))
                elif number==5:
                    list_of_n_comp=[i for i in range(1,nrmse.shape[0]+1)]
                    self.paint_n_comp(row=row,col=col,rmse_ncomp=nrmse,
                                      n_comp=np.array(list_of_n_comp))
                elif number==6:
                    list_of_n_comp=[i for i in range(self.number_of_components_of_first_step+1,nrmse.shape[0]+1)]
                    self.paint_n_comp(row=row,col=col,rmse_ncomp=nrmse[self.number_of_components_of_first_step:],
                                      n_comp=np.array(list_of_n_comp))
                elif number==7:
                    continue
                number+=1
        plt.tight_layout(h_pad=5,w_pad=5)
        
        if save:
            plt.savefig(save_file_name+'.pdf', format='pdf', dpi=300,bbox_inches='tight')
            plt.savefig(save_file_name+'.jpg', format='jpg', dpi=300,bbox_inches='tight')
            plt.savefig(save_file_name+".svg", format="svg",bbox_inches='tight')

        plt.show()
    
    def main(self,w_i,w_k,nrmse,emission_wave_lenth,excitation_wave_lenth,data_set_name:str='Synthetic',
              fluorophore_name:str="first",save:bool=False):
        save_name=self.create_save_name(data_set_name=data_set_name,fluorophore_name=fluorophore_name,save=save)
        self.painter(w_i=w_i[:,:,0],w_k=w_k[:,:,0],nrmse=nrmse,emission_wave_lenth=emission_wave_lenth,
                     excitation_wave_lenth=excitation_wave_lenth,save_file_name=save_name,
                     save=save)
        
    