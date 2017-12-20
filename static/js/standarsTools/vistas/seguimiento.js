$(document).ready(function(){
    $("#nvSeguimiento").addClass('active');
    var tblSeguimiento = $("#tblSeguimiento").DataTable(
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
                url: '/estandares_tools/seguimiento_consulta/',
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
            tblSeguimiento.clear().draw();
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
                var row = [
                        ""
                        ,""
                        ,""
                        ,""
                        ,""
                        ,""
                        ,""
                        ,""
                        ,""
                        ,""
                        ,""
                        ,""
                        ,""
                        ,""
                        ,""
                        ,""
                        ,""
                        ,""
                        ,""
                        ,""
                         ,""
                        ,""

                ];


                var person = value.person;
                var opportunity = value.opportunity;
                var standards = value.standards;
                row[0] = person.full_name;
                row[1] = person.email;

                row[3] = opportunity.earliest_start_date;
                row[4] = opportunity.latest_end_date;
                row[5] = value.current_status;
                if($("#cmbProducto option:selected").attr('data-expa') == "person"){
                    row[2] = person.home_lc.name;
                }else{
                    row[2] = opportunity.office.name;
                }

                $.each(standards, function (index, value) {
                    var position = value.position + 5;
                    var option = "";
                    if(value.option == null){
                        row[position] = "Sin contestar";
                    }else{
                        row[position] = value.option;
                    }

                });
                tblSeguimiento.row.add(row).draw();



               lstResultado.push(value);
            });
            if(data.data.length >= 50){
                page++;
                consultar()
            }else {
                 sweetAlert.close();
                console.log(lstResultado);
                $("#tblSeguimiento tr td:contains('true')").css('background-color', 'green');
                $("#tblSeguimiento tr td:contains('false')").css('background-color', 'red');

            }
        }

    }
});