from lcperformance.models import comite, product, custumer_stage, cumplido, target_product, user_register
from django.db.models import Sum
from datetime import datetime, timedelta
from Expa.ExpaToken import ExpaToken
from Expa.AnalitycExpa import AnalitycExpa
class ConsultaLCPerformance:

    def consulta(self, dateInicial, dateFinal, lstProgram):
        dti = datetime.strptime(dateInicial, "%Y-%m-%d")
        dtf = datetime.strptime(dateFinal, "%Y-%m-%d")
        lstResultado = {}
        lstComite = comite.objects.all()
        lstPrograma = product.objects.filter(id__in=lstProgram)
        lstCustomerStage = custumer_stage.objects.all()
        for lc in lstComite:
            lstResultado[lc.name] = {}
            for prod in lstPrograma:
                lstResultado[lc.name][prod.name] = {}
                for customer in lstCustomerStage:
                    lstResultado[lc.name][prod.name][customer.name] = {
                        "plan": 0,
                        "cumplido": 0,
                        "porcentajeCumplimiento": 0,
                        "gab": 0,
                        "crecimientoabs": 0,
                        "crecimientorelativo": 0
                    }
                    lcPlan = target_product.objects.filter(code_comite=lc.id,
                                                           code_product=prod.id,
                                                           code_custumer_stage=customer.id,
                                                           code_weekly_id__init_date__gte=dti,
                                                           code_weekly_id__final_date__lte=dtf
                                                           ).aggregate(Sum('target'))
                    lcCumplido = cumplido.objects.filter(code_comite=lc.id,
                                                         code_product=prod.id,
                                                         code_custumer_stage=customer.id,
                                                         date__range=((dti - timedelta(days=1)), (dtf + timedelta(days=1)))
                                                         ).aggregate(Sum('quantity'))

                    """lcAnterior = cumplido.objects.filter(code_comite=lc.id,
                                                         code_product=prod.id,
                                                         code_custumer_stage=customer.id,
                                                         date__range=(dti - timedelta(year=1)
                                                        , dtf - timedelta(year=1))
                                                         ).aggregate(Sum('quantity'))"""



                    if lcPlan["target__sum"] == None:
                        lcPlan["target__sum"] = 0

                    if lcCumplido["quantity__sum"] ==None:
                        lcCumplido["quantity__sum"] = 0


                    print(lcCumplido["quantity__sum"])

                    print(lcPlan["target__sum"])
                    if (lcPlan["target__sum"] != 0):
                        porcentajeCumplimiento = (lcCumplido["quantity__sum"]*100)/lcPlan["target__sum"]
                    else:
                        porcentajeCumplimiento = lcCumplido["quantity__sum"]*100

                    gab = lcPlan["target__sum"] - lcCumplido["quantity__sum"]

                    lstResultado[lc.name][prod.name][customer.name] = {
                        "plan": lcPlan["target__sum"],
                        "cumplido": lcCumplido["quantity__sum"],
                        "porcentajeCumplimiento": porcentajeCumplimiento,
                        "gab": gab
                    }

        return lstResultado

    def consultaNueva(self, dateInicial, dateFinal, lstProgram):
        dti = datetime.strptime(dateInicial, "%Y-%m-%d")
        dtf = datetime.strptime(dateFinal, "%Y-%m-%d")
        objUserRegister = user_register.objects.filter(user_expa='dev.colombia@ai.aiesec.org')[0]

        lstResultado = {}
        lstPrograma = product.objects.filter(id__in=lstProgram)
        objExpaToken = ExpaToken(objUserRegister.user_expa, objUserRegister.password_expa)
        Token = objExpaToken.getToken()
        lstCustomerStage = custumer_stage.objects.all()
        for p in lstPrograma:
            objAnalitycExpa = AnalitycExpa(Token)
            blResultado, jsonBuckets = objAnalitycExpa.ConsultCountry(dti, dtf, p.code_expa, p.type_expa,
                                                                      1551)
            blResultadoAnioAnterior, jsonBucketsAnioAnterior \
                = objAnalitycExpa.ConsultCountry(dti - timedelta(days=365)
                                                 , dtf - timedelta(days=365)
                                                 , p.code_expa
                                                 , p.type_expa,
                                                1551)
            if(blResultado):
                for jsonComite in jsonBuckets:
                    intCodeComite = jsonComite["key"]
                    lc = comite.objects.filter(code_expa=int(intCodeComite))[0]
                    lstResultado[lc.name] = {}
                    lstResultado[lc.name][p.name] = {}
                    for customer in lstCustomerStage:
                        lstResultado[lc.name][p.name][customer.name] = {}
                        lcPlan = target_product.objects.filter(code_comite=lc.id,
                                                               code_product=p.id,
                                                               code_custumer_stage=customer.id,
                                                               code_weekly_id__init_date__gte=dti,
                                                               code_weekly_id__final_date__lte=dtf
                                                               ).aggregate(Sum('target'))
                        if lcPlan["target__sum"] == None:
                            lcPlan["target__sum"] = 0

                        intPlan = int(lcPlan["target__sum"])
                        intCumpplido = self.__getCumplido(customer, jsonComite)
                        intCumpplidoAnterior = self.__getValorAnterior(customer, blResultadoAnioAnterior, jsonBucketsAnioAnterior, lc)

                        if (intPlan != 0):
                            porcentajeCumplimiento = (intCumpplido * 100) / intPlan
                        else:
                            porcentajeCumplimiento = intCumpplido * 100

                        gab = intPlan - intCumpplido
                        crecimientoabs = intCumpplido - intCumpplidoAnterior
                        if intCumpplidoAnterior == 0:
                            crecimeintorelativo = (intCumpplido / 1)*100
                        else:
                            crecimeintorelativo = (intCumpplido / intCumpplidoAnterior) * 100

                        lstResultado[lc.name][p.name][customer.name] = {
                            "plan": intPlan,
                            "cumplido": intCumpplido,
                            "porcentajeCumplimiento": porcentajeCumplimiento,
                            "gab": gab,
                            "cumplidoAnioanterior": intCumpplidoAnterior,
                            "crecimientoabs": crecimientoabs,
                            "crecimeintorelativo": crecimeintorelativo

                        }
        return  lstResultado


    def __getValorAnterior(self, CustomerStage, blResultadoAnioAnterior, jsonBucketsAnioAnterior, lc):
        intValueCumpplido = 0
        if blResultadoAnioAnterior:
            for jsonComite in jsonBucketsAnioAnterior:
                if int(jsonComite["key"]) == lc.code_expa:
                    intValueCumpplido = self.__getCumplido(CustomerStage, jsonComite)
                    return intValueCumpplido
        return intValueCumpplido


    def __getCumplido(self, CustomerStage, jsonComite):
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
        return  intValueCumpplido







