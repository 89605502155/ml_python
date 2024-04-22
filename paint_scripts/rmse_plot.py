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

class Rmse_Plot_new:
    def __init__(self,ax_name_label_fontsize:int=42,
                 title_label_name_fontsize:int=45, text_size_in_box:int=42,
                 ax_label_number_font:int=40) -> None:
        self.col=1
        self.row=1
        self.ax_name_label_fontsize=ax_name_label_fontsize
        self.title_label_name_fontsize=title_label_name_fontsize
        self.text_size_in_box=text_size_in_box
        self.ax_label_number_font=ax_label_number_font

    def __create_save_name(self,data_set_name:str,fluorophore_name:str,save:bool=False):
        dir_name='plots5/rmse/v2/'+data_set_name+fluorophore_name
        if save:
            Path(dir_name).mkdir(parents=True, exist_ok=True)
        return dir_name+'/'+fluorophore_name



    def paint_n_comp(self,l21,l22,snr,rmse_l2_snr:np.ndarray, rmse_l2:np.ndarray,
                     n_comp:np.ndarray,log_scale:bool,legend_outside:bool):
        row=0
        col=0
        self.ax = self.fig.add_subplot(self.spec[row, col])
        self.ax.plot(n_comp,rmse_l2,'*',color='green',ms=20,label='lg($L_{2}$)='+f'{l21}')
        # self.ax.plot([n_comp[i] for i in range(rmse_l2.shape[0])],rmse_l2,'*',color='green',ms=20,label='lg($L_{2}$)='+f'{l2}')
        # self.ax.plot([n_comp[i] for i in range(rmse_snr.shape[0])],rmse_snr,'^',color='blue',ms=20,label='SNR='+f'{snr}')
        self.ax.plot([n_comp[i] for i in range(rmse_l2_snr.shape[0])],rmse_l2_snr,'^',color='#800080',ms=20,label='lg($L_{2}$)='+f'{l22}'+' SNR='+f'{snr}')
        
        # self.ax.set_xticks(range(1,n_comp[-1]+1))
        if log_scale:
            plt.yscale('log')
    
        self.ax.grid(color="black", drawstyle="default", linewidth=0.7)
        self.ax.set_xlabel("Количество компонент",  fontsize=self.ax_name_label_fontsize,
                    labelpad=15)
        self.ax.set_ylabel("$\\frac {RMSE}{ДК}$",  fontsize=self.ax_name_label_fontsize,
                    labelpad=15)
        if legend_outside:
            plt.legend(loc='center left',labelcolor='linecolor',  bbox_to_anchor=(1,0.5),fontsize=self.ax_label_number_font-10)
        else:
            plt.legend(labelcolor='linecolor',fontsize=self.ax_label_number_font-10)
        self.ax.tick_params(which='major', length=10, width=2)
        self.ax.set_xticklabels(self.ax.get_xticklabels(), fontsize=self.ax_label_number_font)
        self.ax.set_yticklabels(self.ax.get_yticklabels(), fontsize=self.ax_label_number_font)
        self.ax.tick_params(axis='x', pad=15)
        self.ax.get_xaxis().set_tick_params(direction='in')
        self.ax.get_yaxis().set_tick_params(direction='in')

    def painter(self, l21,l22,snr,rmse_l2_snr:np.ndarray,rmse_l2:np.ndarray,
                n_comp:np.ndarray,log_scale:bool,legend_outside:bool,
                save_file_name:str,save:bool=False):
        mpl.rc('font',family='Times New Roman')
        self.fig = plt.figure(figsize=(12*self.col, 8*self.row),constrained_layout=True)
        self.spec = self.fig.add_gridspec(ncols=self.col, nrows=self.row)
        #plt.subplots_adjust(wspace=0.3, hspace=0.3)
        self.paint_n_comp(l21=l21,l22=l22,snr=snr,rmse_l2=rmse_l2,
                            rmse_l2_snr=rmse_l2_snr,
                            log_scale=log_scale,legend_outside=legend_outside,n_comp=n_comp)
        plt.tight_layout(h_pad=5,w_pad=5)

        if log_scale:
            save_file_name+='_log'
        if legend_outside:
            save_file_name+='_outside'
        
        if save:
            plt.savefig(save_file_name+'.pdf', format='pdf', dpi=300,bbox_inches='tight')
            plt.savefig(save_file_name+'.jpg', format='jpg', dpi=300,bbox_inches='tight')
            plt.savefig(save_file_name+".svg", format="svg",bbox_inches='tight')

        plt.show()

    def main(self,l21,l22,snr,rmse_l2_snr:np.ndarray,rmse_l2:np.ndarray,
            n_comp:np.ndarray, 
            data_set_name:str,fluorophore_name:str, save:bool=False):
        save_name=self.__create_save_name(data_set_name=data_set_name,fluorophore_name=fluorophore_name,save=save)
        self.painter(l21=l21,l22=l22,snr=snr,rmse_l2=rmse_l2,
                    rmse_l2_snr=rmse_l2_snr,
                    log_scale=False,legend_outside=False,
                    n_comp=n_comp,save=save,save_file_name=save_name)
        self.painter(l21=l21,l22=l22,snr=snr,rmse_l2=rmse_l2,
                    rmse_l2_snr=rmse_l2_snr,
                    log_scale=False,legend_outside=True,
                    n_comp=n_comp,save=save,save_file_name=save_name)
        self.painter(l21=l21,l22=l22,snr=snr,rmse_l2=rmse_l2,
                    rmse_l2_snr=rmse_l2_snr,
                    log_scale=True,legend_outside=False,
                    n_comp=n_comp,save=save,save_file_name=save_name)
        self.painter(l21=l21,l22=l22,snr=snr,rmse_l2=rmse_l2,
                    rmse_l2_snr=rmse_l2_snr,
                    log_scale=True,legend_outside=True,
                    n_comp=n_comp,save=save,save_file_name=save_name)

