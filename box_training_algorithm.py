from open import Open_file
from centering_and_cross_validation import Cross_validation as cv
from centering_and_cross_validation import Cross_validation_for_pls as cvpls
from centering_and_cross_validation import Centetering
from dataset_model import Cross_validation_dataset_model as cvdm
from npls import npls
from sklearn.metrics import r2_score, make_scorer
from sklearn.cross_decomposition import PLSRegression
import sklearn
from sklearn.model_selection import ShuffleSplit
from sklearn.metrics import mean_squared_error
import numpy as np
import warnings
from numpy.linalg import LinAlgError
from paint_scripts.draw_valid_matrix_rus import Draw_valid_matrix_rus as painter
from sklearn.model_selection import GridSearchCV
from dataset_model import Dataset_model as dm
from dataset_model import Centering_dataset_model as cdm
from sklearn.exceptions import FitFailedWarning
import numpy as np
from sklearn.base import BaseEstimator
from sklearn.base import RegressorMixin
from signal_noise import signal_noise

class npls_(RegressorMixin,BaseEstimator):
    def  __init__(self, excitation_wavelenth:np.ndarray,
                  emission_wavelenth:np.ndarray, n_components:int=2,a:float=3,
                  derivative_rang:list=[],norm_func:list=[],
                  crash_norm_name:str=None,crash_norm_value:float=None):
        self.n_components = n_components
        self.a=a
        self.derivative_rang=derivative_rang
        self.norm_func=norm_func
        self.crash_norm_name=crash_norm_name
        self.crash_norm_value=crash_norm_value
        self.excitation_wavelenth=excitation_wavelenth
        self.emission_wavelenth=emission_wavelenth

    def check_smooth_loadings(self,w_i,excitation_wavelenth,
                              w_k,emission_wavelenth, n_component:int) -> dict[str,dict]:
        # print(w_i.shape,excitation_wavelenth.shape,
        #                       w_k.shape,emission_wavelenth.shape, n_component)
        resp_emission=self.chek_smooth_one_model(w_k,emission_wavelenth)
        resp_excitation=self.chek_smooth_one_model(w_i,excitation_wavelenth)
        if self.crash_norm_name is not None:
            #print(resp_emission,self.crash_norm_name,resp_emission[self.crash_norm_name],resp_excitation[self.crash_norm_name])
            for j in range(len(resp_emission[self.crash_norm_name])):
                #print(resp_emission[self.crash_norm_name][j])
                if resp_emission[self.crash_norm_name][j]<=self.crash_norm_value:
                    error_message_1=f'Emission {n_component} component is a very noisy.'
                    error_message_2=' May be you can choose another norm.'
                    error_message_3=f' Now you choose {self.crash_norm_name} norm'
                    error_message=error_message_1+error_message_2+error_message_3
                    raise ValueError(error_message)
                if resp_excitation[self.crash_norm_name][j]<=self.crash_norm_value:
                    error_message_1=f'Excitation {n_component} component is a very noisy.'
                    error_message_2=' May be you can choose another norm.'
                    error_message_3=f' Now you choose {self.crash_norm_name} norm'
                    error_message=error_message_1+error_message_2+error_message_3
                    raise ValueError(error_message)
        return {
            "Emission":resp_emission,
            "Excitation":resp_excitation
            }


    def chek_smooth_one_model(self,signal,x) -> dict[str, list]:
        model=signal_noise()
        response=model.main(signal=signal,x=x)
        #print(response,signal,x)
        return response

    def fit(self, xtrain, ytrain):
        """Fits the model to the data (X, y)
        Parameters
        ----------
        X : ndarray
        y : 1D-array of shape (n_samples, )
            labels associated with each sample


            """
        x=xtrain.copy()
        y=ytrain.copy()

        if len(self.derivative_rang)>0:
            self.snr_emission=list()
            self.snr_excitation=list()
        Tt=np.zeros([x.shape[0],self.n_components])
        mass=np.zeros([y.shape[0]])
        y_copy=ytrain.copy()
        w_k_mass=np.zeros([self.n_components,x.shape[1],1])
        w_i_mass=np.zeros([self.n_components,x.shape[2],1])
        bf_array=[]

        mmas=np.zeros([x.shape[0],x.shape[1],x.shape[2]])
        z_pz=np.eye(x.shape[1])

        for f in range(0,self.n_components):
            z=np.zeros([x.shape[1],x.shape[2]])
            x_product=np.zeros([x.shape[0],x.shape[1],x.shape[2]])
            for i in range(0,x.shape[0]):
                x_product[i,:,:]=y[i]*x[i,:,:]
            z=x_product.sum(axis=0)
            Wk, S, WI = np.linalg.svd(z)
            w_k=np.array(Wk[:,0]).reshape(x.shape[1],1)
            w_i=np.array(WI[0,:]).reshape(x.shape[2],1)

            if len(self.derivative_rang)>0:
                response=self.check_smooth_loadings(w_i=w_i[:,0],excitation_wavelenth=self.excitation_wavelenth,
                                           w_k=w_k[:,0],emission_wavelenth=self.emission_wavelenth,
                                           n_component=f)
                self.snr_emission.append(response['Emission'])
                self.snr_excitation.append(response['Excitation'])

            w_k_mass[f,:,:]=w_k
            w_i_mass[f,:,:]=w_i
            for h in range(0,x.shape[0]):
                Tt[h,f]=np.dot(np.dot(w_i.transpose(),x[h,:,:].transpose()),w_k)
            T=np.array(Tt[:,0:f+1]).reshape(x.shape[0],f+1)
            bf=np.dot((np.dot(np.linalg.inv(np.dot(T,T.transpose())-(((self.a))*np.eye(x.shape[0]))),T)).transpose(),
                        y.reshape([x.shape[0],1]))
            bf_array+=[bf]
            WW=np.kron(w_k,w_i).reshape(x.shape[1],x.shape[2])
            for g in range(0,x.shape[0]):
                mmas[g,:,:]=Tt[g,f]*WW
            x=np.array(x-(mmas))
            y=(y-(np.dot(T,bf)).reshape(x.shape[0]))
            mass+=(np.dot(T,bf)).reshape(x.shape[0]).reshape(x.shape[0])
            bf=0
        self.bf_array=bf_array
        self.train_error=(np.square(mass - y_copy)).mean(axis=None)
        self.w_k=w_k_mass
        self.w_i=w_i_mass

        return self

    def predict(self, xtest):
        x=xtest.copy()
        Tt=np.zeros([x.shape[0],self.n_components])
        y=np.zeros([x.shape[0]])
        mmas=np.zeros([x.shape[0],x.shape[1],x.shape[2]])
        for f in range(0,self.n_components):
            w_k=self.w_k[f,:,:]
            w_i=self.w_i[f,:,:]
            for h in range(0,x.shape[0]):
                Tt[h,f]=np.dot(np.dot(w_i.transpose(),x[h,:,:].transpose()),w_k)
            T=np.array(Tt[:,0:f+1]).reshape(x.shape[0],f+1)
            WW=np.kron(w_k,w_i).reshape(x.shape[1],x.shape[2])
            for g in range(0,x.shape[0]):
                mmas[g,:,:]=Tt[g,f]*WW
            x=np.array(x-(mmas))
            y=(y+(np.dot(T,self.bf_array[f])).reshape(x.shape[0]))
        return y



