<?php 

include_once 'pacienteDAO.php';

session_start();
$idpaciente=$_GET['id'];
if (!isset($_SESSION['idusuario'])) {
  echo "<script type='text/javascript'>
          alert('Contenido solo accesible para usuarios registrados.');
          window.location='index.php'
      </script>";
}

if(isset($_GET["id"])) {
  $oPaciente = new PacienteDAO;
  $aPacientes = $oPaciente->buscarPaciente($_GET["id"]);
}

?>

<!DOCTYPE html>
<html lang="es">
<head>
<title>Encuestas Pacientes</title>
<meta charset="utf-8" />
   <meta http-equiv="X-UA-Compatible" content="IE=edge">
   <meta name="viewport" content="width=device-width, initial-scale=1">
   <script src="http://code.jquery.com/jquery-latest.min.js" type="text/javascript"></script>
   <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0, user-scalable=no"/>
   <link rel="stylesheet" href="css/estiloapp.css" />
    <link rel="stylesheet" href="Bootstrap/css/bootstrap.css" />

    <link rel="stylesheet" href="http://code.jquery.com/ui/1.10.3/themes/smoothness/jquery-ui.css" />
  <script src="http://code.jquery.com/jquery-1.9.1.js"></script>
  <script src="http://code.jquery.com/ui/1.10.3/jquery-ui.js"></script>
  <script src="js/script_menu.js"></script>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js"></script>
<script type="text/javascript">
function CargarEncuesta(){
document.getElementById('CargarEncuesta').style.display = 'block';
}
function NuevaEncuesta(){
document.getElementById('NuevaEncuesta').style.display = 'block';
}
</script>
<script>
    $(function() {
 
        var enlace_movil = $('#nav-responsive'),
            menu = $('#responsive-menu').find('ul');
 
        enlace_movil.on('click', function (e) {
            e.preventDefault();
 
            var esto = $(this);
 
            esto.toggleClass('nav-active');
            menu.toggleClass('open-responsive-menu');
        })
 
    });
</script>
</head>
<body>
  <header> 
    <div id="logo"><img src="img/logo2.png"  height="180"></div>
    <div id="user"><?php echo "<img src='img/iconos/user.png' width='32' height='32'>  "."<a href='cerrarsesion.php'><img src='img/iconos/salir.png' width='32' height='32'></a> </br>".$_SESSION['nombre']  ; ?></div>     
  </header>

  <nav id="responsive-menu">
    <a class="nav-responsive" id="nav-responsive" href="#"></a> 
    <ul>
      <li></br><label>Historias</label><a href="historiaclinica.php"><img src="img/iconos/historias.png" width="40" height="40"></a> </li>
      <li></br><label>Pacientes</label> <a href="pacientePrincipal.php"><img src="img/iconos/pacientes.png" width="40" height="40"></a></li>
      <!--li></br><label>Medicos</label><a href="#"><img src="img/iconos/medico.png" width="40" height="40"></a></li-->
      <li></br><label>Reportes</label><a href="reportesPrincipal.php"><img src="img/iconos/reportes.png" width="40" height="40"></a></li>
      <?php
        if ($_SESSION['tipousuario']==1) {
          echo '<li></br><label>Usuarios</label><a href="usuarioPrincipal.php"><img src="img/iconos/user.png" width="40" height="40"></a></li>';
        }
      ?>           
    </ul>
  </nav>

  <div id="div_center"> 

   
<?php



$link = mysql_connect("209.239.120.108","opensaluds_admin", "OpenAdmin2014"); 
mysql_select_db("opensaluds_opensalud", $link); 

$consulta="SELECT * FROM encuesta WHERE idpaciente='$idpaciente'";
$result = mysql_query($consulta, $link)or die("Error  " . mysql_error());;

$row=mysql_fetch_array($result);



