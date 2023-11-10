import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import matplotlib as mpl
from dataset_model import Dataset_model as dm
# from dataset_model import Cross_validation_dataset_model as cvdm
from dataset_model import Centering_dataset_model as cdm
from pathlib import Path

class Draw_simple_spectrum:
    def __init__(self,data:dm|cdm,number_of_spectrum_for_draw:int,number_column_for_concentration_for_dm:int=0) -> None:
        self.data=data
        self.number_of_spectrum_for_draw=number_of_spectrum_for_draw
        self.number_column_for_concentration_for_dm=number_column_for_concentration_for_dm
        self.t()

    def t(self):
        if dm==type(self.data):
            self.matrix=self.data.Sectrun[self.number_of_spectrum_for_draw,:,:]
            self.substance_name=self.data.Name_of_column_list[self.number_column_for_concentration_for_dm]
        elif cdm==type(self.data):
            self.matrix=self.data.Centering_spectrum[self.number_of_spectrum_for_draw,:,:]
            self.substance_name=self.data.Name_of_column_list
        else:
            raise TypeError('Ты ввёл объект не того типа. Посмотри детали в draw_simple_spectrum.py файле.')
        return self
    
    def make_dir_name(self,name_dataset:str|None)->str:
        if name_dataset==None:
            return 'plots/none/'+self.substance_name
        else:
            return 'plots/'+str(name_dataset)+'/'+self.substance_name


    def make_full_name_file(self,name_dataset:str|None)->str:
        return self.make_dir_name(name_dataset=name_dataset)+'/'+'spectrum_'+str(self.number_of_spectrum_for_draw)

    def main(self,save:bool=False,name_of_dataset:str|None=None,size_img:tuple=(15,11), label_x_number_size:int=30,
             label_y_number_size:int=30,pad:int=15, title_fontsize:int=45,label_name_fontsize:int=40,
             need_of_title_on_plot:bool=False):
        self.plot(save=save,file_name=self.make_full_name_file(name_of_dataset),
                  size_img=size_img,label_x_number_size=label_x_number_size,
                  label_y_number_size=label_y_number_size,pad=pad,
                  title_fontsize=title_fontsize,label_name_fontsize=label_name_fontsize,
                  data_set_name=name_of_dataset, need_of_title_on_plot=need_of_title_on_plot)

    def plot(self,save,file_name:str,size_img:tuple,label_x_number_size:int,label_y_number_size:int,pad:int,
             title_fontsize:int,label_name_fontsize:int,data_set_name:str|None=None,need_of_title_on_plot:bool=False):
        mpl.rc('font',family='Times New Roman')
        fg = plt.figure(figsize=size_img,constrained_layout=False)
        gs = gridspec.GridSpec(ncols=1, nrows=1, figure=fg)
        #plt.title("Центрирование спектра образца 5",  {'fontname':'Times New Roman'}, fontsize=28,loc="center" ,pad=45)

        plt.subplots_adjust(wspace=0, hspace=0)

        fig_ax_1 = fg.add_subplot(gs[0])
        #plt.imshow(on+tw+th+fo+trtrt,aspect="auto", origin='lower')
        plt.imshow(self.matrix,aspect="auto", origin='lower',extent=[self.data.Exitation_wale[0],
                                                                     self.data.Exitation_wale[-1],
                                                                     self.data.Emission_wale[0],
                                                                     self.data.Emission_wale[-1]])
        plt.ylabel("Emission" , fontsize=label_name_fontsize,labelpad=pad)
        plt.xlabel("Excitation",  fontsize=label_name_fontsize,labelpad=pad)
        if need_of_title_on_plot:
            if data_set_name==None:
                title="EEM "+self.substance_name
            else:
                title="EEM "+self.substance_name+" fluorophore "+data_set_name
            plt.title(title, fontsize=title_fontsize,loc="center" ,pad=pad)
        cbar = plt.colorbar()
        cbar.ax.tick_params(labelsize=30)
        #plt.yticks(range(240,690,50),fontsize=20)
        fig_ax_1.set_yticklabels(fig_ax_1.get_yticklabels(), fontsize=label_y_number_size)
        fig_ax_1.set_xticklabels(fig_ax_1.get_xticklabels(), fontsize=label_x_number_size)
        fig_ax_1.get_xaxis().set_tick_params(direction='in')
        fig_ax_1.get_yaxis().set_tick_params(direction='in')
        #plt.xticks(indexx,lower,fontsize=20)
        if save:
            dir_name=self.make_dir_name(name_dataset=data_set_name)
            Path(dir_name).mkdir(parents=True, exist_ok=True)
            plt.savefig(file_name+'.pdf', format='pdf', dpi=300,bbox_inches='tight')
            plt.savefig(file_name+'.jpg', format='jpg', dpi=300,bbox_inches='tight')
            plt.savefig(file_name+".svg", format="svg",bbox_inches='tight')

        plt.show();
