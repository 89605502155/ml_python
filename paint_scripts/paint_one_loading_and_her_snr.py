import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib as mpl

class Plot_one_loading_and_her_snr:
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


    def painter(self, snr,loading:np.ndarray,wave_lenghts:np.ndarray):
        mpl.rc('font',family='Times New Roman')
        self.fig = plt.figure(figsize=(9, 9.5),constrained_layout=True)
        ax = self.fig.add_subplot()
        ax.plot(wave_lenghts,loading,color='green',lw=5,label=str(snr))
        ax.grid(color="black", drawstyle="default", linewidth=0.7)
        ax.set_xticklabels(ax.get_xticklabels(), fontsize=self.ax_label_number_font)
        ax.set_yticklabels(ax.get_yticklabels(), fontsize=self.ax_label_number_font)
        ax.text(wave_lenghts[0],1.2*max(loading),str(snr), fontsize=self.text_size_in_box,fontweight='bold',
              bbox=dict(boxstyle="round",fc='white',ec='black'))
        plt.show()