import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib as mpl

class Theory_practice_loadings:
    def __init__(self,practice_excitation_loadings:np.ndarray, theory_excitation_loadings: np.ndarray,
             excitation_wave_lenth: np.ndarray,  practice_emission_loadings:np.ndarray, 
             theory_emission_loadings: np.ndarray, emission_wave_lenth: np.ndarray,
             ax_name_label_fontsize:int=42,
            title_label_name_fontsize:int=45, text_size_in_box:int=42,
            ax_label_number_font:int=40,x_label_control:bool=False):
        self.practice_excitation_loadings=practice_excitation_loadings
        self.theory_excitation_loadings= theory_excitation_loadings
        self.excitation_wave_lenth=excitation_wave_lenth
        self.practice_emission_loadings=  practice_emission_loadings
        self.theory_emission_loadings= theory_emission_loadings
        self.emission_wave_lenth= emission_wave_lenth
        self.col=2
        self.row=1
        self.ax_name_label_fontsize=ax_name_label_fontsize
        self.title_label_name_fontsize=title_label_name_fontsize
        self.text_size_in_box=text_size_in_box
        self.ax_label_number_font=ax_label_number_font
        self.x_label_control=x_label_control


    def create_save_name(self,data_set_name:str,fluorophore_name:str,save:bool=False):
        dir_name='plots21_may/loadings2/'+data_set_name+'/'+fluorophore_name
        if save:
            Path(dir_name).mkdir(parents=True, exist_ok=True)
        return dir_name+'/'+fluorophore_name
    
    def simpl_derivation(self,array,i,lenth:int=4):
        if lenth==4:
            return array[i-2]-8*array[i-1]+8*array[i+1]-array[i+2]
        elif lenth==2:
            return array[i+1]-array[i-1]
    
    def derivation(self,theory:np.ndarray, practise:np.ndarray):
        theory_derivation=list()
        theory_for_line=list()
        practise_for_line=list()
        theory_=theory
        practise_=practise*(max(theory)/max(practise))
        for i in range(2,theory.shape[0]-2):
            theory_derivation.append(self.simpl_derivation(theory_,i,2))
        # print(theory_derivation)
        theory_for_line=list(theory[0:2])
        practise_for_line=list(practise[0:2])
        for i in range(2,practise.shape[0]-2):
            practice_derivative=self.simpl_derivation(practise_,i,2)
            # print(practice_derivative,end=", ")
            # print(practice_derivative)
            if practice_derivative<=theory_derivation[i-2]*1.2+0.15 and practice_derivative>=theory_derivation[i-2]*0.85-0.15 and practise_[i]>=practise_[-1]*0.85:
                theory_for_line.append(theory[i])
                practise_for_line.append(practise[i])
                print(i,end=", ")
            elif practice_derivative>=theory_derivation[i-2]*1.2-0.15 and practice_derivative<=theory_derivation[i-2]*0.85+0.15 and practise_[i]>=practise_[-1]*0.85:
                theory_for_line.append(theory[i])
                practise_for_line.append(practise[i])
                print(i,end=", ")
        print()
        # print(theory_derivation)
        theory_for_line.append(theory[-2])
        practise_for_line.append(practise[-2])

        theory_for_line.append(theory[-1])
        practise_for_line.append(practise[-1])
        return np.array(theory_for_line),np.array(practise_for_line)

    def coeff(self, theory:np.ndarray, practise:np.ndarray):
        if abs(theory.max())<abs(theory.min()):
            theory=theory*(-1)
        m=np.argmax(theory)
        if practise[m]<0:
            practise=practise*(-1)
        theory_,practise_=self.derivation(theory=theory,practise=practise)
        theory_mean:np.float64=theory_.mean()
        practise_mean:np.float64=practise_.mean()
        b1=np.sum((theory_-theory_mean)*(practise_-practise_mean))/np.sum((practise_-practise_mean)**2)
        b0=theory_mean-(b1*practise_mean)
        practise_modification=(practise*b1)+b0

        # err=theory-(b1*practise+b0)
        # -x*(sqrt(y)-sqrt(x*b+k))=0
        # -(sqrt(y)-sqrt(x*b+k))=0
        # y=
        # k1=theory[m]-theory.min()
        # k2=practise[m]-practise.min()
        # k=np.float_(k1/k2)
        # practise = practise*k
        # d1=theory.min()-practise.min()
        # practise=practise+d1
        return theory,practise_modification
    
    def paint(self, col, row, theory,practise,wale_lenth,x_name:str):
        self.ax = self.fig.add_subplot(self.spec[row, col])
        theory,practise=self.coeff(theory,practise)
        self.ax.plot(wale_lenth,theory,'--',color='green',lw=4,label="чистое вещество")
        self.ax.plot(wale_lenth,practise,color='red',lw=4,label="экспериментальные")
        
        # self.ax.set_xticks(range(1,n_comp[-1]+1))
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
    
    def painter(self, save_file_name:str,fluorophore_name:str,save:bool=False):
        mpl.rc('font',family='Times New Roman')
        self.fig = plt.figure(figsize=(9*self.col, 9.5*self.row),constrained_layout=True)
        self.spec = self.fig.add_gridspec(ncols=self.col, nrows=self.row)
        #plt.subplots_adjust(wspace=0.3, hspace=0.3)
        number=0
        for row in range(self.row):
            for col in range(self.col):
                if number==0:
                    self.paint(col=col,row=row,theory=self.theory_emission_loadings,
                               practise=self.practice_emission_loadings,
                               wale_lenth=self.emission_wave_lenth, x_name="длина волны регистрации, нм")
                # self.paint_block(row,col,[1,2,3],[3,2,3],0.0123,'String')
                elif number==1:
                    self.paint(col=col,row=row,theory=self.theory_excitation_loadings,
                               practise=self.practice_excitation_loadings,
                               wale_lenth=self.excitation_wave_lenth, x_name="длина волны возбуждения, нм")
                number+=1
        plt.tight_layout(h_pad=5,w_pad=5)
        
        if save:
            plt.savefig(save_file_name+'.pdf', format='pdf', dpi=300,bbox_inches='tight')
            plt.savefig(save_file_name+'.jpg', format='jpg', dpi=300,bbox_inches='tight')
            plt.savefig(save_file_name+".svg", format="svg",bbox_inches='tight')

        plt.show()

    def main(self,data_set_name:str,fluorophore_name:str, save:bool=False):
        save_name=self.create_save_name(data_set_name=data_set_name,fluorophore_name=fluorophore_name,save=save)
        self.painter(save_file_name=save_name,fluorophore_name=fluorophore_name,save=save)
        
        
        
