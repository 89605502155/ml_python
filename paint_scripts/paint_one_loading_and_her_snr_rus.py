import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib as mpl

class Plot_one_loading_and_her_snr_rus:
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


    def painter(self, snr_bad,snr_good,loading_bad:np.ndarray,wave_lenghts_bad:np.ndarray,
                loading_good:np.ndarray,wave_lenghts_good:np.ndarray,save:bool=False):
        mpl.rc('font',family='Times New Roman')
        self.fig = plt.figure(figsize=(12, 8),constrained_layout=True)
        ax = self.fig.add_subplot()
        ax.plot(wave_lenghts_good,loading_good,color='green',lw=5,label='SNR='+str(round(snr_good['evklid'][0],2)))
        ax.plot(wave_lenghts_bad,loading_bad,color='#800080',lw=5,label='SNR='+str(round(snr_bad['evklid'][0],2)))
        plt.legend(labelcolor='linecolor',fontsize=self.ax_label_number_font)
        ax.grid(color="black", drawstyle="default", linewidth=0.7)

        pad=15
        # plt.ylabel("Регистрация, нм" , fontsize=self.ax_name_label_fontsize,labelpad=pad)
        plt.xlabel("Длина волны, нм",  fontsize=self.ax_name_label_fontsize,labelpad=pad)
        ax.set_xticklabels(ax.get_xticklabels(), fontsize=self.ax_label_number_font)
        ax.set_yticklabels(ax.get_yticklabels(), fontsize=self.ax_label_number_font)
        # ax.text(wave_lenghts[0],1.2*max(loading),str(snr), fontsize=self.text_size_in_box,fontweight='bold',
        #       bbox=dict(boxstyle="round",fc='white',ec='black'))
        if save:

            dir_name='plots/ru_load/snr'
            file_name='signal_noise_example'
            Path(dir_name).mkdir(parents=True, exist_ok=True)
            plt.savefig(file_name+'.pdf', format='pdf', dpi=300,bbox_inches='tight')
            plt.savefig(file_name+'.jpg', format='jpg', dpi=300,bbox_inches='tight')
            plt.savefig(file_name+'.tif', format='tif', dpi=300,bbox_inches='tight')
            plt.savefig(file_name+'.tiff', format='tiff', dpi=300,bbox_inches='tight')
            plt.savefig(file_name+".svg", format="svg",bbox_inches='tight')
        plt.show()