$idpe=$row['idpaciente'];
$nomacomp=$row['nombre_responsable'];
$idacomp=$row['id_responsable'];
$preg1=$row['preg1'];
$preg2=$row['preg2'];
$preg3=$row['preg3'];
$preg4=$row['preg4'];
$preg5=$row['preg5'];
$preg6=$row['preg6'];
$preg7=$row['preg7'];
$preg8=$row['preg8'];
$preg9=$row['preg9'];
$preg10=$row['preg10'];
$preg11=$row['preg11'];
$preg12=$row['preg12'];
$preg13=$row['preg13'];
$preg14=$row['preg14'];
$medico_visita=$row['medico_visita'];
$id_medico=$row['id_medico'];
$fecha_visita=$row['fecha_visita'];
$hora_visita=$row['hora_visita'];



if($idpaciente==$idpe )
{


  echo'Existe una encuesta diligenciada para este paciente</br>';
  echo'<button class="btn btn-primary" onclick="CargarEncuesta();">CARGAR ENCUESTA</button>';


}else{

  echo'No existe encuesta digilenciada para este paciente </br>';
  echo'<button class="btn btn-primary" onclick="NuevaEncuesta();">DILIGENCIAR ENCUESTA</button>';
}

?> 

<div id='CargarEncuesta' style='display:none;'>


        <div> 

<table>

<tr>

  <td colspan="4"> <h2>Encuesta</h2> </td>  

</tr>
<tr>

 <td colspan="4"><h4>Datos del paciente</br></td>

</tr>
<tr>

<td><strong>N° Identificacion:</strong></td>
<td><?php echo $aPacientes[0]['Identificacion']?></td>
<td><strong>Tipo Identificacion:</strong></td>
<td><?php echo $aPacientes[0]['TipoIdentificacion']?></td>

</tr>

<tr>
  <td><strong>Nombres:</strong></td>
<td><?php echo $aPacientes[0]['Nombres']?></td>  
<td><strong>Apellidos:</strong></td>
<td><?php echo $aPacientes[0]['Apellidos']?></td>  

</tr>

<tr>
  <td colspan="4"><h4>Datos de persona responsable</h4></td>
  </tr>
<tr>
  <td><strong>Nombre Completo:</strong></td>
<td><?php echo $nomacomp?></td>  
<td><strong>Identificacion:</strong></td>
<td><?php echo $idacomp?></td> 
</tr>



</table>
               
                  <!--span class="required_notification">* Datos requeridos</span-->      
         
              <h1>Resultados</h1>
 
              <table>
              <tr>

                <td><strong>Lista de Chequeo para garantizar la seguridad del paciente</strong></td>
                <td><strong>Respuesta</strong></td>
                </tr>
                 <!--pre1-->
                <tr>
                  <td> 
                   La vivienda cuenta con servicios públicos: Acueducto, alcantarillado.
                  </td>
                  <td>
                    <center><?php echo $preg1?></center>
                 </td>
                </tr>
                 
                 <tr>
                  <td> 
                 La vivienda cuenta con servicios de energía.
                  </td>
                  <td> <center><?php echo $preg2?></center>
                 </td>
                </tr>
                 
                 <tr>
                  <td> 
             La vivienda cuenta con telefonía fija o móvil.
                  </td>
                  <td> <center><?php echo $preg3?></center>
                 </td>
                </tr>

  <tr>
                  <td> 
           La vivienda cuenta con Baño adecuado para el 

paciente
                  </td>
                  <td> <center><?php echo $preg4?></center>
                 </td>
                </tr>

                  <tr>
                  <td> 
         Área para almacenamiento de residuos generados

en la atención de salud, para luego ser 

transportados por la empresa recolectora de 

residuos. (puede ubicarse la caneca roja para 

recolección de los residuos dentro del baño)
                  </td>
                  <td> <center><?php echo $preg5?></center>
                 </td>
                </tr>

                  <tr>
                  <td> 
         Se evidencia  Maletín Médico con: fonendoscopio,

tensiómetro, equipo de órgano pulsoxímetro, 

