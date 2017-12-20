from django.shortcuts import render, redirect
from django.http import HttpResponse
from Expa.ExpaToken import ExpaToken
from lcperformance.models import product
from datetime import datetime
import json
from standarsTools.process.Administracion import Administracion

# Create your views here.
def index(request):
    return render(request, 'index.html')

def iniciarSesion(request):
    correo = request.GET.get('correo')
    password = request.GET.get('password')
    objExpaToken = ExpaToken(correo, password)
    token = objExpaToken.getToken()
    if token != None:
        request.session["token"] = token
        objAdministracion = Administracion()
        resultado, currentOffice = objAdministracion.currentOffice(token)
        if len(currentOffice) > 0 and resultado:
            request.session['comite_id'] = currentOffice[0]['id']
            request.session["token_admin"] = objAdministracion.getTokenAdmin()
            jsonData = {
                "result": True,
                "mensaje": "Correcto"
            }
        else:
            del request.session['token']
            jsonData = {
                "result": False,
                "mensaje": "Actualmente no cuenta con rol en expa"
            }
    else:
        jsonData = {
            "result": False,
            "mensaje": "Usuario o contraseña incorrectos"
        }
    return HttpResponse(json.dumps(jsonData), content_type="application/json")

def seguimientoIndex(request):
    if "token" in request.session.keys():
        lstProduct = product.objects.all()
        return render(request, 'seguimiento.html', {'lstProduct': lstProduct})
    else:
        return redirect('/estandares_tools/')

def seguimientoConsulta(request):
    if "token" in request.session.keys():
        fechaInicio = request.GET.get('fechaInicio')
        fechaFin = request.GET.get('fechaFin')
        objProducto = product.objects.filter(id = int(request.GET.get('producto')))[0]
        producto = objProducto.code_expa
        idComite = request.session['comite_id']
        per_page = request.GET.get('per_page')
        page = request.GET.get('page')
        type_expa = objProducto.type_expa
        objAdministracion = Administracion()
        if(type_expa == "person"):
            resultado, data = objAdministracion.consulRealizeOgx(request.session["token_admin"], fechaInicio, fechaFin,
                                                                 producto, idComite, per_page, page)
        else:
            resultado, data = objAdministracion.consulRealizeIgx(request.session["token_admin"], fechaInicio, fechaFin
                                                                 , producto, idComite, per_page, page)
        return HttpResponse(json.dumps({'resultado': resultado, 'data': data['data']}), content_type="application/json")
    else:
        return redirect('/estandares_tools/')

def finishSinStandarIndex(request):
    if "token" in request.session.keys():
        lstProduct = product.objects.all()
        return render(request, 'finish_sin_standars.html', {'lstProduct': lstProduct})
    else:
        return redirect('/estandares_tools/')

def finishSinStandarConsulta(request):
    if "token" in request.session.keys():
        fechaInicio = request.GET.get('fechaInicio')
        fechaFin = request.GET.get('fechaFin')
        objProducto = product.objects.filter(id = int(request.GET.get('producto')))[0]
        producto = objProducto.code_expa
        idComite = request.session['comite_id']
        per_page = request.GET.get('per_page')
        page = request.GET.get('page')
        type_expa = objProducto.type_expa
        objAdministracion = Administracion()
        lstResultado = []
        if(type_expa == "person"):
            resultado, data = objAdministracion.consulRealizeOgx(request.session["token_admin"], fechaInicio, fechaFin,
                                                                 producto, idComite, per_page, page)
        else:
            resultado, data = objAdministracion.consulRealizeIgx(request.session["token_admin"], fechaInicio, fechaFin
                                                                 , producto, idComite, per_page, page)

        for dato in data['data']:
            person = dato['person'];
            opportunity = dato['opportunity']
            lstStandards = dato['standards']

            ahora = datetime.now()
            fechaFinal = datetime.strptime(opportunity['latest_end_date'].split('T')[0], "%Y-%m-%d")

            if (ahora > fechaFinal):
                home_lc = ""
                print(type_expa)
                if (type_expa == "person"):
                    home_lc = person['home_lc']['name']
                else:
                    home_lc = opportunity['office']['name']

                row = {'nombre': person['full_name']
                    , 'email': person['email']
                    , 'comite': home_lc
                    , 'fecha_inicio': opportunity['earliest_start_date']
                    , 'fecha_fin': opportunity['latest_end_date']
                    , 'numero_standar': 0}
                numeroStand = 0
                respuestas = 0
                for standards in lstStandards:
                    numeroStand = numeroStand + 1
                    print(standards['option'])
                    if standards['option'] != None:
                        respuestas = respuestas + 1
                row['numero_standar'] = str(numeroStand) + "/" + str(respuestas)
                if numeroStand > respuestas:
                    lstResultado.append(row)

        return HttpResponse(json.dumps({'resultado': resultado, 'data': lstResultado, 'numeroDatos': len(data['data'])}), content_type="application/json")
    else:
        return redirect('/estandares_tools/')




def salir(request):
    del request.session['token']
    del request.session['comite_id']
    del request.session["token_admin"]
    return redirect('/estandares_tools/')