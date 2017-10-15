from podio.pypodio2 import api
from podio.ExtraerInformacionPodio import ExtraerInformacionPodio
from datetime import datetime
from lcperformance.models import user_register, aplicacion


class ProcesoOGEPodio():
    objExtraerInformacionPodio = ExtraerInformacionPodio()


    def consultarMes(self, comite, fechaInicio, fechaFin):
        lstResultadoOpenUniversidad = {}
        lstResultadoOpenMes = {}
        lstResultadoHowMeet = {}
        lstOGV = {}

        intOffSet = 0
        intNumeroLista = 500
        params = {
            'limit': 500,
            "offset": intOffSet,
            'filters': [
                {
                    "key": "lc",
                    "values": int(comite)
                },
                {
                    "key": "created_on",
                    "values": {"from": fechaInicio, "to": fechaFin}
                }

            ],
        }
        objAplicacion = aplicacion.objects.filter(unique_name='mc_oge')[0]
        objUsuario = user_register.objects.filter(user_expa='desarrollo.upb@aiesec.net')[0]

        ApiOgeManager = api.OAuthAppClient(objUsuario.id_cliente_podio
                                           , objUsuario.codigo_secreto_podio
                                           , objAplicacion.podio_id
                                           , objAplicacion.code_secret)

        lstTotal = []
        request = 0
        while intNumeroLista >= 500:
            lstParcial = self.__ConsultarDatos(ApiOgeManager, params, objAplicacion.podio_id)
            lstTotal = lstTotal + lstParcial
            intNumeroLista = len(lstParcial)
            intOffSet = intOffSet + 500
            params["offset"] = intOffSet
            request = request + 1
            print(request)

        for aplicante in lstTotal:
            values = aplicante["values"]
            initial_revision = aplicante["initial_revision"]

            if "howmet-2" in values.keys():
                if values["howmet-2"] in lstResultadoHowMeet.keys():
                    lstResultadoHowMeet[values["howmet-2"]] = lstResultadoHowMeet[values["howmet-2"]] + 1
                else:
                    lstResultadoHowMeet[values["howmet-2"]] = 1

            if "university" in values.keys():
                if values["university"] in lstResultadoOpenUniversidad.keys():
                    lstResultadoOpenUniversidad[values["university"]] = lstResultadoOpenUniversidad[
                                                                            values["university"]] + 1
                else:
                    lstResultadoOpenUniversidad[values["university"]] = 1

            if "created_on" in initial_revision.keys():
                print(initial_revision["created_on"])
                dt = datetime.strptime(initial_revision["created_on"], "%Y-%m-%d %H:%M:%S")

                if str(dt.month) in lstResultadoOpenMes.keys():
                    lstResultadoOpenMes[str(dt.month)] = lstResultadoOpenMes[str(dt.month)] + 1
                else:
                    lstResultadoOpenMes[str(dt.month)] = 1
            lstOGV["lstResultadoHowMeet"] = lstResultadoHowMeet
            lstOGV["lstResultadoOpenUniversidad"] = lstResultadoOpenUniversidad
            lstOGV["lstResultadoOpenMes"] = lstResultadoOpenMes
        return lstOGV

    def __ConsultarDatos(self, Api, params, id_aplicacion):

        data = Api.Item.filter(
            int(id_aplicacion), params
        )["items"]
        fields = [self.objExtraerInformacionPodio.makeDict(item, nested=Api,lstFields=['howmet-2','university','created_on']) for item in data]

        return fields