glucómetro, martillo, termómetro, metro
                  </td>
                  <td> <center><?php echo $preg6?></center>
                 </td>
                </tr>

                  <tr>
                  <td> 
             Se evidencia en el domicilio del paciente nevera, 

en caso de que los medicamentos requeridos por 

el paciente exijan que sea conservada la cadena 

de frío, cuando requiera resguardo de 

medicamentos en esas condiciones de 

temperatura
                  </td>
                  <td> <center><?php echo $preg7?></center>
                 </td>
                </tr>

                  <tr>
                  <td> 
            Se evidencia Maletín enfermería: con dispositivos 

médicos, según patología del paciente
                  </td>
                  <td> <center><?php echo $preg8?></center>
                 </td>
                </tr>

                  <tr>
                  <td> 
           Se evidencia Maletín con medicamentos de 

acuerdo con inventario establecido para uso en la 

atención en casa
                  </td>
                  <td> <center><?php echo $preg9?></center>
                 </td>
                </tr>

                  <tr>
                  <td> 
            Se evidencian Bombas de infusión para líquidos y

nutrición parenteral en caso de requerirlo el 

paciente
                  </td>
                  <td> <center><?php echo $preg10?></center>
                 </td>
                </tr>

                  <tr>
                  <td> 
             Se evidencia atriles
                  </td>
                  <td> <center><?php echo $preg11?></center>
                 </td>
                </tr>

                  <tr>
                  <td> 
     Se evidencia  la dotación de los elementos, 

insumos y equipos que  se requieren para  la 

atención del paciente y aquellos de protección 

personal, contenedores y bolsas para la 

clasificación, segregación y manipulación de los 

residuos biológicos- infecciosos generados en el 

domicilio del paciente.
                  </td>
                  <td><center><?php echo $preg12?></center>
                 </td>
                </tr>

                  <tr>
                  <td> 
            se evidencia ruta sanitaria en el  domicilio inscrito

al programa.
                  </td>
                  <td><center><?php echo $preg13?></center>
                 </td>
                </tr>

                  <tr>
                  <td> 
            se evidencia transporte asistencial  medicalizado
                  </td>
                  <td><center><?php echo $preg14?></center>
                 </td>
                </tr>

            

                 </table>

                 <table>
<tr>

  <td colspan="4"><h4>Datos de persona responsable de la visita</h4></td>


</tr>
    
             <tr>
             <td><strong>Nombre completo:</strong></td>
              <td><?php echo $medico_visita?></td>
             <td><strong>Identificacion:</strong></td>
              <td><?php echo $id_medico?></td>
              </tr>
             <tr>
             <td><strong>Fecha :</strong></td>
              <td><?php echo $fecha_visita?></td>
             <td><strong>Hora:</strong></td>
              <td><?php echo $hora_visita?></td>
              </tr>

            </table>
</div>
             </div>










<div id='NuevaEncuesta' style='display:none;'>

