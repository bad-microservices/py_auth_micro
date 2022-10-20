from abc import ABC, abstractmethod

class LoginBaseClass(ABC):
    username:str
    password:str
    ldap_config:str

    
    def __init__(self,**kwargs):

        for key,value in kwargs.items():
            if key in self.__annotations__.keys():
                setattr(self,key,value)
        pass
       
    def __repr__(self):
        data_list=[]
        for key,value in self.__dict__.items():

            data_list.append(f"{key}={value!r}")
        return f"{self.__class__.__name__}({', '.join(data_list)})"
    
    @abstractmethod
    def perform_login()->bool:
        pass
