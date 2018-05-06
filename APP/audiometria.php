<?php
/**
 * Created by PhpStorm.
 * User: Jaime
 * Date: 5/4/2018
 * Time: 1:10 PM
 */
global $tipo_exam;
$tipo_exam = "Auditivo";

?>

<!DOCTYPE html>
<html>
<?php include "base/head.html"; ?>

<body>
    <?php include "base/navbar.html"; ?>

    <?php include "base/menu.html"; ?>

    <?php include "forms/audiologica.html"; ?>

    <?php include "base/scripts.html"; ?>

    <script type="application/javascript">
        //Checkbox for audiologica tipo de proteccion auditiva
        $('#prot_auditiva_si').click(function(){
            $('#tipo_prot_auditiva').append("<div id='loaded'> \ " +
                "<label for='t_pro_auditiva'>Tipo de proteccion auditiva</label>\ " +
                "<input type='text' class='form-control' name='t_pro_auditiva' id='t_pro_auditiva' value=''/> \
                </div>");
        })

        $('#prot_auditiva_no').click(function(){
            $('#loaded').remove();
        })
    </script>
</body>
</html>
