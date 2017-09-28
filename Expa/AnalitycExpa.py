import requests
import json
from urllib.parse import urlencode
class AnalitycExpa():
    TokenExpa=None
    def __init__ (self,TokenExpa):
        self.TokenExpa=TokenExpa

    def ConsultCountry(self,DateInit,DateFinish,Programe,Type,CodeOffice):
        params = {"access_token":self.TokenExpa
                      ,"start_date":DateInit.strftime("%y-%m-%d")
                       ,"end_date":DateFinish.strftime("%y-%m-%d")
                      ,"basic[home_office_id]":CodeOffice 
                      ,"basic[type]":Type
                      ,"programmes[]":Programe
        }
        baseUrl = "https://gis-api.aiesec.org/{version}/{routes}?{params}"
        
        url=baseUrl.format(version='v2', routes="applications/analyze.json", params=urlencode(params, True))
        r = requests.get(url)
        if int(r.status_code)==200:
            Comites=json.loads(r.text)
            return True, Comites["analytics"]["children"]["buckets"]
        else:
            print("salio mal")
            return False, None

    def ConsultCountry(self, DateInit, DateFinish, Programe, Type, CodeOffice):
        params = {"access_token": self.TokenExpa
            , "start_date": DateInit.strftime("%y-%m-%d")
            , "end_date": DateFinish.strftime("%y-%m-%d")
            , "basic[home_office_id]": CodeOffice
            , "basic[type]": Type
            , "programmes[]": Programe
                  }
        baseUrl = "https://gis-api.aiesec.org/{version}/{routes}?{params}"

        url = baseUrl.format(version='v2', routes="applications/analyze.json", params=urlencode(params, True))
        r = requests.get(url)
        if int(r.status_code) == 200:
            Comites = json.loads(r.text)
            return True, Comites["analytics"]["children"]["buckets"]
        else:
            print("salio mal")
            return False, None


