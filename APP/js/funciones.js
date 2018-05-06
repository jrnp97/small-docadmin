//Validacion de tipo de busqueda para mostrar parametros de busqueda fechas.
$(document).ready(function(){
	$("#fechas").hide();	
	$("#tipobusqueda").change(function(){
		if (this.value == 5 | this.value ==7) {
			$("#buscar").show();
			$("#fechas").show();	
		}else if(this.value == 6){
			$("#buscar").hide();
			$("#fechas").show();
		}else{
			$("#buscar").show();
			$("#fechas").hide();
		};    
	}); 

	$(function() {
    	$( ".fecha" ).datepicker();
    	$( ".fecha" ).datepicker( "option", "dateFormat", "yy-mm-dd" );
	});  

  //Para validar que el campo solo sea numerico.
  $('.input_num').keyup(function () {
    this.value = this.value.replace(/[^0-9]/g,''); 
  });   

  //Validacion de formulario
  $('.submit').click(function(){
    var msjError = "";
    var convenio = $('input[name=convenio]').val();
    var numid = $('input[name=numid]').val();
    var apellidos = $('input[name=apellidos]').val();
    var nombres = $('input[name=nombres]').val();
    var edad = $('input[name=edad]').val();
    var direccion = $('input[name=direccion]').val();
    var telefono = $('input[name=telefono]').val();
    var firma = $('input[name=firmaconsentimiento]').val();
    
    if (convenio == "") {
      msjError += "Convenio no puede estar vacio.\n";      
    }    
    if (numid == "") {
      msjError += "Identificación no puede estar vacio.\n";      
    }
    if (apellidos == "") {
      msjError += "Apellidos no puede estar vacio.\n";      
    }
    if (nombres == "") {
      msjError += "Nombres no puede estar vacio.\n";      
    }
    if (edad == "") {
      msjError += "Edad no puede estar vacio.\n";      
    }
    if (direccion == "") {
      msjError += "Dirección no puede estar vacio.\n";      
    }    
    if (telefono == "") {
      msjError += "Teléfono no puede estar vacio.\n";      
    }  
    if (firma == "") {
      msjError += "Firma del paciente no puede estar vacio.\n";      
    }

    if (msjError == "" ) {
      return true;
    }else{
      alert(msjError);
      return false;
    }

  }); // fin validacion Formulario.

  //Funciones para autollenado Valoraciones. 
  //Craneal/ Facial/ Cervical
  $("#valo_cfc").change(function(){
    if ($("#valo_cfc:checked").length == 1) {

      $('textarea[name=cfc]').val("Normo céfalo, no limitación a la movilización cervical.");    
    }else{
      $('textarea[name=cfc]').val("");
    }  
  });
  //Sistema Respiratorio
  $("#valo_sr").change(function(){
    if ($("#valo_sr:checked").length == 1) {
      $('textarea[name=sisrespiratorio]').val("Pulmones buena entrada de aire bilateral,  buena mecánica respiratoria, murmullo vesicular conservado.");   
    }else{
      $('textarea[name=sisrespiratorio]').val("");
    }  
  });
  //Sistema Cardiovascular
  $("#valo_sc").change(function(){
    if ($("#valo_sc:checked").length == 1) {
      $('textarea[name=siscardiovascular]').val("Ruidos cardiacos rítmicos, R1 R2 en 4 focos, silencios impresionan libres. Paciente hemodinamicamente estable.");
    }else{
      $('textarea[name=siscardiovascular]').val("");
    }  
  });
  //Abdomen
  $("#valo_abd").change(function(){
    if ($("#valo_abd:checked").length == 1) {
      $('textarea[name=abdomen]').val("Blando depresible, no masas ni megalias, ruidos hidroaereos positivos, no signos peritoneales.");
    }else{
      $('textarea[name=abdomen]').val("");
    }  
  });  
  //Extremidades
  $("#valo_ext").change(function(){
    if ($("#valo_ext:checked").length == 1) {
      $('textarea[name=extremidades]').val("Móviles, Eutróficas, sin limitación funcional. Pulsos presentes buena perfusión distal.");
    }else{
      $('textarea[name=extremidades]').val("");
    }  
  }); 
  //Sistema Nervioso
  $("#valo_sn").change(function(){
    if ($("#valo_sn:checked").length == 1) {
      $('textarea[name=sisnervioso]').val("Pupilas isocoricas  normo reactivas, Glasgow 15/15,  sin déficit motor ni sensitivo.");
    }else{
      $('textarea[name=sisnervioso]').val("");
    }  
  });
  //Fin funciones autorrelleno valoracion
  /*$("#valoracion").change(function(){
    if ($("#valoracion:checked").length == 1) {
      $('textarea[name=cfc]').val("Normo céfalo, no limitación a la movilización cervical.");
      $('textarea[name=sisrespiratorio]').val("Pulmones buena entrada de aire bilateral,  buena mecánica respiratoria, murmullo vesicular conservado.");
      $('textarea[name=siscardiovascular]').val("Ruidos cardiacos rítmicos, R1 R2 en 4 focos, silencios impresionan libres. Paciente hemodinamicamente estable.");
      $('textarea[name=abdomen]').val("Blando depresible, no masas ni megalias, ruidos hidroaereos positivos, no signos peritoneales.");
      $('textarea[name=extremidades]').val("Móviles, Eutróficas, sin limitación funcional. Pulsos presentes buena perfusión distal.");
      $('textarea[name=sisnervioso]').val("Pupilas isocoricas  normo reactivas, Glasgow 15/15,  sin déficit motor ni sensitivo.");
    }else{
      $('textarea[name=cfc]').val("");
      $('textarea[name=sisrespiratorio]').val("");
      $('textarea[name=siscardiovascular]').val("");
      $('textarea[name=abdomen]').val("");
      $('textarea[name=extremidades]').val("");
      $('textarea[name=sisnervioso]').val("");
    }  
  });*/
  
  //Inicializamos los divs ocultos
  $("#rechaza_select").hide();
  $("textarea[name=consentimiento]").val("Con la presente autorizo a OPENSALUD a prestar atención o traslado y todas las acciones consecuentes derivadas del mismo. Renuncio a repelar legalmente contra su personal médico, paramédico y compañía en general.");
  //Funcion valida firma acepta o rechaza
  $("select[name=concent_info]").change(function(){
    var select = $("select[name=concent_info]").val();
    if (select == "acepta") {
      $("#rechaza_select").hide();
      $("#consentimiento_div").show();
      $("textarea[name=consentimiento]").val("Con la presente autorizo a OPENSALUD a prestar atención o traslado y todas las acciones consecuentes derivadas del mismo. Renuncio a repelar legalmente contra su personal médico, paramédico y compañía en general.");
        
    }else{    
      $("#rechaza_select").show();
      $("#consentimiento_div").show();
      $("textarea[name=consentimiento]").val("Me niego a recibir atención medica, traslado o internación, siendo informado de las posibles consecuencias y corriendo los riesgos bajo mi responsabilidad. Firmo declarando que me encuentro en pleno uso y razón de mis facultades mentales.");
    }

  });// Fin funcion valida acepta o rechaza

  //Funcion valida tipo de atencion, si es traslado mostrar div tripulacion de lo contrario ocultar
  $("#tripulacion_ul").hide();
  $("#tripulacion_div").hide();
  $("#origen_ul").hide();
  $("#origen_div").hide();

  $("select[name=ClasificacionDelServicio]").change(function(){
    var select = $("select[name=ClasificacionDelServicio]").val();
    if (select != "Translado") {      
      $("#tripulacion_ul").hide();
      $("#tripulacion_div").hide();        
      $("#origen_ul").hide();
      $("#origen_div").hide();      
    }else{    
      $("#tripulacion_ul").show();
      $("#tripulacion_div").show();
      $("#origen_ul").show();
      $("#origen_div").show();      
    }

  });// Fin funcion valida tipo atencion


});

