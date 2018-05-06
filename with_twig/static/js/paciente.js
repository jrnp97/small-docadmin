$(function(){
   /* Ponemos evento blur a la escucha sobre id nombre en id paciente. */
   $('#div_center').on('blur','#numid',function(){
      /* Obtenemos el valor del campo */
      var valor = this.value;
      /* Si la longitud del valor es mayor a 2 caracteres.. */
      if(valor.length>=3){
 
         /* Cambiamos el estado.. */
         $('#estado').html('Cargando datos de servidor...');
 
         /* Hacemos la consulta ajax */
         var consulta = $.ajax({
            type:'POST',
            url:'pacienteController.php',
            data:{identificacion:valor},
            dataType:'JSON'
         });
 
         /* En caso de que se haya retornado bien.. */
         consulta.done(function(data){
            if(data.error!==undefined){
               $('#estado').html('Ha ocurrido un error: '+data.error);
               return false;
            } else {
               if(data.Apellidos!==undefined){$('#div_center #apellidos').val(data.Apellidos);}
               if(data.Nombres!==undefined){$('#div_center #nombres').val(data.Nombres);}
               //$(“#provincia > option[value="+ valor +"]“).attr(“selected”,true)
               if(data.TipoIdentificacion!==undefined){$('#div_center #tipoidentificacion').val(data.TipoIdentificacion);}
               if(data.Edad!==undefined){$('#div_center #edad').val(data.Edad);}
               if(data.TipoEdad!==undefined){$('#div_center #Tipoedad').val(data.TipoEdad);}
               if(data.Sexo!==undefined){$('#div_center #sexo').val(data.Sexo);}
               if(data.EstadoCivil!==undefined){$('#div_center #ecivil').val(data.EstadoCivil);}
               if(data.Ocupacion!==undefined){$('#div_center #ocupacion').val(data.Ocupacion);}
               if(data.Residencia!==undefined){$('#div_center #direccion').val(data.Residencia);}
               if(data.Municipio!==undefined){$('#div_center #municipio').val(data.Municipio);}
               if(data.Telefono!==undefined){$('#div_center #telefono').val(data.Telefono);}

               $('#estado').html('Datos cargados..');
               return true;
            }
         });
 
         /* Si la consulta ha fallado.. */
         consulta.fail(function(){
            $('#estado').html('Ha habido un error contactando el servidor.');
            return false;
         });
 
      } else {
         /* Mostrar error */
         $('#estado').html('El nombre tener una longitud mayor a 2 caracteres...');
         return false;
      }
   });
});

$(function(){
   /* Ponemos evento blur a la escucha sobre id nombre en id acompañante. */
   $('#div_center').on('blur','#numidacom',function(){
      /* Obtenemos el valor del campo */
      var valor = this.value;
      /* Si la longitud del valor es mayor a 2 caracteres.. */
      if(valor.length>=3){
 
         /* Cambiamos el estado.. */
         $('#estado').html('Cargando datos de servidor...');
 
         /* Hacemos la consulta ajax */
         var consulta = $.ajax({
            type:'POST',
            url:'pacienteController.php',
            data:{identacom:valor},
            dataType:'JSON'
         });
 
         /* En caso de que se haya retornado bien.. */
         consulta.done(function(data){
            if(data.error!==undefined){
               $('#estado').html('Ha ocurrido un error: '+data.error);
               return false;
            } else {
               if(data.TipoIdentificaciona!==undefined){$('#div_center #tipoidentificacionacom').val(data.TipoIdentificaciona);}
               if(data.Apellidosa!==undefined){$('#div_center #apellidosacom').val(data.Apellidosa);}
               if(data.Nombresa!==undefined){$('#div_center #nombresacom').val(data.Nombresa);}
               if(data.Parentesco!==undefined){$('#div_center #parentesco').val(data.Parentesco);}
               if(data.Telefonoa!==undefined){$('#div_center #telefonoacom').val(data.Telefonoa);}
               
               $('#estado').html('Datos cargados..');
               return true;
            }
         });
 
         /* Si la consulta ha fallado.. */
         consulta.fail(function(){
            $('#estado').html('Ha habido un error contactando el servidor.');
            return false;
         });
 
      } else {
         /* Mostrar error */
         $('#estado').html('El nombre tener una longitud mayor a 2 caracteres...');
         return false;
      }
   });
});