class May_SNR_loadings:
    def __init__(self,excitation_loadings:np.ndarray, excitation_snr:np.ndarray,
             excitation_wave_lenth: np.ndarray,  emission_loadings:np.ndarray, 
             emission_wave_lenth: np.ndarray, emission_snr:np.ndarray,
             ax_name_label_fontsize:int=42,
            title_label_name_fontsize:int=45, text_size_in_box:int=42,
            ax_label_number_font:int=40,x_label_control:bool=False):
        self.excitation_loadings=excitation_loadings
        self.excitation_wave_lenth=excitation_wave_lenth
        self.emission_loadings=  emission_loadings
        self.emission_wave_lenth= emission_wave_lenth
        self.col=2
        self.row=1
        self.ax_name_label_fontsize=ax_name_label_fontsize
        self.title_label_name_fontsize=title_label_name_fontsize
        self.text_size_in_box=text_size_in_box
        self.ax_label_number_font=ax_label_number_font
        self.x_label_control=x_label_control
        self.excitation_snr=excitation_snr
        self.emission_snr=emission_snr


    def create_save_name(self,data_set_name:str,fluorophore_name:str,save:bool=False):
        dir_name='plots_snr_may_21/loadings2/'+data_set_name+'/'+fluorophore_name
        if save:
            Path(dir_name).mkdir(parents=True, exist_ok=True)
        return dir_name+'/'+fluorophore_name
    

    def generate_string_from_number_of_component(self,num)->str:
        match num:
            case 1: return "1-ая"
            case 2: return "2-ая"
            case 3: return "3-я"
            case 4: return "4-ая"
            case 5: return "5-ая"
            case 6: return "6-ая"
            case 7: return "7-ая"
            case 8: return "8-ая"
            case 9: return "9-ая"
            case 10: return "10-ая"
            
    def paint(self, col, row, loadings,wale_lenth,snr, ancor_a,ancor_b, x_name:str):
        self.ax = self.fig.add_subplot(self.spec[row, col])
        
        colors_list=['red','green','blue','#A020F0','#A63600']
        
        for i in range(len(colors_list)):
            self.ax.plot(wale_lenth,loadings[i*2,:,0],color=colors_list[i],lw=4,
                         label=f"{self.generate_string_from_number_of_component(2*i+1)}"+" "+f"{round(snr[i*2],2)}")
        
        
        # self.ax.set_xticks(range(1,n_comp[-1]+1))
        if self.x_label_control:
            self.ax.locator_params(axis='x', nbins=6)
    
        self.ax.grid(color="black", drawstyle="default", linewidth=0.7)
        self.ax.set_xlabel(x_name,  fontsize=self.ax_name_label_fontsize,
                    labelpad=15)
        self.ax.tick_params(which='major', length=10, width=2)
        self.ax.set_xticklabels(self.ax.get_xticklabels(), fontsize=self.ax_label_number_font)
        self.ax.set_yticklabels(self.ax.get_yticklabels(), fontsize=self.ax_label_number_font)
        self.ax.tick_params(axis='x', pad=15)
        self.ax.legend(loc='center', bbox_to_anchor=(ancor_a, ancor_b),ncol=2,
            fontsize=30,labelcolor=colors_list, edgecolor='black',
                       facecolor='white',framealpha=1)
        self.ax.get_xaxis().set_tick_params(direction='in')
        self.ax.get_yaxis().set_tick_params(direction='in')
    
    def painter(self, save_file_name:str,x_s:float,y_s:float,ancor_a:float,ancor_b:float,
                fluorophore_name:str,save:bool=False):
        mpl.rc('font',family='Times New Roman')
        self.fig = plt.figure(figsize=(x_s*self.col, y_s*self.row),constrained_layout=True)
        self.spec = self.fig.add_gridspec(ncols=self.col, nrows=self.row)
        #plt.subplots_adjust(wspace=0.3, hspace=0.3)
        number=0
        for row in range(self.row):
            for col in range(self.col):
                if number==0:
                    self.paint(col=col,row=row,
                               loadings=self.emission_loadings, snr=self.emission_snr,
                               wale_lenth=self.emission_wave_lenth, x_name="длина волны \nрегистрации, нм",
                               ancor_a=ancor_a,ancor_b=ancor_b)
                # self.paint_block(row,col,[1,2,3],[3,2,3],0.0123,'String')
                elif number==1:
                    self.paint(col=col,row=row,
                               loadings=self.excitation_loadings, snr=self.excitation_snr,
                               wale_lenth=self.excitation_wave_lenth, x_name="длина волны \nвозбуждения, нм",
                               ancor_a=ancor_a,ancor_b=ancor_b)
                number+=1
        plt.tight_layout(h_pad=5,w_pad=5)
        
        if save:
            plt.savefig(save_file_name+'.pdf', format='pdf', dpi=300,bbox_inches='tight')
            plt.savefig(save_file_name+'.jpg', format='jpg', dpi=300,bbox_inches='tight')
            plt.savefig(save_file_name+".svg", format="svg",bbox_inches='tight')

        plt.show()

    def main(self,data_set_name:str,fluorophore_name:str, save:bool=False,x_s:float=0,y_s:float=0,
             ancor_a:float=0,ancor_b:float=0):
        save_name=self.create_save_name(data_set_name=data_set_name,fluorophore_name=fluorophore_name,save=save)
        self.painter(save_file_name=save_name,fluorophore_name=fluorophore_name,save=save,
                     x_s=x_s,y_s=y_s,ancor_a=ancor_a,ancor_b=ancor_b)
        
  