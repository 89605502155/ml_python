from dataset_model import Dataset_model as dm
from dataset_model import Cross_validation_dataset_model as cvdm
from dataset_model import Centering_dataset_model as cdm
from sklearn.model_selection import train_test_split

class Centetering:
    def __init__(self,data:dm,number_of_column:int=0) -> None:
        self.data=data
        self.number_of_column=number_of_column

    def centering(self):
        y_mean=self.data.Consentration[:,self.number_of_column].mean()
        x_mean=self.data.Sectrun.mean(axis=0)
        return [x_mean, y_mean]
    
    def main(self)-> cdm:
        centering_constants_list=self.centering()
        concentration_range=max(self.data.Consentration[:,self.number_of_column])-min(self.data.Consentration[:,self.number_of_column])
        a=cdm(Emission_wale=self.data.Emission_wale,
              Exitation_wale=self.data.Exitation_wale,
              Name_of_column_list=self.data.Name_of_column_list[self.number_of_column],
              Centering_concentration=self.data.Consentration[:,self.number_of_column]-centering_constants_list[1],
              Const_centering_concentraton=centering_constants_list[1],
              Const_centering_spectrum=centering_constants_list[0],
              Centering_spectrum=self.data.Sectrun-centering_constants_list[0],
              Concentration_range=concentration_range)
        return a
    
class Cross_validation:
    def __init__(self,data:dm,number_of_column:int=0, is_centering_needs:bool=True,test_size_for_split:float=0.1428) -> None:
        self.data=data
        self.number_of_column=number_of_column
        self.is_centering_needs=is_centering_needs
        self.test_size_for_split=test_size_for_split

    def cross_validation(self, spectrum:dm|cdm)->cvdm:
        if cdm==type(spectrum):
            X_train, X_test, y_train, y_test = train_test_split(
                spectrum.Centering_spectrum, spectrum.Centering_concentration,
                  test_size=self.test_size_for_split, random_state=42)
            cross_validation_data=cvdm(Emission_wale=self.data.Emission_wale,
                                       Exitation_wale=self.data.Exitation_wale,
                                       Name_of_column_list=spectrum.Name_of_column_list,
                                       Train_concentration=y_train,
                                       Test_concentration=y_test,
                                       Train_spectrum=X_train,
                                       Test_spectrum=X_test,
                                       Const_centering_concentraton=spectrum.Const_centering_concentraton,
                                       Const_centering_spectrum=spectrum.Const_centering_spectrum,
                                       Concentration_range=spectrum.Concentration_range)
        elif dm==type(spectrum):
            X_train, X_test, y_train, y_test = train_test_split(
                spectrum.Sectrun, spectrum.Consentration[:,self.number_of_column],
                  test_size=self.test_size_for_split, random_state=42)
            cross_validation_data=cvdm(Emission_wale=self.data.Emission_wale,
                                       Exitation_wale=self.data.Exitation_wale,
                                       Name_of_column_list=self.data.Name_of_column_list[self.number_of_column],
                                       Train_concentration=y_train,
                                       Test_concentration=y_test,
                                       Train_spectrum=X_train,
                                       Test_spectrum=X_test,
                                       Concentration_range=max(self.data.Consentration[:,self.number_of_column])-min(self.data.Consentration[:,self.number_of_column])
        )
        else:
            raise TypeError('You have some problems with centering_and_cross_validation.py 60 line')
        return cross_validation_data


    def main(self)->cvdm:
        if self.is_centering_needs:
            centering_model=Centetering(data=self.data,number_of_column=self.number_of_column)
            centering_data=centering_model.main()
            cross_validation_data=self.cross_validation(centering_data)
        else:
            cross_validation_data=self.cross_validation(self.data)
        return cross_validation_data