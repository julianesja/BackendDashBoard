from Expa.ExpaToken import ExpaToken
from Expa.AnalitycExpa import AnalitycExpa
from datetime import datetime, timedelta
from lcperformance.models import product, cumplido, comite, custumer_stage

"""Esta clase se encarga de consultar la informacion de expa y guardarla en la base de datos """


class LcPerformance():
    def __init__(self):
        """ codigo index """

    """Este Metodo se encarga consulta la informacion de expa y la guarda en la base de datos"""

    def SaveLcs(self):
        """Declaracion de variables"""
        objExpaToken = ExpaToken("dev.colombia@ai.aiesec.org", "ITcolombia1718")
        Token = objExpaToken.getToken()
        objAnalitycExpa = AnalitycExpa(Token)
        for p in product.objects.all():
            date_now = datetime.now()
            blResultado, jsonBuckets = objAnalitycExpa.ConsultCountry(date_now, date_now, p.code_expa, p.type_expa,
                                                                      1551)
            if blResultado:
                for jsonComite in jsonBuckets:
                    intCodeComite = jsonComite["key"]

                    objComite = comite.objects.filter(code_expa=int(intCodeComite))[0]
                    lstCustomerStage = custumer_stage.objects.all()
                    for CustomerStage in lstCustomerStage:
                        intValueCumpplido = 0
                        if CustomerStage.code_expa == "total_realized":
                            intValueCumpplido = int(jsonComite["total_realized"]["doc_count"])

                        elif CustomerStage.code_expa == "total_finished":
                            intValueCumpplido = int(jsonComite["total_realized"]["doc_count"])

                        elif CustomerStage.code_expa == "total_completed":
                            intValueCumpplido = int(jsonComite["total_completed"]["doc_count"])

                        elif CustomerStage.code_expa == "total_applications":
                            intValueCumpplido = int(jsonComite["total_applications"]["doc_count"])

                        elif CustomerStage.code_expa == "total_an_accepted":
                            intValueCumpplido = int(jsonComite["total_an_accepted"]["unique_profiles"]["value"])

                        elif CustomerStage.code_expa == "total_approvals":
                            intValueCumpplido = int(jsonComite["total_approvals"]["doc_count"])

                        elif CustomerStage.code_expa == "total_matched":
                            intValueCumpplido = int(jsonComite["total_matched"]["unique_profiles"]["value"])

                        lstCumplidoExist = cumplido.objects.filter(code_comite=objComite,
                                                                   date=date_now,
                                                                   code_product=p,
                                                                   code_custumer_stage=CustomerStage)
                        if len( lstCumplidoExist) > 0:
                            objCumplidoExits = lstCumplidoExist[0]
                            cumplido.objects.filter(code_comite=objComite,
                                                    date=date_now,
                                                    code_product=p,
                                                    code_custumer_stage=CustomerStage).update(quantity=intValueCumpplido)

                        else:
                            objcumplido = cumplido(code_comite=objComite,
                                                   date=date_now,
                                                   code_product=p,
                                                   quantity=intValueCumpplido,
                                                   code_custumer_stage=CustomerStage)

                            objcumplido.save()

    def SaveLcsInicial(self):
        #340
        """Declaracion de variables"""
        objExpaToken = ExpaToken("dev.colombia@ai.aiesec.org", "ITcolombia1718")
        Token = objExpaToken.getToken()
        objAnalitycExpa = AnalitycExpa(Token)
        for dayInitial in range(0, 30):
            for p in product.objects.all():
                date_now = datetime.strptime("2017-08-01", "%Y-%m-%d") - timedelta(days=dayInitial)
                blResultado, jsonBuckets = objAnalitycExpa.ConsultCountry(date_now, date_now, p.code_expa, p.type_expa,
                                                                          1551)
                if blResultado:
                    for jsonComite in jsonBuckets:
                        intCodeComite = jsonComite["key"]

                        objComite = comite.objects.filter(code_expa=int(intCodeComite))[0]
                        lstCustomerStage = custumer_stage.objects.all()
                        for CustomerStage in lstCustomerStage:
                            intValueCumpplido = 0
                            if CustomerStage.code_expa == "total_realized":
                                intValueCumpplido = int(jsonComite["total_realized"]["doc_count"])

                            elif CustomerStage.code_expa == "total_finished":
                                intValueCumpplido = int(jsonComite["total_finished"]["doc_count"])

                            elif CustomerStage.code_expa == "total_completed":
                                intValueCumpplido = int(jsonComite["total_completed"]["doc_count"])

                            elif CustomerStage.code_expa == "total_applications":
                                intValueCumpplido = int(jsonComite["total_applications"]["applicants"]["value"])

                            elif CustomerStage.code_expa == "total_an_accepted":
                                intValueCumpplido = int(jsonComite["total_an_accepted"]["unique_profiles"]["value"])

                            elif CustomerStage.code_expa == "total_approvals":
                                intValueCumpplido = int(jsonComite["total_approvals"]["doc_count"])

                            elif CustomerStage.code_expa == "total_matched":
                                intValueCumpplido = int(jsonComite["total_matched"]["unique_profiles"]["value"])

                            lstCumplidoExist = cumplido.objects.filter(code_comite=objComite,
                                                                       date=date_now,
                                                                       code_product=p,
                                                                       code_custumer_stage=CustomerStage)
                            if len(lstCumplidoExist) > 0:
                                cumplido.objects.filter(code_comite=objComite,
                                                        date=date_now,
                                                        code_product=p,
                                                        code_custumer_stage=CustomerStage).update(quantity=intValueCumpplido)

                            else:
                                objcumplido = cumplido(code_comite=objComite,
                                                       date=date_now,
                                                       code_product=p,
                                                       quantity=intValueCumpplido,
                                                       code_custumer_stage=CustomerStage)

                                objcumplido.save()