<form  class="contact_form" id="contact_form" method="post" action="registrarEncuestas.php">  
        <div> 
          <ul>
              <li>
                  <h2>Diligenciar Encuesta</h2>  
                  <!--span class="required_notification">* Datos requeridos</span-->      
              </li>
          </ul>
          <div class="ul_left">           
            <ul>
                  <h4>Datos del paciente</h4></br>
              <li>
                <label for="numid">N° Identificacion:</label>
                <input type="text"  id="numid" name="numid" value="<?php echo $aPacientes[0]['Identificacion']?>" required>
                <!--div id="estado">Esperando input.</div-->
              </li>
              <li>
                
                <label for="tipoidentificacion">Tipo:</label>
                 <input type="text"  id="tipoid" name="tipoid" value="<?php echo $aPacientes[0]['TipoIdentificacion']?>" required>
              </li>
              <li>
                <label for="apellidos">Apellidos:</label>
                <input type="text" id="apellidos" name="apellidos" value="<?php echo $aPacientes[0]['Apellidos']?>" required>
              </li>
              <li>
                <label for="nombres">Nombres:</label></td>
                <input type="text" id="nombres" name="nombres" value="<?php echo $aPacientes[0]['Nombres']?>" required>
              </li>
               <h4>Datos de persona responsable</h4></br>
               <li>
               <label for="numidr">N° Identificacion:</label>
                <input type="text"  id="numidr" name="numidr" required>
                <!--div id="estado">Esperando input.</div-->
              </li>
         
              <li>
                <label for="nombresr">Nombre Completo:</label></td>
                <input type="text" id="nombresr" name="nombresr"  required>
              </li>

              <h1>Encuesta</h1>
 
              <table>
              <tr>

                <td><strong>Lista de Chequeo para garantizar la seguridad del paciente</strong></td>
                <td><strong>Respuesta</strong></td>
                </tr>
                 <!--pre1-->
                <tr>
                  <td> 
                   La vivienda cuenta con servicios públicos: Acueducto, alcantarillado.
                  </td>
                  <td><select name="preg1">  
                        <option value="No hubo eleccion">ELEGIR </option>
                        <option value="SI">SI</option>
                        <option value="NO">No</option>
                        <option value="N/A">N/A</option>
                       
                      </select>
                 </td>
                </tr>
                 
                 <tr>
                  <td> 
                 La vivienda cuenta con servicios de energía.
                  </td>
                  <td><select name="preg2">      
                         <option value="No hubo eleccion">ELEGIR </option>               
                        <option value="SI">SI</option>
                        <option value="NO">No</option>
                        <option value="N/A">N/A</option>
                       
                      </select>
                 </td>
                </tr>
                 
                 <tr>
                  <td> 
             La vivienda cuenta con telefonía fija o móvil.
                  </td>
                  <td><select name="preg3">           
                   <option value="No hubo eleccion">ELEGIR </option>           
                        <option value="SI">SI</option>
                        <option value="NO">No</option>
                        <option value="N/A">N/A</option>
                       
                      </select>
                 </td>
                </tr>

  <tr>
                  <td> 
           La vivienda cuenta con Baño adecuado para el 

paciente
                  </td>
                  <td><select name="preg4">           
                   <option value="No hubo eleccion">ELEGIR </option>           
                        <option value="SI">SI</option>
                        <option value="NO">No</option>
                        <option value="N/A">N/A</option>
                       
                      </select>
                 </td>
                </tr>

                  <tr>
                  <td> 
         Área para almacenamiento de residuos generados

en la atención de salud, para luego ser 

transportados por la empresa recolectora de 

residuos. (puede ubicarse la caneca roja para 

recolección de los residuos dentro del baño)
                  </td>
                  <td><select name="preg5">           
                   <option value="No hubo eleccion">ELEGIR </option>           
                        <option value="SI">SI</option>
                        <option value="NO">No</option>
                        <option value="N/A">N/A</option>
                       
                      </select>
                 </td>
                </tr>

                  <tr>
                  <td> 
         Se evidencia  Maletín Médico con: fonendoscopio,

tensiómetro, equipo de órgano pulsoxímetro, 

glucómetro, martillo, termómetro, metro
                  </td>
                  <td><select name="preg6">           
                   <option value="No hubo eleccion">ELEGIR </option>           
                        <option value="SI">SI</option>
                        <option value="NO">No</option>
                        <option value="N/A">N/A</option>
                       
                      </select>
                 </td>
                </tr>

                  <tr>
                  <td> 
             Se evidencia en el domicilio del paciente nevera, 

en caso de que los medicamentos requeridos por 

el paciente exijan que sea conservada la cadena 

de frío, cuando requiera resguardo de 

medicamentos en esas condiciones de 

temperatura
                  </td>
                  <td><select name="preg7">           
                   <option value="No hubo eleccion">ELEGIR </option>           
                        <option value="SI">SI</option>
                        <option value="NO">No</option>
                        <option value="N/A">N/A</option>
                       
                      </select>
                 </td>
                </tr>

                  <tr>
                  <td> 
            Se evidencia Maletín enfermería: con dispositivos 

