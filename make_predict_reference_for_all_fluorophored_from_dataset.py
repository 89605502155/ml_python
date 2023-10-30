from training_algorithm import Predict
import numpy as np
from npls import npls
import pandas as pd
from predict_reference_plot import Predict_reference_plot

class Make_predict_reference_for_all_fluorophores_from_dataset:
    def __init__(self, file_name:str=None, regression_method=npls) -> None:
        self.file_name=file_name
        self.regression_method=regression_method

    def get_dataset_name(self,name:str)->str:
        names=dict()
        names['syn']='Synthetic'
        names['asmund']='asmund'
        names['dorrit']='dorrit'
        names['marat']='marat'
        return names[name]


    def painter(self,col,row,save:bool=False):
        paint=Predict_reference_plot(col=col,row=row)
        name=self.get_dataset_name(self.file_name)
        paint.main(result=self.response,dataset_name=name, save=save)

    def make_result(self):
        df1=pd.read_excel('best_param.ods', engine="odf",header=None,names=['name','n','a'])
        df2=df1[df1.name==self.file_name]
        all_result=list()
        print(df2)
        num=0
        for i,j in df2.iterrows():
            print(j['n'],type(j['a']),i)
            model=Predict(file_name=self.file_name,number_of_column=num,
                           number_of_components=[j['n']],l2_coefs=np.array([j['a']]),
                           regression_method=npls)
            result = model.main()
            num+=1
            all_result.append(result) 
        self.response=all_result
        return all_result
    

        
