import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import matplotlib as mpl
from dataset_model import Dataset_model as dm
# from dataset_model import Cross_validation_dataset_model as cvdm
from dataset_model import Centering_dataset_model as cdm
from pathlib import Path
from training_algorithm import Predict

class Predict_reference_plot:
    def __init__(self,col:int=2,row:int=2,ax_name_label_fontsize:int=42,
                 title_label_name_fontsize:int=45, text_size_in_box:int=42,
                 ax_label_number_font:int=40
                 ) -> None:
        self.col=col
        self.row=row
        self.ax_name_label_fontsize=ax_name_label_fontsize
        self.title_label_name_fontsize=title_label_name_fontsize
        self.text_size_in_box=text_size_in_box
        self.ax_label_number_font=ax_label_number_font

    def info(self):
        print('Use only main function for work with this class.')

    def paint_block(self,row,col,y,pred,rmse,name:str):
        self.ax = self.fig.add_subplot(self.spec[row, col])
        self.ax.plot(y,y,'blue',lw=3)
        self.ax.plot(y,pred,'.',color='red',ms=20)
        self.ax.grid(color="black", drawstyle="default", linewidth=0.7)
        self.ax.set_xlabel("Введено",  fontsize=self.ax_name_label_fontsize,
                    labelpad=15)
        self.ax.set_ylabel("Найдено",  fontsize=self.ax_name_label_fontsize,
                    labelpad=15)
        self.ax.set_title(self.rus_names(name), fontsize=self.title_label_name_fontsize,
                   loc="center" ,pad=15)
        self.ax.tick_params(which='major', length=10, width=2)
        if rmse>=0.0001:
            stri='$\\frac {RMSE}{ДК}$'+'='+str(rmse.round(4))
        else:
            stri='$\\frac {RMSE}{ДК}$'+'<0.0001'
        self.ax.text(1.1*min(y),0.85*max([max(y),max(pred)]),stri, fontsize=self.text_size_in_box,fontweight='bold',
              bbox=dict(boxstyle="round",fc='white',ec='black'))
        self.ax.set_xticklabels(self.ax.get_xticklabels(), fontsize=self.ax_label_number_font)
        self.ax.set_yticklabels(self.ax.get_yticklabels(), fontsize=self.ax_label_number_font)
        self.ax.get_xaxis().set_tick_params(direction='in')
        self.ax.get_yaxis().set_tick_params(direction='in')

    def make_dir_name(self,name_dataset:str|None)->str:
        if name_dataset==None:
            return 'plots2_ru_p/none'
        else:
            return 'plots2_ru_p/'+str(name_dataset)


    def make_full_name_file(self,name_dataset:str|None)->str:
        return self.make_dir_name(name_dataset=name_dataset)+'/'+'predict_reference'
    
    def rus_names(self,name:str)->str:
        match name:
            case 'humic':return 'гумины'
            case 'tryptophane': return 'триптофан'
            case 'tyrosine': return 'тирозин'
            case 'catechol': return 'катехол'
            case 'hydroquinone': return 'гидрохинон'
            case 'indole': return 'индол'
            case 'resorcinol': return 'резорцин'
            case 'phenylalanine': return 'фелинлаланин'
            case 'DOPA': return 'DOPA'
            case 'first': return 'первый флуорофор'
            case'second': return 'второй флуорофор'
            case 'third': return 'третий флуорофор'
            case 'fourth': return 'четвертый флуорофор'
            case _:return ' '
        
        

    def paint(self,result:list,save:bool=False,dataset_name:str='Synthetic'):
        mpl.rc('font',family='Times New Roman')
        self.fig = plt.figure(figsize=(9*self.col, 9.5*self.row),constrained_layout=True)
        self.spec = self.fig.add_gridspec(ncols=self.col, nrows=self.row)
        #plt.subplots_adjust(wspace=0.3, hspace=0.3)
        number=0
        for row in range(self.row):
            for col in range(self.col):
                try:
                    if dataset_name=='asmund' and result[number][5]=='tyrosine':
                        raise IndexError
                    self.paint_block(row=row,col=col,
                                    y=result[number][0],
                                    pred=result[number][1],
                                    rmse=result[number][3],
                                    name=result[number][5])
                    # self.paint_block(row,col,[1,2,3],[3,2,3],0.0123,'String')
                    number+=1
                except IndexError:
                    continue
        plt.tight_layout(h_pad=5,w_pad=5)
        if save:
            dir_name=self.make_dir_name(name_dataset=dataset_name)
            Path(dir_name).mkdir(parents=True, exist_ok=True)
            file_name=self.make_full_name_file(name_dataset=dataset_name)
            plt.savefig(file_name+'.pdf', format='pdf', dpi=300,bbox_inches='tight')
            plt.savefig(file_name+'.jpg', format='jpg', dpi=300,bbox_inches='tight')
            plt.savefig(file_name+".svg", format="svg",bbox_inches='tight')

        plt.show()

    def main(self,result:list,save:bool=False,dataset_name:str='Synthetic'):

        self.paint(result=result,save=save,dataset_name=dataset_name)


# class Predicted_reference_controller:
#     def __init__(self,col:int=2,row:int=2,ax_name_label_fontsize:int=42,
#                  title_label_name_fontsize:int=45, text_size_in_box:int=42,
#                  ax_label_number_font:int=40
#                  ) -> None:
#         self.col=col
#         self.row=row
#         self.ax_name_label_fontsize=ax_name_label_fontsize
#         self.title_label_name_fontsize=title_label_name_fontsize
#         self.text_size_in_box=text_size_in_box
#         self.ax_label_number_font=ax_label_number_font