class Box_training_algorithm:
    def __init__(self, file_name:str=None,number_of_column:int=0, regression_method=npls,
                 number_of_components:list=[6],l2_coefs:np.ndarray=np.array([0.1]),
                 derivative_rang:list=None,norm_func:list=None,snr:float=100.0) -> None:
        self.file_name=file_name
        self.number_of_column=number_of_column
        self.regression_method=regression_method
        self.number_of_components=number_of_components
        self.l2_coefs=l2_coefs
        self.derivative_rang=derivative_rang
        self.norm_func=norm_func
        self.snr=snr

    def train(self,l2,n_comp,conc_range,data:cvdm):
        if self.derivative_rang is None:
            model=npls_(excitation_wavelenth=data.Exitation_wale,
                                        emission_wavelenth=data.Emission_wale,derivative_rang=[2],
                                        crash_norm_name='evklid',crash_norm_value=self.snr)
        else:
            model=npls_(excitation_wavelenth=data.Exitation_wale,
                                         emission_wavelenth=data.Emission_wale,
                                         norm_func=self.norm_func,derivative_rang=[2],
                                         crash_norm_name='evklid',crash_norm_value=self.snr)
        scoring={'mse': make_scorer(mean_squared_error),'r2':'r2'}
        shuffle_split = ShuffleSplit(n_splits=27,test_size=1*0.1428, random_state=42)
        parametrsNames={
                'n_components': [n_comp],
                'a': np.array([l2]),
            }
        try:
            gridCought=GridSearchCV(model, parametrsNames, cv=shuffle_split, scoring=scoring,
                            refit='r2', return_train_score=True)
            
            gridCought.fit(data.Train_spectrum,data.Train_concentration)
        
            q2_p=gridCought.score(data.Test_spectrum,data.Test_concentration)
            
            rmse_p=np.sqrt(mean_squared_error(data.Test_concentration,gridCought.predict(data.Test_spectrum)
                                                ))/conc_range
            rmse_cv=np.sqrt(gridCought.cv_results_[ "mean_test_mse" ][0])/conc_range
            q2_cv=gridCought.cv_results_[ "mean_test_r2" ][0]
        
        except (ValueError,LinAlgError,FitFailedWarning,AttributeError):
            rmse_p=np.nan
            rmse_cv=np.nan
            q2_p=np.nan
            q2_cv=np.nan
        return [rmse_p,rmse_cv,q2_p,q2_cv]
        
                                
    def return_resoults(self):
        return [self.rmse_p,self.rmse_cv,self.q2_p,self.q2_cv]

    def calc(self):
        b=Open_file()
        a=b.main(file_name=self.file_name)
        mod=cv(data=a,number_of_column=self.number_of_column,
               test_size_for_split=0.1428)
        data=mod.main()
        rmse_p_=[]
        rmse_cv_=[]
        q2_p_=[]
        q2_cv_=[]
        for i in self.number_of_components:
            rmse_p=[]
            rmse_cv=[]
            q2_p=[]
            q2_cv=[]
            for j in self.l2_coefs:
                resoult=self.train(data=data,l2=j,n_comp=i,conc_range=data.Concentration_range)
                rmse_p.append(resoult[0])
                rmse_cv.append(resoult[1])
                q2_p.append(resoult[2])
                q2_cv.append(resoult[3])
            rmse_p_.append(rmse_p)
            rmse_cv_.append(rmse_cv)
            q2_p_.append(q2_p)
            q2_cv_.append(q2_cv)
        self.rmse_p=np.array(rmse_p_)
        self.rmse_cv=np.array(rmse_cv_)
        self.q2_p=np.array(q2_p_)
        self.q2_cv=np.array(q2_cv_)

    def __find_best_param(self,string,value,arr):
        for i in range(self.rmse_p.shape[0]):
            for j in range(self.rmse_p.shape[1]):
                #print(value)
                if value==arr[i][j]:
                    print(string,self.file_name,self.number_of_column,value,
                          self.number_of_components[i],self.l2_coefs[j])
                    # return i,j
                    
    def __find_best_param_q(self,string,value,arr):
        for i in range(self.rmse_p.shape[0]):
            for j in range(self.rmse_p.shape[1]):
                if value==arr[i][j]:
                    print(string,self.file_name,self.number_of_column,value,
                          self.number_of_components[i],np.log10([self.l2_coefs[j]])[0])
                    return i,j

    def best_params(self):
        best_rmse_cv=np.nanmin(self.rmse_cv)
        best_q2_cv=np.nanmax(self.q2_cv)
        # self.__find_best_param("RMSE_CV",best_rmse_cv,arr=self.rmse_cv)
        i,j=self.__find_best_param_q("Q2_CV",best_q2_cv,arr=self.q2_cv)
        rmse_p=self.rmse_p[i][j]
        q2_p=self.q2_p[i][j]
        print("RMSE_CV ",self.rmse_cv[i][j])
        print("RMSE_P ",rmse_p)
        print("Q2_P ",q2_p)

        print()
        print()
        print()

    def paint_rmse_p(self,metrics_name:str,save:bool=False):
        plotter=painter(self.rmse_cv,l2=self.l2_coefs,n_comp=self.number_of_components,
                        substanse_name= self.file_name+"_"+str(self.number_of_column),metrics_name=metrics_name)
        plotter.main(save=save)

    def paint_rmse_log(self,metrics_name:str,save:bool=False):
        plotter=painter(np.log10(self.rmse_cv),l2=self.l2_coefs,n_comp=self.number_of_components,
                        substanse_name= self.file_name+"_"+str(self.number_of_column),metrics_name=metrics_name+"_log10")
        plotter.main(save=save)

    def paint_q2_cv(self,metrics_name:str,save:bool=False):
        plotter=painter(self.q2_cv,l2=self.l2_coefs,n_comp=self.number_of_components,
                        substanse_name= self.file_name+"_"+str(self.number_of_column),metrics_name=metrics_name)
        plotter.main(save=save)

