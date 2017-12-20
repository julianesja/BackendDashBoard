$(document).ready(function(){
    var txtCorreo = $("#txtCorreo");
    var txtPassword = $("#txtPassword");

    $("#btnIniciar").on("click", function () {
        if(txtCorreo.val() == "" ){
            swal("Alerta", "Ingrese el email", "warning");
        }else if (txtPassword.val() == ""){
            swal("Alerta", "Ingrese el password", "warning");
        }else{
            jQuery.ajax({
                    type: "GET",
                    url: '/estandares_tools/iniciar_sesion/',
                    data:  {'correo': txtCorreo.val(), 'password': txtPassword.val()} ,
                    //contentType: "application/json; charset=utf-8",
                    dataType: "json",
                    beforeSend: beforeSendAjax,
                    error: errorAjax,
                    success: successAjax,
                });
        }

        /*complete*/
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
            if(data.result){
                location.href = "./seguimiento_index";
            }else{
                swal("Error", data.mensaje, "error");
            }
        }
    });
});