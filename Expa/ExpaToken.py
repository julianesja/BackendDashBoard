'''
Created on 24 abr. 2017

@author: julian
'''

from bs4 import BeautifulSoup
import requests
class ExpaToken():
    Correo=None
    Contrasenia=None

    def __init__(self,Correo,Contrasenia):
        self.Correo=Correo
        self.Contrasenia=Contrasenia

    def getToken(self):
        AUTH_URL = "https://auth.aiesec.org/users/sign_in"
        params = {
            'user[email]': self.Correo,
            'user[password]': self.Contrasenia,
        }
        s = requests.Session()
        token_response = s.get("https://experience.aiesec.org").text
        soup = BeautifulSoup(token_response, 'html.parser')
        token2 = soup.find("form").find(attrs={'name': 'authenticity_token'}).attrs[
            'value']  # name="authenticity_token").value
        params['authenticity_token'] = token2
        response = s.post(AUTH_URL, data=params)
        try:
            if len(response.history) > 0:
                token = response.history[-1].cookies['expa_token']
                return token
            else:
                return None
        except KeyError:
            return None

