from open import Open_file
from centering_and_cross_validation import Cross_validation as cv
from dataset_model import Cross_validation_dataset_model as cvdm
from npls import npls
from sklearn.metrics import r2_score, make_scorer
import sklearn
from sklearn.model_selection import ShuffleSplit
from sklearn.metrics import mean_squared_error
import numpy as np
from sklearn.model_selection import GridSearchCV
from dataset_model import Dataset_model as dm

class Training:
    def __init__(self, file_name:str=None,number_of_column:int=0, regression_method=npls,
                 number_of_components:list=[6],l2_coefs:np.ndarray=np.array([0.1])) -> None:
        self.file_name=file_name
        self.number_of_column=number_of_column
        self.regression_method=regression_method
        self.number_of_components=number_of_components
        self.l2_coefs=l2_coefs

    def train(self,data:cvdm):
        model=self.regression_method()
        scoring={'mse': make_scorer(mean_squared_error),'r2':'r2'}
        shuffle_split = ShuffleSplit(n_splits=27,test_size=1*0.1428, random_state=42)
        parametrsNames={
            'n_components': self.number_of_components,
            'a': self.l2_coefs
            }
        gridCought=GridSearchCV(model, parametrsNames, cv=shuffle_split, scoring=scoring,
                          refit='r2', return_train_score=True)
        gridCought.fit(data.Train_spectrum,data.Train_concentration)
        # gridCought.fit(X_train, y_train)
        r2_p=gridCought.score(data.Test_spectrum,data.Test_concentration)
        # mse_cv=gridCought.cv_results_[ "mean_test_mse" ]
        # mse_c=gridCought.cv_results_[ "mean_train_mse" ]
        # r2_cv=gridCought.cv_results_[ "mean_test_r2" ]
        # r2_c=gridCought.cv_results_[ "mean_train_r2" ]
        #gridCought.cv_results_['std_test_mse'
        return [r2_p,gridCought.cv_results_,gridCought.best_params_,gridCought.best_estimator_]

    def main(self):
        b=Open_file()
        a=b.main(file_name=self.file_name)
        mod=cv(data=a,number_of_column=self.number_of_column)
        data=mod.main()
        resoult=self.train(data=data)
        resoult.append(data.Concentration_range)
        resoult.append(b.get_number_column_concentration()[self.file_name])
        return resoult
    
class Predict:
    def __init__(self, file_name:str=None,number_of_column:int=0, regression_method=npls,
                 number_of_components:list=[6],l2_coefs:np.ndarray=np.array([0.1])) -> None:
        self.file_name=file_name
        self.number_of_column=number_of_column
        self.regression_method=regression_method
        self.number_of_components=number_of_components
        self.l2_coefs=l2_coefs

    def rmse(self,pred,y)->float:
        mse=mean_squared_error(y_true=y,y_pred=pred)
        return pow(mse,0.5)
    
    def concat(self,p1,p2):
        p=[]
        for i in p1:
            p.append(i)
        for i in p2:
            p.append(i)
        return np.array(p)
    
    def train(self,data:cvdm,all_data:dm,number_of_column:int,concentration_range:float=1):
        model=self.regression_method()
        scoring={'mse': make_scorer(mean_squared_error),'r2':'r2'}
        shuffle_split = ShuffleSplit(n_splits=27,test_size=1*0.1428, random_state=42)
        parametrsNames={
            'n_components': self.number_of_components,
            'a': self.l2_coefs
            }
        gridCought=GridSearchCV(model, parametrsNames, cv=shuffle_split, scoring=scoring,
                          refit='r2', return_train_score=True)
        gridCought.fit(data.Train_spectrum,data.Train_concentration)
        # r2_p=gridCought.score(data.Test_spectrum,data.Test_concentration)
        # predictors1=gridCought.predict(data.Test_spectrum)
        # predictors2=gridCought.predict(data.Train_spectrum)
        x_mean=all_data.Sectrun.mean(axis=0)
        predictors=gridCought.predict(all_data.Sectrun-x_mean)
        predictors+=data.Const_centering_concentraton
        # predictors=self.concat(predictors1,predictors2)
        y=all_data.Consentration[:,number_of_column]
        rmse=self.rmse(pred=predictors,y=y)
        # predictors+=data.Const_centering_concentraton
        return [y,predictors,rmse,rmse/concentration_range,data.Name_of_column_list]

    def main(self)->list:
        b=Open_file()
        a=b.main(file_name=self.file_name)
        mod=cv(data=a,number_of_column=self.number_of_column)
        data=mod.main()
        resoult=self.train(data=data,all_data=a,number_of_column=self.number_of_column,
                           concentration_range=data.Concentration_range)
        resoult.append(data.Concentration_range)
        return resoult

    
