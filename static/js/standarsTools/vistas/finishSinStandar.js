$(document).ready(function(){
    $("#nvFinishSinStandar").addClass('active');
    var tblFinishSinStandar = $("#tblFinishSinStandar").DataTable(
        {
            "scrollX": true,
            "language": {
            "url": "https://cdn.datatables.net/plug-ins/1.10.16/i18n/Spanish.json"
            },
            dom: 'Bfrtip',
            buttons: [
                'copy', 'csv', 'excel', 'pdf', 'print'
            ],
             "paging": false,
            "scrollY":        "450px",
            "scrollCollapse": true,
        });
    var per_page = 50;
    var page = 0;
    var lstResultado = [];
    $('select').material_select();
    $('.datepicker').pickadate({
        selectMonths: true, // Creates a dropdown to control month
        selectYears: 15, // Creates a dropdown of 15 years to control year,
        today: 'Today',
        clear: 'Clear',
        close: 'Ok',
        closeOnSelect: false, // Close upon selecting a date,
        format: 'yyyy-mm-dd'
    });

    function consultar() {
        var fechaInicio = $("#txtFechaInicial").val();
        var fechaFin = $("#txtFechaFinal").val();
        var producto = $("#cmbProducto").val();
        jQuery.ajax({
                type: "GET",
                url: '/estandares_tools/finish_sin_standar_consulta',
                data:  {
                    'fechaInicio':fechaInicio
                    , 'fechaFin': fechaFin
                    , 'producto': producto
                   , 'per_page': per_page
                , 'page': page} ,
                //contentType: "application/json; charset=utf-8",
                dataType: "json",
                beforeSend: beforeSendAjax,
                error: errorAjax,
                success: successAjax,
        });
    }


    $("#btnGuardar").on("click", function () {
        if($('#txtFechaInicial').val() == ""){
            swal("Alerta", "Seleccione una fecha de inicio", "warning");
        }else if ($('#txtFechaFinal').val() == ""){
            swal("Alerta", "Seleccione una fecha final", "warning");
        }else{
            tblFinishSinStandar.clear().draw();
            page = 1;
            lstResultado = [];
            consultar();
        }
    });
    function beforeSendAjax(data) {
        swal({title:"Cargando..."
                    , text: '<div style="position:relative;height:110px"> <div style="position: absolute;right:40%" class="loader"></div> </div> '
                    , html: true
                    , showConfirmButton : false,});
    }

    /*error*/
    function errorAjax(data) {
        console.log(data);
    }
    /*Susses*/
    function successAjax(data) {
        if(data.resultado){
            $.each(data.data, function (index, value) {
                tblFinishSinStandar.row.add([
                    value.nombre
                    ,value.email
                    ,value.comite
                    ,value.fecha_inicio
                    ,value.fecha_fin
                    ,value.numero_standar
                ]).draw();
               lstResultado.push(value);
            });
            if(data.numeroDatos >= 50){
                page++;
                consultar()
            }else {
                 sweetAlert.close();
                console.log(lstResultado);
            }
        }

    }
});