médicos, según patología del paciente
                  </td>
                  <td><select name="preg8">           
                   <option value="No hubo eleccion">ELEGIR </option>           
                        <option value="SI">SI</option>
                        <option value="NO">No</option>
                        <option value="N/A">N/A</option>
                       
                      </select>
                 </td>
                </tr>

                  <tr>
                  <td> 
           Se evidencia Maletín con medicamentos de 

acuerdo con inventario establecido para uso en la 

atención en casa
                  </td>
                  <td><select name="preg9">           
                   <option value="No hubo eleccion">ELEGIR </option>           
                        <option value="SI">SI</option>
                        <option value="NO">No</option>
                        <option value="N/A">N/A</option>
                       
                      </select>
                 </td>
                </tr>

                  <tr>
                  <td> 
            Se evidencian Bombas de infusión para líquidos y

nutrición parenteral en caso de requerirlo el 

paciente
                  </td>
                  <td><select name="preg10">           
                   <option value="No hubo eleccion">ELEGIR </option>           
                        <option value="SI">SI</option>
                        <option value="NO">No</option>
                        <option value="N/A">N/A</option>
                       
                      </select>
                 </td>
                </tr>

                  <tr>
                  <td> 
             Se evidencia atriles
                  </td>
                  <td><select name="preg11">           
                   <option value="No hubo eleccion">ELEGIR </option>           
                        <option value="SI">SI</option>
                        <option value="NO">No</option>
                        <option value="N/A">N/A</option>
                       
                      </select>
                 </td>
                </tr>

                  <tr>
                  <td> 
     Se evidencia  la dotación de los elementos, 

insumos y equipos que  se requieren para  la 

atención del paciente y aquellos de protección 

personal, contenedores y bolsas para la 

clasificación, segregación y manipulación de los 

residuos biológicos- infecciosos generados en el 

domicilio del paciente.
                  </td>
                  <td><select name="preg12">           
                   <option value="No hubo eleccion">ELEGIR </option>           
                        <option value="SI">SI</option>
                        <option value="NO">No</option>
                        <option value="N/A">N/A</option>
                       
                      </select>
                 </td>
                </tr>

                  <tr>
                  <td> 
            se evidencia ruta sanitaria en el  domicilio inscrito

al programa.
                  </td>
                  <td><select name="preg13">           
                   <option value="No hubo eleccion">ELEGIR </option>           
                        <option value="SI">SI</option>
                        <option value="NO">No</option>
                        <option value="N/A">N/A</option>
                       
                      </select>
                 </td>
                </tr>

                  <tr>
                  <td> 
            se evidencia transporte asistencial  medicalizado
                  </td>
                  <td><select name="preg14">           
                   <option value="No hubo eleccion">ELEGIR </option>           
                        <option value="SI">SI</option>
                        <option value="NO">No</option>
                        <option value="N/A">N/A</option>
                       
                      </select>
                 </td>
                </tr>

            

                 </table>

    <h4>Datos de persona responsable</h4></br>
               <li>
               <label for="nombrev">Responsable de la visita:</label>
                <input type="text"  id="nombrev" name="nombrev" required>
                <!--div id="estado">Esperando input.</div-->
              </li>
              <li>
                
                <label for="cedulav">Identificacion:</label>
                 <input type="text"  id="cedulav" name="cedulav"  required>
              </li>
              <li>
                <label for="fechav">Fecha Visita:</label>
            <input type="date" id="datepicker" name="fechav" value="<?php echo date('Y-m-d'); ?>" required/>
              </li>
              <li>
                <label for="horav">Hora Visita:</label></td>
            <input type="time"  name="horav" value="<?php echo date('H:i:s'); ?>" required/>
              </li> 

            </br>
            </br>


             <input class="btn btn-info"type="submit" value="Registrar Encuesta">
              
              </form>
       </br>
       </br>

</div>



            
             </div>


  </div>    




</body>
</html>