class Box_training_algorithm_pls:
    def __init__(self, file_name:str=None,number_of_column:int=0, regression_method=npls,
                 number_of_components:list=[6]) -> None:
        self.file_name=file_name
        self.number_of_column=number_of_column
        self.regression_method=regression_method
        self.number_of_components=number_of_components

    def train(self,n_comp,random,conc_range,data:cvdm):
        model=PLSRegression()
        scoring={'mse': make_scorer(mean_squared_error),'r2':'r2'}
        shuffle_split = ShuffleSplit(n_splits=27,test_size=1*0.1428, random_state=random)
        parametrsNames={
                'n_components': [n_comp],
            }
        try:
            gridCought=GridSearchCV(model, parametrsNames, cv=shuffle_split, scoring=scoring,
                            refit='r2', return_train_score=True)
            
            gridCought.fit(data.Train_spectrum,data.Train_concentration)
        
            q2_p=gridCought.score(data.Test_spectrum,data.Test_concentration)
            
            rmse_p=np.sqrt(mean_squared_error(data.Test_concentration,gridCought.predict(data.Test_spectrum)
                                                ))/conc_range
            rmse_cv=np.sqrt(gridCought.cv_results_[ "mean_test_mse" ][0])/conc_range
            q2_cv=gridCought.cv_results_[ "mean_test_r2" ][0]
        
        except (ValueError,LinAlgError,FitFailedWarning,AttributeError):
            rmse_p=np.nan
            rmse_cv=np.nan
            q2_p=np.nan
            q2_cv=np.nan
        return [rmse_p,rmse_cv,q2_p,q2_cv]
        
                                
    def return_resoults(self):
        return [self.rmse_p,self.rmse_cv,self.q2_p,self.q2_cv]

    def calc(self,random):
        b=Open_file()
        a=b.main(file_name=self.file_name)
        mod=cvpls(data=a,number_of_column=self.number_of_column,
               test_size_for_split=0.1428)
        data=mod.main()
        rmse_p_=[]
        rmse_cv_=[]
        q2_p_=[]
        q2_cv_=[]
        for i in self.number_of_components:
            resoult=self.train(data=data,n_comp=i,conc_range=data.Concentration_range,random=random)
            
            rmse_p_.append(resoult[0])
            rmse_cv_.append(resoult[1])
            q2_p_.append(resoult[2])
            q2_cv_.append(resoult[3])
        self.rmse_p=np.array(rmse_p_)
        self.rmse_cv=np.array(rmse_cv_)
        self.q2_p=np.array(q2_p_)
        self.q2_cv=np.array(q2_cv_)

    def __find_best_param(self,string,value,arr):
        for i in range(self.rmse_p.shape[0]):
            #print(value)
            if value==arr[i]:
                print(string,self.file_name,self.number_of_column,value,
                        self.number_of_components[i])
                # return i,j
                    
    def __find_best_param_q(self,string,value,arr):
        for i in range(self.rmse_p.shape[0]):
            if value==arr[i]:
                print(string,self.file_name,self.number_of_column,value,
                        self.number_of_components[i])
                return i

    def best_params(self):
        best_rmse_cv=np.nanmin(self.rmse_cv)
        best_q2_cv=np.nanmax(self.q2_cv)
        # self.__find_best_param("RMSE_CV",best_rmse_cv,arr=self.rmse_cv)
        i=self.__find_best_param_q("Q2_CV",best_q2_cv,arr=self.q2_cv)
        rmse_p=self.rmse_p[i]
        q2_p=self.q2_p[i]
        print("RMSE_CV ",self.rmse_cv[i])
        print("RMSE_P ",rmse_p)
        print("Q2_P ",q2_p)

        print()
        print()
        print()




            
    