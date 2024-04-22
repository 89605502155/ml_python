import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib as mpl

class Plot_b_koefs_and_her_l2_rus:
    def __init__(self,ax_name_label_fontsize:int=42,
                 title_label_name_fontsize:int=45, text_size_in_box:int=42,
                 ax_label_number_font:int=40, number_of_components_of_first_step:int=4,
                 x_label_control:bool=False) -> None:
        self.ax_name_label_fontsize=ax_name_label_fontsize
        self.title_label_name_fontsize=title_label_name_fontsize
        self.text_size_in_box=text_size_in_box
        self.ax_label_number_font=ax_label_number_font
        self.number_of_components_of_first_step=number_of_components_of_first_step
        self.x_label_control=x_label_control


    def painter(self, l2,loading_bad:np.ndarray,
                loading_good:np.ndarray,save:bool=False):
        mpl.rc('font',family='Times New Roman')
        self.fig = plt.figure(figsize=(12, 8),constrained_layout=True)
        ax = self.fig.add_subplot()
        ax.plot(loading_good,color='green',lw=5,label='L$_{2}$='+str(l2))
        ax.plot(loading_bad,color='#800080',lw=5,label='Без регуляризации')
        # plt.yscale('log')
        plt.legend(labelcolor='linecolor',fontsize=self.ax_label_number_font)
        ax.grid(color="black", drawstyle="default", linewidth=0.7)

        pad=15
        # plt.ylabel("Регистрация, нм" , fontsize=self.ax_name_label_fontsize,labelpad=pad)
        # plt.xlabel("Длина волны, нм",  fontsize=self.ax_name_label_fontsize,labelpad=pad)
        y_lab=[f'{int(i.get_position()[1]/1e11)} $\cdot 10^{{11}}$' for i in ax.get_yticklabels()]
        ax.set_xticklabels(ax.get_xticklabels(), fontsize=self.ax_label_number_font)
        ax.set_yticklabels(y_lab, fontsize=self.ax_label_number_font)
        # ax.text(wave_lenghts[0],1.2*max(loading),str(snr), fontsize=self.text_size_in_box,fontweight='bold',
        #       bbox=dict(boxstyle="round",fc='white',ec='black'))
        if save:

            dir_name='plots/ru_bkoefs/l2'
            file_name=dir_name+'/reg_example'
            Path(dir_name).mkdir(parents=True, exist_ok=True)
            plt.savefig(file_name+'.pdf', format='pdf', dpi=300,bbox_inches='tight')
            plt.savefig(file_name+'.jpg', format='jpg', dpi=300,bbox_inches='tight')
            plt.savefig(file_name+'.tif', format='tif', dpi=300,bbox_inches='tight')
            plt.savefig(file_name+'.tiff', format='tiff', dpi=300,bbox_inches='tight')
            plt.savefig(file_name+".svg", format="svg",bbox_inches='tight')
        plt.show()

class Plot_b_koefs_and_her_l2_log_rus:
    def __init__(self,ax_name_label_fontsize:int=42,
                 title_label_name_fontsize:int=45, text_size_in_box:int=42,
                 ax_label_number_font:int=40, number_of_components_of_first_step:int=4,
                 x_label_control:bool=False) -> None:
        self.ax_name_label_fontsize=ax_name_label_fontsize
        self.title_label_name_fontsize=title_label_name_fontsize
        self.text_size_in_box=text_size_in_box
        self.ax_label_number_font=ax_label_number_font
        self.number_of_components_of_first_step=number_of_components_of_first_step
        self.x_label_control=x_label_control


    def painter(self, l2,loading_bad:np.ndarray,
                loading_good:np.ndarray,save:bool=False):
        mpl.rc('font',family='Times New Roman')
        self.fig = plt.figure(figsize=(12, 8),constrained_layout=True)
        ax = self.fig.add_subplot()
        ax.plot(loading_good,color='green',lw=5,label='L$_{2}$='+str(l2))
        ax.plot(loading_bad,color='#800080',lw=5,label='Без регуляризации')
        # plt.yscale('log')
        plt.legend(labelcolor='linecolor',fontsize=self.ax_label_number_font)
        ax.grid(color="black", drawstyle="default", linewidth=0.7)

        pad=15
        # plt.ylabel("Регистрация, нм" , fontsize=self.ax_name_label_fontsize,labelpad=pad)
        # plt.xlabel("Длина волны, нм",  fontsize=self.ax_name_label_fontsize,labelpad=pad)
        # y_lab=[f'{int(i.get_position()[1]/1e11)} $\cdot 10^{{11}}$' for i in ax.get_yticklabels()]
        ax.set_xticklabels(ax.get_xticklabels(), fontsize=self.ax_label_number_font)
        ax.set_yticklabels(ax.get_xticklabels(), fontsize=self.ax_label_number_font)
        plt.ylabel("$lg(|b_{koefs}|)$" , fontsize=40,labelpad=pad)
        # ax.text(wave_lenghts[0],1.2*max(loading),str(snr), fontsize=self.text_size_in_box,fontweight='bold',
        #       bbox=dict(boxstyle="round",fc='white',ec='black'))
        if save:

            dir_name='plots/ru_bkoefs_log/l2'
            file_name=dir_name+'/reg_example'
            Path(dir_name).mkdir(parents=True, exist_ok=True)
            plt.savefig(file_name+'.pdf', format='pdf', dpi=300,bbox_inches='tight')
            plt.savefig(file_name+'.jpg', format='jpg', dpi=300,bbox_inches='tight')
            plt.savefig(file_name+'.tif', format='tif', dpi=300,bbox_inches='tight')
            plt.savefig(file_name+'.tiff', format='tiff', dpi=300,bbox_inches='tight')
            plt.savefig(file_name+".svg", format="svg",bbox_inches='tight')
        plt.show()