class Rmse_Plot_pls:
    def __init__(self,ax_name_label_fontsize:int=42,
                 title_label_name_fontsize:int=45, text_size_in_box:int=42,
                 ax_label_number_font:int=40) -> None:
        self.col=1
        self.row=1
        self.ax_name_label_fontsize=ax_name_label_fontsize
        self.title_label_name_fontsize=title_label_name_fontsize
        self.text_size_in_box=text_size_in_box
        self.ax_label_number_font=ax_label_number_font

    def __create_save_name_rmse(self,data_set_name:str,fluorophore_name:str,save:bool=False):
        dir_name='plots_pls/rmse/'+data_set_name+fluorophore_name
        if save:
            Path(dir_name).mkdir(parents=True, exist_ok=True)
        return dir_name+'/'+fluorophore_name
    
    def __create_save_name_q2(self,data_set_name:str,fluorophore_name:str,save:bool=False):
        dir_name='plots_pls/q2/'+data_set_name+fluorophore_name
        if save:
            Path(dir_name).mkdir(parents=True, exist_ok=True)
        return dir_name+'/'+fluorophore_name



    def paint_n_comp_rmse(self,rmse:np.ndarray,
                     n_comp:np.ndarray,log_scale:bool):
        row=0
        col=0
        self.ax = self.fig.add_subplot(self.spec[row, col])
        self.ax.plot(n_comp,rmse,'.',color='red',ms=20)
        # self.ax.plot([n_comp[i] for i in range(rmse_l2.shape[0])],rmse_l2,'*',color='green',ms=20,label='lg($L_{2}$)='+f'{l2}')
        # self.ax.plot([n_comp[i] for i in range(rmse_snr.shape[0])],rmse_snr,'^',color='blue',ms=20,label='SNR='+f'{snr}')
        # self.ax.plot([n_comp[i] for i in range(rmse_l2_snr.shape[0])],rmse_l2_snr,'^',color='#800080',ms=20,label='lg($L_{2}$)='+f'{l22}'+' SNR='+f'{snr}')
        
        # self.ax.set_xticks(range(1,n_comp[-1]+1))
        if log_scale:
            plt.yscale('log')
    
        self.ax.grid(color="black", drawstyle="default", linewidth=0.7)
        self.ax.set_xlabel("Количество компонент",  fontsize=self.ax_name_label_fontsize,
                    labelpad=15)
        self.ax.set_ylabel("$\\frac {RMSE}{ДК}$",  fontsize=self.ax_name_label_fontsize,
                    labelpad=15)
        # if legend_outside:
        #     plt.legend(loc='center left',labelcolor='linecolor',  bbox_to_anchor=(1,0.5),fontsize=self.ax_label_number_font-10)
        # else:
        #     plt.legend(labelcolor='linecolor',fontsize=self.ax_label_number_font-10)
        self.ax.tick_params(which='major', length=10, width=2)
        self.ax.set_xticklabels(self.ax.get_xticklabels(), fontsize=self.ax_label_number_font)
        self.ax.set_yticklabels(self.ax.get_yticklabels(), fontsize=self.ax_label_number_font)
        self.ax.tick_params(axis='x', pad=15)
        self.ax.get_xaxis().set_tick_params(direction='in')
        self.ax.get_yaxis().set_tick_params(direction='in')

    def paint_n_comp_q2(self,q2:np.ndarray,
                     n_comp:np.ndarray):
        row=0
        col=0
        self.ax = self.fig.add_subplot(self.spec[row, col])
        self.ax.plot(n_comp,q2,'.',color='red',ms=20)
        # self.ax.plot([n_comp[i] for i in range(rmse_l2.shape[0])],rmse_l2,'*',color='green',ms=20,label='lg($L_{2}$)='+f'{l2}')
        # self.ax.plot([n_comp[i] for i in range(rmse_snr.shape[0])],rmse_snr,'^',color='blue',ms=20,label='SNR='+f'{snr}')
        # self.ax.plot([n_comp[i] for i in range(rmse_l2_snr.shape[0])],rmse_l2_snr,'^',color='#800080',ms=20,label='lg($L_{2}$)='+f'{l22}'+' SNR='+f'{snr}')
        
        # self.ax.set_xticks(range(1,n_comp[-1]+1))
        
    
        self.ax.grid(color="black", drawstyle="default", linewidth=0.7)
        self.ax.set_xlabel("Количество компонент",  fontsize=self.ax_name_label_fontsize,
                    labelpad=15)
        self.ax.set_ylabel("$Q^{2}$",  fontsize=self.ax_name_label_fontsize,
                    labelpad=15)
        # if legend_outside:
        #     plt.legend(loc='center left',labelcolor='linecolor',  bbox_to_anchor=(1,0.5),fontsize=self.ax_label_number_font-10)
        # else:
        #     plt.legend(labelcolor='linecolor',fontsize=self.ax_label_number_font-10)
        self.ax.tick_params(which='major', length=10, width=2)
        self.ax.set_xticklabels(self.ax.get_xticklabels(), fontsize=self.ax_label_number_font)
        self.ax.set_yticklabels(self.ax.get_yticklabels(), fontsize=self.ax_label_number_font)
        self.ax.tick_params(axis='x', pad=15)
        self.ax.get_xaxis().set_tick_params(direction='in')
        self.ax.get_yaxis().set_tick_params(direction='in')

    def painter_rmse(self, rmse:np.ndarray,
                n_comp:np.ndarray,log_scale:bool,
                save_file_name:str,save:bool=False):
        mpl.rc('font',family='Times New Roman')
        self.fig = plt.figure(figsize=(12*self.col, 8*self.row),constrained_layout=True)
        self.spec = self.fig.add_gridspec(ncols=self.col, nrows=self.row)
        #plt.subplots_adjust(wspace=0.3, hspace=0.3)
        self.paint_n_comp_rmse(rmse=rmse,
                            log_scale=log_scale,n_comp=n_comp)
        plt.tight_layout(h_pad=5,w_pad=5)

        if log_scale:
            save_file_name+='_log'
       
        if save:
            plt.savefig(save_file_name+'.pdf', format='pdf', dpi=300,bbox_inches='tight')
            plt.savefig(save_file_name+'.jpg', format='jpg', dpi=300,bbox_inches='tight')
            plt.savefig(save_file_name+".svg", format="svg",bbox_inches='tight')

        plt.show()

    def painter_q2(self, q2:np.ndarray,
                n_comp:np.ndarray,
                save_file_name:str,save:bool=False):
        mpl.rc('font',family='Times New Roman')
        self.fig = plt.figure(figsize=(12*self.col, 8*self.row),constrained_layout=True)
        self.spec = self.fig.add_gridspec(ncols=self.col, nrows=self.row)
        #plt.subplots_adjust(wspace=0.3, hspace=0.3)
        self.paint_n_comp_q2(q2=q2,n_comp=n_comp)
        plt.tight_layout(h_pad=5,w_pad=5)
       
        if save:
            plt.savefig(save_file_name+'.pdf', format='pdf', dpi=300,bbox_inches='tight')
            plt.savefig(save_file_name+'.jpg', format='jpg', dpi=300,bbox_inches='tight')
            plt.savefig(save_file_name+".svg", format="svg",bbox_inches='tight')

        plt.show()

    def main(self,rmse:np.ndarray,
            n_comp:np.ndarray, q2:np.ndarray,
            data_set_name:str,fluorophore_name:str, save:bool=False):
        save_name_rmse=self.__create_save_name_rmse(data_set_name=data_set_name,
                                                    fluorophore_name=fluorophore_name,save=save)
        save_name_q2=self.__create_save_name_q2(data_set_name=data_set_name,
                                                    fluorophore_name=fluorophore_name,save=save)
        self.painter_rmse(rmse=rmse,
                    log_scale=False,
                    n_comp=n_comp,save=save,save_file_name=save_name_rmse)
        self.painter_rmse( rmse=rmse,
                    log_scale=True,
                    n_comp=n_comp,save=save,save_file_name=save_name_rmse)
        self.painter_q2(q2=q2,n_comp=n_comp,save=save,save_file_name=save_name_q2)
        