$(document).ready(function(){

});

//Validacion de sexo para mostrar la opcion de ginecostetra
$(document).ready(function(){
	$("#gineco_ul").hide();
	$("#gineco_div").hide();
	
	$("#sexo").change(function(){
		if (this.value == 'Femenino') {
			$("#gineco_ul").show();
			$("#gineco_div").show();	
		}else{
			$("#gineco_ul").hide();
			$("#gineco_div").hide();
		};    
	});
});

//funcion para la carga de los diagnosticos.
 $(function() {
        function llenar(diagnostico){
            var diag = $('textarea[name=impresiondiagnostica]').val();
            $('textarea[name=impresiondiagnostica]').val(diag ? diag+"\n"+diagnostico : diagnostico);
            //$('input[name=bdiagnostico]').val('');
        }
 
    $( "#diagnostico" ).autocomplete({
      source: function( request, response ) {
        $.ajax({
          type:'POST',
          url:'historiaController.php',
          dataType:'JSON',
          //dataType: "jsonp",
          data: {
            buscar: request.term
          },
          success: function( data ) {
            response( data );
          }
        });
      },
      minLength: 3,
      select: function( event, ui ) {
          llenar(ui.item ? ui.item.value+" - "+ui.item.label : this.value);
      }

    });
  }); 

