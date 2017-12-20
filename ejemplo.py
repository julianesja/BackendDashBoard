from datetime import datetime

fechaFinal = "2017-12-26T00:00:00Z"
fechaInicio = "2017-05-15T00:00:00Z"
vecfecha = fechaFinal.split('T')
ahora = datetime.now()

dtFechaFinal = datetime.strptime(fechaFinal.split("T")[0], "%Y-%m-%d")
dtFechaInicial = datetime.strptime(fechaInicio.split("T")[0], "%Y-%m-%d")

if(dtFechaFinal < ahora):
    print("mostrar")


