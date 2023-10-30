from typing import Any
import numpy

class Dataset_model:
    def __init__(self,Sectrun:numpy.ndarray, Consentration:numpy.ndarray,  
                 Emission_wale:numpy.ndarray,Exitation_wale:numpy.ndarray,
                 Name_of_column_list:list):
        self.Sectrun=Sectrun
        self.Consentration=Consentration
        self.Emission_wale=Emission_wale
        self.Exitation_wale=Exitation_wale
        self.Name_of_column_list=Name_of_column_list

    def __str__(self) -> str:
        return self.name
    
class Dataset_model_with_theoretical_loadings_only_for_synthetic:
    def __init__(self,Sectrun:numpy.ndarray, Consentration:numpy.ndarray,  
                 Emission_wale:numpy.ndarray,Exitation_wale:numpy.ndarray,
                 Name_of_column_list:list, emission_theoretical_loadings:numpy.ndarray,
                 excitation_theoretical_loadings:numpy.ndarray):
        self.Sectrun=Sectrun
        self.Consentration=Consentration
        self.Emission_wale=Emission_wale
        self.Exitation_wale=Exitation_wale
        self.Name_of_column_list=Name_of_column_list
        self.emission_theoretical_loadings=emission_theoretical_loadings
        self.excitation_theoretical_loadings=excitation_theoretical_loadings

    def __str__(self) -> str:
        return self.name

class Centering_dataset_model:
    def __init__(self,  Emission_wale: numpy.ndarray, Exitation_wale: numpy.ndarray, 
                 Name_of_column_list: str,
                 Centering_spectrum:numpy.ndarray,
                 Const_centering_spectrum:float,
                 Const_centering_concentraton:float,
                 Centering_concentration:numpy.ndarray,
                 Concentration_range:float):
        self.Emission_wale=Emission_wale
        self.Exitation_wale=Exitation_wale
        self.Centering_spectrum=Centering_spectrum
        self.Const_centering_spectrum=Const_centering_spectrum
        self.Centering_concentration=Centering_concentration
        self.Const_centering_concentraton=Const_centering_concentraton
        self.Name_of_column_list=Name_of_column_list
        self.Concentration_range=Concentration_range

    def __str__(self) -> str:
        return self.name


class Cross_validation_dataset_model:
    def __init__(self, Emission_wale: numpy.ndarray, Exitation_wale: numpy.ndarray, 
                 Name_of_column_list: str,
                 Train_spectrum:numpy.ndarray,
                 Test_spectrum:numpy.ndarray,
                 Train_concentration:numpy.ndarray,
                 Test_concentration:numpy.ndarray,
                 Const_centering_concentraton:float=0,
                 Const_centering_spectrum:float=0,
                 Concentration_range:float=1):
        self.Emission_wale=Emission_wale
        self.Exitation_wale=Exitation_wale
        self.Train_spectrum=Train_spectrum
        self.Test_spectrum=Test_spectrum
        self.Train_concentration=Train_concentration
        self.Test_concentration=Test_concentration
        self.Name_of_column_list=Name_of_column_list
        self.Const_centering_concentraton=Const_centering_concentraton
        self.Const_centering_spectrum=Const_centering_spectrum
        self.Concentration_range=Concentration_range

    def __str__(self) -> str:
        return self.name
    
    