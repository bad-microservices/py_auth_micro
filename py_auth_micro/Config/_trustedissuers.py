from dataclasses import dataclass
from typing import Union
from ..Core import SignMethod

class TrustedIssuers:
    issuers: dict

    def add_issuer(self,issuer:str,supported_methods:list[SignMethod],secret:Union[str,bytes])-> None:
        self.issuers[issuer] = {
            "secret":secret,
            "methods":supported_methods
        }
    
    def check_access_token(self,token:str) -> bool:

        #check expiry_time

        #get_issuer

        #check signing method

        #check token signing with issuer secret




        return True