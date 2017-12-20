import requests
import json
from urllib.parse import urlencode
from lcperformance.models import user_register
from Expa.ExpaToken import ExpaToken
class Administracion:

    def currentOffice(self, token):
        params = {"access_token": token}
        baseUrl = "https://gis-api.aiesec.org/{version}/{routes}?{params}"
        url = baseUrl.format(version='v2', routes="current_person.json", params=urlencode(params, True))
        r = requests.get(url)
        if int(r.status_code) == 200:
            persona = json.loads(r.text)
            return True, persona["current_offices"]
        else:
            print("salio mal")
            return False, None, None

    def consulRealizeOgx(self, token, fechaInicial, fechaFinal, Programa, comite, per_page, page):
        params = {'access_token': token,
                  'filters[date_realized[from]]': fechaInicial,
                  'filters[date_realized[to]]': fechaFinal,
                  'filters[programmes][]': Programa,
                  'filters[person_committee]': comite,
                  'per_page': per_page,
                   'page': page
                  }
        baseUrl = "https://gis-api.aiesec.org/{version}/{routes}?{params}"
        url = baseUrl.format(version='v2', routes="applications.json", params=urlencode(params, True))

        r = requests.get(url)
        if int(r.status_code) == 200:
            datos = json.loads(r.text)
            return True, datos
        else:
            print("salio mal")
            return False, None


    def consulRealizeIgx(self, token, fechaInicial, fechaFinal, Programa, comite, per_page, page):
        params = {'access_token': token,
                  'filters[date_realized[from]]': fechaInicial,
                  'filters[date_realized[to]]': fechaFinal,
                  'filters[programmes][]': Programa,
                  'filters[opportunity_committee]': comite,
                  'per_page': per_page,
                  'page': page,
                  'filters[for]': 'opportunities',
                  'sort': 'status'

                  }
        baseUrl = "https://gis-api.aiesec.org/{version}/{routes}?{params}"
        url = baseUrl.format(version='v2', routes="applications.json", params=urlencode(params, True))

        r = requests.get(url)
        if int(r.status_code) == 200:
            datos = json.loads(r.text)
            return True, datos
        else:
            print("salio mal")
            return False, None
        pass

    def getTokenAdmin(self):
        objUserRegister = user_register.objects.filter(user_expa='dev.colombia@ai.aiesec.org')[0]
        objExpaToken = ExpaToken(objUserRegister.user_expa, objUserRegister.password_expa)
        Token = objExpaToken.getToken()
        return Token